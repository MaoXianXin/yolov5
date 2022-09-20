#!/bin/bash

workdir=/home/mao/workspace/yolov5
# 模型路径
weights=/home/mao/workspace/yolov5/runs/train/exp14/weights/best.pt
# 待预测图片路径
# imgDir=/home/mao/datasets/测试样本/汇总-字符不同
# imgDir=/home/mao/datasets/inner_map_save_dir_4358
imgDir=/home/mao/datasets/inner_map_save_dir_46920
# imgDir=/home/mao/datasets/G7-合成样本-笔画偏移
# 阈值设置
confThres=0.05
# 文件夹名
expName=exp-conf-$confThres
expDir=/home/mao/workspace/yolov5/runs/detect/$expName

cd $workdir
rm -rf $expDir
sleep 5
python detect.py --weights $weights --source $imgDir --img 416 --conf-thres $confThres --device 0 --save-txt --name $expName --save-conf

cd /home/mao/workspace/PycharmProjects

python diff_area_utils.py --root_dirs $expDir --type 0
# for var in {"汉仪劲楷简.ttf",}
# do
#     python detect.py --weights /home/mao/workspace/yolov5/runs/train/20220826-1/weights/best.pt --source /home/mao/datasets/假章重合图-含分区域-158/all_inner_bmp_img --img 416 --conf-thres 0.3 --device 0 --save-txt --name exp-conf-0.3
# done