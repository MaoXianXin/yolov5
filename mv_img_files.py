import json
import glob
import os.path as osp
import os
from tqdm import tqdm
import shutil

def make_folders(path="output"):
    # if os.path.exists(path):
    #     shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    return path

img_paths = glob.glob(osp.join('/home/mao/disk/Diff标注数据集', '*/*/*.bmp'))
for img in img_paths:
    shutil.copy(img, '/home/mao/disk/Diff标注数据集/images/'+img.split('/')[-1])