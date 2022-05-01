import yaml
import os
import shutil

root_dir = '../datasets/coco'
train = '../datasets/coco/train2017.txt'
# val = '../datasets/coco/val2017.txt'
# test = '../datasets/coco/test-dev2017.txt'

select_classes = ['person',]
categories = []
label2id = {}
id2label = {}
with open("./data/coco.yaml", 'r') as stream:
    try:
        parsed_yaml=yaml.safe_load(stream)
        categories = parsed_yaml['names']
    except yaml.YAMLError as exc:
        print(exc)

for name in categories:
    label2id[name] = categories.index(name)
    id2label[categories.index(name)] = name

with open(train) as f:
    lines = f.readlines()
    lines = [(root_dir + line.strip().replace('.jpg', '.txt')[1:]).replace('images', 'labels') for line in lines]
# lines = lines[:2500]
lines = sorted(lines)

id_count_dict = {}
for cls_name in select_classes:
    id_count_dict[cls_name] = 0
for line in lines:
    if not os.path.exists(line):
        continue
    preserve_line = []
    with open(line) as f:
        object_lines = f.readlines()
        for object in object_lines:
            if id2label[int(object.split(' ')[0])] in select_classes:
                preserve_line.append(object)
                id_count_dict[id2label[int(object.split(' ')[0])]] += 1
    if len(preserve_line) == 0:
        continue
    save_file = line.replace('datasets', 'transform_datasets')
    if not os.path.exists('/'.join(save_file.split('/')[0:-1])):
        os.makedirs('/'.join(save_file.split('/')[0:-1]))
    with open(save_file, 'w') as f:
        for preserve in preserve_line:
            f.write(preserve)


img_names = os.listdir('/'.join(save_file.split('/')[0:-1]))
img_paths = [root_dir + '/images/train2017/' + img.replace('.txt', '.jpg') for img in img_names]


if not os.path.exists('/'.join(save_file.split('/')[0:-1]).replace('labels', 'images')):
    os.makedirs('/'.join(save_file.split('/')[0:-1]).replace('labels', 'images'))
for source in img_paths:
    shutil.copyfile(source, source.replace('datasets', 'transform_datasets'))
id_count_dict = sorted(id_count_dict.items(), key=lambda item: item[1], reverse=True)
print(id_count_dict)
print(1)