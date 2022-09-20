import os

# 删除预测为空的图片
def delete_empty_pred_img(exp_dir):
    txt_file = os.listdir(os.path.join(exp_dir, 'labels'))
    txt_file_name = [file.replace('.txt', '') for file in txt_file]
    img_file = os.listdir(exp_dir)
    for file in img_file:
        if file == 'labels':
            continue
        if file.replace('.jpg', '') not in txt_file_name:
            print(file)
            os.remove(os.path.join(exp_dir, file))
            print('remove success')


# 删除已经拦截的图片
def delete_has_intercept_img(exp_dir):
    txt_file = os.listdir('/home/mao/datasets/Diff模型对比/生产章比对/第二版模型拦截到的假章')
    txt_file_name = [file.replace('.jpg', '') for file in txt_file]
    img_file = os.listdir(exp_dir)
    for file in img_file:
        if file == 'labels':
            continue
        if file.replace('.jpg', '') in txt_file_name:
            print(file)
            os.remove(os.path.join(exp_dir, file))
            print('remove success')


exp_dir = '/home/mao/workspace/yolov5/runs/detect/exp29/'
delete_empty_pred_img(exp_dir)
# delete_has_intercept_img(exp_dir)