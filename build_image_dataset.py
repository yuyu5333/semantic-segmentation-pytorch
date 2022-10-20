from matplotlib.font_manager import json_dump
import torch
from PIL import Image
import glob
import json


file_infos = {}
base_path = "./self_data/JPEGImages/"
with open("./self_data/ImageSets/train.txt","r") as f:
    file_name = str(f.readline()).replace("\n","")
    full_name = base_path+file_name+".jpg"
    img = Image.open(full_name)
    file_info = {}
    file_info["height"] = img.height
    file_info["width"] = img.width
    file_info["fpath_img"] = full_name
    file_info["fpath_segm"] = full_name.replace("JPEGImages","SegmentationClass")
    file_infos[file_name] = file_info
# file_infos = json_dump(file_infos)
with open("./self_data/ImageSets/train_infos.json","w") as f:
    f.write(file_infos)
    
    
