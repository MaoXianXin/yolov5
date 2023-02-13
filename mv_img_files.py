import json
import glob
import os.path as osp
import os
from tqdm import tqdm
import shutil

# def make_folders(path="output"):
#     # if os.path.exists(path):
#     #     shutil.rmtree(path)
#     os.makedirs(path, exist_ok=True)
#     return path
#
# img_paths = glob.glob(osp.join('/home/mao/disk/Diff标注数据集', '*/*/*.bmp'))
# for img in img_paths:
#     shutil.copy(img, '/home/mao/disk/Diff标注数据集/images/'+img.split('/')[-1])

def get_file_paths(root_dirs):
    '''
        可以传入多个源文件夹, 获取所有的文件path
        root_dirs格式如下: ['/home/mao/Downloads/票证/1-背景_barcode_各种背景图像-17322张/各种背景图像-17322张',]
    '''
    img_paths_list = []
    for root_dir in root_dirs:
        for fpathe, dirs, fs in os.walk(root_dir):
            for f in fs:
                img_paths_list.append(os.path.join(fpathe, f))
    return img_paths_list


def filter_by_keyword(keyword_list, all_file):
    '''
        可以传入多个关键词用于过滤
        keyword_list格式如下: ['.jpg', '.bmp']
        all_file是一个列表, 里面的元素是文件路径
    '''
    filterd_file_list = []
    for keyword in keyword_list:
        for file in all_file:
            if keyword in file:
                filterd_file_list.append(file)
    return filterd_file_list


all_file_paths = get_file_paths(['/home/mao/datasets/OK'])
all_bmp_file_paths = filter_by_keyword(['inner'], all_file_paths)

for path in all_bmp_file_paths:
    shutil.copy(path, "/home/mao/datasets/inner_img_bmp")
print(1111)