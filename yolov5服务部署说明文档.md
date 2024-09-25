首先通过nvcr.io/nvidia/pytorch:23.03-py3-v2镜像进行pt格式模型到engine格式模型的转换
启动镜像命令如下:

```
第一步需要先cd到yolov5工程目录下，然后再运行下面的命令
docker run --gpus all --shm-size=16g --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --name tensorrt-convert -it -v $PWD:$PWD -w $PWD nvcr.io/nvidia/pytorch:23.03-py3-v2 /bin/bash

# MRZ，训练好的模型文件存储在runs/train/exp6/weights/best.pt
# 运行下面的命令进行engine格式模型导出，在不同机器上，特别是显卡不一样的情况需要重复这一步操作
python export.py --weights runs/train/exp6/weights/best.pt --data data/MRZ.yaml --include engine --batch-size 1

拷贝best.engine到model_repository:
mv runs/train/exp6/weights/best.engine ./model_repository/yolov5_mrz/1/model.plan

# Type_CountryCode_Sex，同理
python export.py --weights runs/train/exp15/weights/best.pt --data data/vis_type.yaml --include engine --batch-size 1

拷贝best.engine到model_repository:
mv runs/train/exp15/weights/best.engine ./model_repository/yolov5_type_sex_code/1/model.plan
```

model_repository仓库相关说明:
```
模型仓库结构如下所示:
./
├── yolov5_mrz
│   ├── 1
│   │   └── model.plan
│   └── config.pbtxt
└── yolov5_type_sex_code
    ├── 1
    │   └── model.plan
    └── config.pbtxt
其中plan文件是由engine格式模型重命名得到
config.pbtxt示例如下:
name: "yolov5_mrz"
platform: "tensorrt_plan"
max_batch_size: 1
input [
  {
    name: "input"
    data_type: TYPE_FP32
    dims: [ 3, 640, 640 ]
  }
]
output [
  {
    name: "output"
    data_type: TYPE_FP32
    dims: [ 25200, 7 ]
  }
]
```

转换好模型之后启动nvcr.io/nvidia/tritonserver:23.03-py3镜像进行部署
```
# --model-repository要使用绝对路径
docker run -d --gpus all --shm-size=16g --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --name tritonserver -p18220:8000 -p18221:8001 -p18222:8002 -v $PWD:$PWD nvcr.io/nvidia/tritonserver:23.03-py3 tritonserver --model-repository=/home/mao/workspace/train_yolov5/yolov5/model_repository
```

多张显卡情况下如何指定使用某一张:

```
--gpus '"device=0,1"'用于指定容器仅使用GPU 0和GPU 1
如果只想使用单个GPU，比如GPU 0，那么可以将其修改为--gpus '"device=0"'
```

部署好服务后进行请求测试:

```
客户端client.py文件位置: tensorrt-triton-yolov5/triton-deploy/clients/python/
运行client.py示例命令:
python client.py image 测试tensorrt/ --out /home/nja/mao/workspace/tensorrt-triton-yolov5/triton-deploy/clients/python/predict --url 127.0.0.1:18221 --model yolov5_type_sex_code --confidence 0.7 --nms 0.6
```

