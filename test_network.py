# System libs
from modulefinder import Module
import os
import argparse
from distutils.version import LooseVersion
# Numerical libs
import numpy as np
import torch
import torch.nn as nn
from scipy.io import loadmat
import csv
# Our libs
from mit_semseg.dataset import My_Test_Dataset, TestDataset
from mit_semseg.models import ModelBuilder, SegmentationModule
from mit_semseg.utils import colorEncode, find_recursive, setup_logger
from mit_semseg.lib.nn import user_scattered_collate, async_copy_to
from mit_semseg.lib.utils import as_numpy
from PIL import Image
from tqdm import tqdm
from mit_semseg.config import cfg
import json

colors = loadmat('../data/color150.mat')['colors']
names = {}
with open('../data/object150_info.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        names[int(row[0])] = row[5].split(";")[0]


def visualize_result(data, pred, cfg):
    (img, info) = data
    
    img_name = info.split('/')[-1]
    # print predictions in descending order
    pred = np.int32(pred)
    pixs = pred.size
    uniques, counts = np.unique(pred, return_counts=True)
    print("Predictions in [{}]:".format(info))
    for idx in np.argsort(counts)[::-1]:
        name = names[uniques[idx] + 1]
        ratio = counts[idx] / pixs * 100
        if ratio > 0.1:
            print("  {}: {:.2f}%".format(name, ratio))

    # colorize prediction
    pred = pred.astype('int')
    pred_color = colorEncode(pred, colors).astype(np.uint8)
    
    with open(cfg.TEST.height_result,"rb") as f:
        data_infos = json.loads(f.read())
    
    data_info = {}
    
    for i in range(1,5):
        lable_bool = pred==i
        data_info[str(i)]=check_height(lable_bool)    
        lable_bool_rgb = np.expand_dims(lable_bool,axis=-1)
        lable_bool_rgb = np.concatenate([lable_bool_rgb,lable_bool_rgb,lable_bool_rgb],axis=-1)
        lable_bool_rgb_rev = lable_bool_rgb==False
        img_save = pred_color*lable_bool_rgb + img*lable_bool_rgb_rev
        
        if not os.path.exists(cfg.TEST.tem_result):
            os.mkdir(cfg.TEST.tem_result)
        Image.fromarray(img_save).save(
        os.path.join(cfg.TEST.tem_result, img_name.replace('.jpg', '_'+str(i)+'.png')))
    
    data_infos[img_name] = data_info
    with open(cfg.TEST.height_result,"w") as f:
        f.write(json.dumps(data_infos))
        
    pred_color_bg = pred==0
    pred_color_bg = np.expand_dims(pred_color_bg,axis=-1)
    pred_color_bg = np.concatenate([pred_color_bg,pred_color_bg,pred_color_bg],axis=-1)
    pred_color_bg = pred_color_bg==False
    pred_color = pred_color_bg*pred_color+(pred_color_bg==False)*img
    
    Image.fromarray(pred_color).save(
        os.path.join(cfg.TEST.result, img_name.replace('.jpg', '.png')))
        
    # aggregate images and save
    im_vis = np.concatenate((img, pred_color), axis=1)

    

def check_height(array):
    height_up = 0
    height_bottom = 0
    
    if not (True in array):
        return 0
    
    for (index,col) in enumerate(array):
        if True in col:
            height_up = index
    
    for index in range(index,array.shape[0]):
        if not(True in array[index]):
            height_bottom = index
    if height_bottom == 0:
        height_bottom = array.shape[0]
    
    return height_bottom-height_up
    

def test_infer(segmentation_module, loader:My_Test_Dataset, gpu, index:int):
    segmentation_module.eval()
    batch_data = loader.getitem(index)
    segSize = (batch_data['img_ori'].shape[0],
            batch_data['img_ori'].shape[1])
    img_resized_list = batch_data['img_data']

    with torch.no_grad():
        scores = torch.zeros(1, cfg.DATASET.num_class, segSize[0], segSize[1])
        scores = async_copy_to(scores, gpu)

        for img in img_resized_list:
            feed_dict = batch_data.copy()
            feed_dict['img_data'] = img
            del feed_dict['img_ori']
            del feed_dict['info']
            feed_dict = async_copy_to(feed_dict, gpu)

                    # forward pass
            pred_tmp = segmentation_module(feed_dict, segSize=segSize)
            scores = scores + pred_tmp / len(cfg.DATASET.imgSizes)

        _, pred = torch.max(scores, dim=1)
        pred = as_numpy(pred.squeeze(0).cpu())

            # visualization
    visualize_result(
                (batch_data['img_ori'], batch_data['info']),
                pred,
                cfg
            )


def main(cfg, gpu):
    torch.cuda.set_device(gpu)

    # Network Builders
    net_encoder = ModelBuilder.build_encoder(
        arch=cfg.MODEL.arch_encoder,
        fc_dim=cfg.MODEL.fc_dim,
        weights=cfg.MODEL.weights_encoder)
    net_decoder = ModelBuilder.build_decoder(
        arch=cfg.MODEL.arch_decoder,
        fc_dim=cfg.MODEL.fc_dim,
        # num_class=cfg.DATASET.num_class,
        num_class=5,
        weights=cfg.MODEL.weights_decoder,
        use_softmax=True)

    crit = nn.NLLLoss(ignore_index=-1)

    segmentation_module = SegmentationModule(net_encoder, net_decoder, crit)

    # Dataset and Loader
    dataset_test = My_Test_Dataset(
        cfg.list_test,
        cfg.DATASET)
    # loader_test = torch.utils.data.DataLoader(
    #     dataset_test,
    #     # batch_size=cfg.TEST.batch_size,
    #     batch_size=8,
    #     shuffle=False,
    #     collate_fn=user_scattered_collate,
    #     num_workers=5,
    #     drop_last=True)

    segmentation_module.cuda()

    # Main loop
    test_infer(segmentation_module, dataset_test, gpu,1)

    print('Inference done!')

def export_call(cfg,gpu):

    if os.path.isdir(cfg.TEST.imgs):
        imgs = find_recursive(cfg.TEST.imgs)
        imgs.sort(key=lambda x:float("".join(re.findall("\d",x))))
    else:
        imgs = [args.imgs]
    assert len(imgs), "imgs should be a path to image (.jpg) or directory."
    cfg.list_test = [{'fpath_img': x} for x in imgs]

    torch.cuda.set_device(gpu)
    # Network Builders
    net_encoder = ModelBuilder.build_encoder(
        arch=cfg.MODEL.arch_encoder,
        fc_dim=cfg.MODEL.fc_dim,
        weights=cfg.MODEL.weights_encoder)
    net_decoder = ModelBuilder.build_decoder(
        arch=cfg.MODEL.arch_decoder,
        fc_dim=cfg.MODEL.fc_dim,
        # num_class=cfg.DATASET.num_class,
        num_class=5,
        weights=cfg.MODEL.weights_decoder,
        use_softmax=True)

    crit = nn.NLLLoss(ignore_index=-1)

    segmentation_module = SegmentationModule(net_encoder, net_decoder, crit)

    # Dataset and Loader
    dataset_test = My_Test_Dataset(
        cfg.list_test,
        cfg.DATASET)
    # loader_test = torch.utils.data.DataLoader(
    #     dataset_test,
    #     # batch_size=cfg.TEST.batch_size,
    #     batch_size=8,
    #     shuffle=False,
    #     collate_fn=user_scattered_collate,
    #     num_workers=5,
    #     drop_last=True)

    segmentation_module.cuda()
    return segmentation_module,dataset_test


import re

if __name__ == '__main__':
    
    assert LooseVersion(torch.__version__) >= LooseVersion('0.4.0'), \
        'PyTorch>=0.4.0 is required'

    parser = argparse.ArgumentParser(
        description="PyTorch Semantic Segmentation Testing"
    )
    parser.add_argument(
        "--imgs",
        required=False,
        type=str,
        help="an image path, or a directory name",
        default="./self_data/JPEGImages/"
    )
    parser.add_argument(
        "--cfg",
        default="config/self_config.yaml",
        metavar="FILE",
        help="path to config file",
        type=str,
    )
    parser.add_argument(
        "--gpu",
        default=0,
        type=int,
        help="gpu id for evaluation"
    )
    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()

    cfg.merge_from_file(args.cfg)
    cfg.merge_from_list(args.opts)
    # cfg.freeze()

    logger = setup_logger(distributed_rank=0)   # TODO
    logger.info("Loaded configuration file {}".format(args.cfg))
    logger.info("Running with config:\n{}".format(cfg))

    cfg.MODEL.arch_encoder = cfg.MODEL.arch_encoder.lower()
    cfg.MODEL.arch_decoder = cfg.MODEL.arch_decoder.lower()

    # absolute paths of model weights
    cfg.MODEL.weights_encoder = os.path.join(
        cfg.DIR, 'encoder_' + cfg.TEST.checkpoint)
    cfg.MODEL.weights_decoder = os.path.join(
        cfg.DIR, 'decoder_' + cfg.TEST.checkpoint)

    assert os.path.exists(cfg.MODEL.weights_encoder) and \
        os.path.exists(cfg.MODEL.weights_decoder), "checkpoint does not exitst!"

    # generate testing image list
    if os.path.isdir(args.imgs):
        imgs = find_recursive(args.imgs)
        imgs.sort(key=lambda x:float("".join(re.findall("\d",x))))
    else:
        imgs = [args.imgs]
    assert len(imgs), "imgs should be a path to image (.jpg) or directory."
    cfg.list_test = [{'fpath_img': x} for x in imgs]

    if not os.path.isdir(cfg.TEST.result):
        os.makedirs(cfg.TEST.result)

    main(cfg, args.gpu)
