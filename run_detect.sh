#!/bin/bash

workdir=/home/mao/workspace/yolov5
# 模型路径
weights=/home/mao/workspace/yolov5/runs/train/20220919-序号1/weights/best.pt
onnx_weights=/home/mao/workspace/yolov5/runs/train/20220919-序号1/weights/best.onnx
ncnn_params=/home/mao/workspace/yolov5/runs/train/20220919-序号1/weights/tecrun_y5s6.param
ncnn_bin=/home/mao/workspace/yolov5/runs/train/20220919-序号1/weights/tecrun_y5s6.bin
ncnn_names=/home/mao/workspace/yolov5/runs/train/20220919-序号1/weights/tecrun_y5s6.names
# 待预测图片路径
# imgDir=/home/mao/datasets/测试样本/汇总-字符不同
imgDir=/home/mao/datasets/inner_map_save_dir_4358
# imgDir=/home/mao/datasets/inner_map_save_dir_46920
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
python export.py --data data/diff-char.yaml --weights $weights --batch-size 1 --device 0 --train --simplify --include onnx

cd /home/mao/workspace/SVN-219/TC_NCNN/trunk/src
./build-all.sh -n yes -d so -t no

cd /home/mao/workspace/SVN-219/TC_NCNN/trunk/src/ncnn/build-host-gcc-linux/tools/onnx
./onnx2ncnn $onnx_weights $ncnn_params $ncnn_bin
cp $ncnn_params $ncnn_bin $ncnn_names /home/mao/workspace/SVN-219/TC_NCNN/trunk/src/test_dir/config/mod

cd /home/mao/workspace/PycharmProjects
python diff_area_utils.py --root_dirs $expDir --type 0

cd /home/mao/workspace/yolov5/utils
python box_analysis.py

# cd /home/mao/workspace/SVN-219/TC_NCNN/trunk/src/test_dir
# ./t1 ./config/mod $imgDir f 4 0.1 ./$expName
# for var in {"汉仪劲楷简.ttf",}
# do
#     python detect.py --weights /home/mao/workspace/yolov5/runs/train/20220826-1/weights/best.pt --source /home/mao/datasets/假章重合图-含分区域-158/all_inner_bmp_img --img 416 --conf-thres 0.3 --device 0 --save-txt --name exp-conf-0.3
# done