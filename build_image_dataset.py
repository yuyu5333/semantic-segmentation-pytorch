from matplotlib.font_manager import json_dump
import torch
from PIL import Image
import glob
import json


file_infos = []
base_path = "./self_data/JPEGImages/"
with open("./self_data/ImageSets/val.txt","r") as f:
    for line in f.readlines():
        file_name = str(line).replace("\n","")
        full_name = base_path+file_name+".jpg"
        img = Image.open(full_name)
        file_info = {}
        file_info["height"] = img.height
        file_info["width"] = img.width
        file_info["fpath_img"] = full_name
        file_info["fpath_segm"] = full_name.replace("JPEGImages","SegmentationClass").replace(".jpg",".png")
        file_infos.append (file_info)
        
file_infos = json_dump(file_infos,"./self_data/ImageSets/val_infos.json")

    
    
