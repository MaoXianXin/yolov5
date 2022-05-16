import json
import glob
import os.path as osp
import os
from tqdm import tqdm
import shutil

def convert_bbox_coco2yolo(img_width, img_height, bbox):
    """
    Convert bounding box from COCO format to YOLO format

    Parameters
    ----------
    img_width : int
        width of image
    img_height : int
        height of image
    bbox : list[int]
        bounding box annotation in COCO format: 
        [top left x position, top left y position, width, height]

    Returns
    -------
    list[float]
        bounding box annotation in YOLO format: 
        [x_center_rel, y_center_rel, width_rel, height_rel]
    """
    
    # YOLO bounding box format: [x_center, y_center, width, height]
    # (float values relative to width and height of image)
    x_tl, y_tl, w, h = bbox

    dw = 1.0 / img_width
    dh = 1.0 / img_height

    x_center = x_tl + w / 2.0
    y_center = y_tl + h / 2.0

    x = x_center * dw
    y = y_center * dh
    w = w * dw
    h = h * dh

    return [x, y, w, h]



def make_folders(path="output"):
    # if os.path.exists(path):
    #     shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    return path


def convert_coco_json_to_yolo_txt(output_path, json_file, anno_txt_files):
    path = make_folders(output_path)

    with open(json_file) as f:
        json_data = json.load(f)

    
    for image in tqdm(json_data["images"], desc="Annotation txt for each iamge"):
        img_id = image["id"]
        img_name = image["file_name"]
        img_width = image["width"]
        img_height = image["height"]

        anno_in_image = [anno for anno in json_data["annotations"] if anno["image_id"] == img_id]
        anno_txt = os.path.join(output_path, img_name.split('/')[-1].split(".")[0] + ".txt")
        with open(anno_txt, "w") as f:
            for anno in anno_in_image:
                category = anno["category_id"]
                if category != 0:
                    continue
                bbox_COCO = anno["bbox"]
                if anno_txt not in anno_txt_files:
                    anno_txt_files.append(anno_txt)
                x, y, w, h = convert_bbox_coco2yolo(img_width, img_height, bbox_COCO)
                f.write(f"{category} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

    print("Converting COCO Json to YOLO txt finished!")


anno_txt_files = []
for result_json in glob.glob(osp.join('/home/mao/disk/Diff标注数据集', '*/*.json')):
    print(result_json)
    convert_coco_json_to_yolo_txt("/home/mao/disk/Diff标注数据集/labels", result_json, anno_txt_files)

print(anno_txt_files)

os.makedirs('/home/mao/disk/Diff标注数据集/labels-1', exist_ok=True)
for anno_txt in anno_txt_files:
    shutil.copy(anno_txt, '/home/mao/disk/Diff标注数据集/labels-1/'+anno_txt.split('/')[-1])

os.makedirs('/home/mao/disk/Diff标注数据集/images-1', exist_ok=True)
for anno_txt in anno_txt_files:
    shutil.copy('/home/mao/disk/Diff标注数据集/images/'+anno_txt.split('/')[-1].replace('.txt', '.jpg'), '/home/mao/disk/Diff标注数据集/images-1/'+anno_txt.split('/')[-1].replace('.txt', '.jpg'))