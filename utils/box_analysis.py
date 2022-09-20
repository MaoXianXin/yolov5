import os
import shutil
import cv2
import numpy as np
from pandas import DataFrame

def get_file_paths(root_dirs):
        '''
            可以传入多个源文件夹, 获取所有的文件path
            root_dirs格式如下: ['/home/mao/Downloads/票证/1-背景_barcode_各种背景图像-17322张/各种背景图像-17322张']
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

class BoxStatistics:
    def __init__(self, im, source):
        self.im = im
        # self.cnt = {0.1:0, 0.2:0, 0.3:0, 0.4:0, 0.5:0, 0.6:0, 0.7:0, 0.8:0, 0.9:0}
        self.cnt = {'threshold': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], 'num': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'percent': [0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.source = source
        self.num_img = len(filter_by_keyword(['.bmp'], get_file_paths([self.source])))

    # 统计检测框内为黑色字体，不可解释的样本
    def calc_black_font_box_samples(self, xyxy, save_path):
        save_dir = '/'.join(save_path.split('/')[:-1])
        print(save_dir)
        save_name = save_path.split('/')[-1]
        print(save_name)
        if not os.path.exists(os.path.join(save_dir, 'black_samples')):
            os.makedirs(os.path.join(save_dir, 'black_samples'), exist_ok=True)
        box = xyxy
        p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
        # cv2.imshow('im0.bmp', im0)
        # cv2.waitKey(0)
        black_cnt = 0
        red_cnt = 0
        green_cnt = 0
        img_blank = np.zeros(self.im.shape, np.uint8)
        for row in range(p1[1], p2[1]):
            for col in range(p1[0], p2[0]):
                if self.im[row, col, 0] == 0 and self.im[row, col, 1] == 0 and self.im[row, col, 2] == 0:
                    black_cnt += 1
                    # red_cnt += 1
                    # green_cnt += 1
                    img_blank[row, col] = [0, 0, 0]
                elif self.im[row, col, 0] == 0 and self.im[row, col, 1] == 0 and self.im[row, col, 2] == 255:
                    red_cnt += 1
                    img_blank[row, col] = [0, 0, 255]
                elif self.im[row, col, 0] == 0 and self.im[row, col, 1] == 255 and self.im[row, col, 2] == 0:
                    green_cnt += 1
                    img_blank[row, col] = [0, 255, 0]
                else:
                    img_blank[row, col] = [200, 200, 200]
        print(black_cnt, red_cnt, green_cnt)
        if black_cnt == 0:
            return
        red_ratio = red_cnt * 1.0 / black_cnt
        green_ratio = green_cnt * 1.0 / black_cnt
        # 如果红色、绿色占比低，说明盖的比较好，属于不可解释的虚警
        if red_ratio < 0.2 and green_ratio < 0.2:
            cv2.rectangle(self.im, p1, p2, (0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
            cv2.imwrite(os.path.join(os.path.join(save_dir, 'black_samples'), save_name), self.im)
        print(red_cnt * 1.0 / black_cnt, green_cnt * 1.0 / black_cnt)
        print(black_cnt * 1.0 / red_cnt, black_cnt * 1.0 / green_cnt)
        # cv2.imshow('img_blank.bmp', img_blank)
        # cv2.waitKey(0)


    # 统计检测框内为红多字体，不可解释的样本
    def calc_red_font_box_samples(self, xyxy, save_path):
        save_dir = '/'.join(save_path.split('/')[:-1])
        print(save_dir)
        save_name = save_path.split('/')[-1]
        print(save_name)
        if not os.path.exists(os.path.join(save_dir, 'red_samples')):
            os.makedirs(os.path.join(save_dir, 'red_samples'), exist_ok=True)
        box = xyxy
        p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
        # cv2.imshow('im0.bmp', im0)
        # cv2.waitKey(0)
        black_cnt = 0
        red_cnt = 0
        green_cnt = 0
        img_blank = np.zeros(self.im.shape, np.uint8)
        for row in range(p1[1], p2[1]):
            for col in range(p1[0], p2[0]):
                if self.im[row, col, 0] == 0 and self.im[row, col, 1] == 0 and self.im[row, col, 2] == 0:
                    black_cnt += 1
                    # red_cnt += 1
                    # green_cnt += 1
                    img_blank[row, col] = [0, 0, 0]
                elif self.im[row, col, 0] == 0 and self.im[row, col, 1] == 0 and self.im[row, col, 2] == 255:
                    red_cnt += 1
                    img_blank[row, col] = [0, 0, 255]
                elif self.im[row, col, 0] == 0 and self.im[row, col, 1] == 255 and self.im[row, col, 2] == 0:
                    green_cnt += 1
                    img_blank[row, col] = [0, 255, 0]
                else:
                    img_blank[row, col] = [200, 200, 200]
        print(black_cnt, red_cnt, green_cnt)
        red_ratio = red_cnt * 1.0 / (black_cnt + red_cnt + green_cnt)
        green_ratio = green_cnt * 1.0 / (black_cnt + red_cnt + green_cnt)
        # 如果红色、绿色占比低，说明盖的比较好，属于不可解释的虚警
        if red_ratio > 0.5 and green_ratio < 0.2:
            cv2.rectangle(self.im, p1, p2, (0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
            cv2.imwrite(os.path.join(os.path.join(save_dir, 'red_samples'), save_name), self.im)
        # cv2.imshow('img_blank.bmp', img_blank)
        # cv2.waitKey(0)
    
    # 设置不同阈值，并保存到对应的文件夹
    def calc_num_by_threshold(self, xyxy, conf, save_path):
        save_dir = '/'.join(save_path.split('/')[:-1])
        # print(save_dir)
        save_name = save_path.split('/')[-1]
        # print(save_name)
        for key in self.cnt['threshold']:
            if conf > key:
                if not os.path.exists(os.path.join(save_dir, str(key))):
                    os.makedirs(os.path.join(save_dir, str(key)), exist_ok=True)
                box = xyxy
                p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
                cv2.rectangle(self.im, p1, p2, (0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
                cv2.imwrite(os.path.join(os.path.join(save_dir, str(key)), save_name), self.im)


    # 获取某个阈值区间内的预测结果
    def calc_num_by_threshold_between_two(self, xyxy, conf, save_path):
        save_dir = '/'.join(save_path.split('/')[:-1])
        # print(save_dir)
        save_name = save_path.split('/')[-1]
        # print(save_name)
        for i in range(len(self.cnt['threshold']) - 1):
            if conf > self.cnt['threshold'][i] and conf < self.cnt['threshold'][i+1]:
                if not os.path.exists(os.path.join(save_dir, str(self.cnt['threshold'][i]))):
                    os.makedirs(os.path.join(save_dir, str(self.cnt['threshold'][i])), exist_ok=True)
                box = xyxy
                p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
                cv2.rectangle(self.im, p1, p2, (0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
                cv2.imwrite(os.path.join(os.path.join(save_dir, str(self.cnt['threshold'][i])), save_name), self.im)
    
    
    # 获取不同阈值下预测结果数，并以字典形式返回
    def get_threshold_predict_num(self, save_path):
        save_dir = '/'.join(save_path.split('/')[:-1])
        # print(save_dir)
        for index in range(len(self.cnt['num'])):
            self.cnt['num'][index] = len(os.listdir(os.path.join(save_dir, str(self.cnt['threshold'][index]))))
            self.cnt['percent'][index] = self.cnt['num'][index] * 1.0 / self.num_img * 100
        print(self.cnt)
        print(self.num_img)
        data = DataFrame(self.cnt)  # 将字典转换成为数据框
        data.to_csv('cnt.csv', index=False)

    
# 解析预测结果的txt文件，获取每个阈值区间的预测结果数
def parse_predict_txt(root_dir, samples_cnt):
    all_file_paths = get_file_paths(root_dir)
    all_txt_paths = filter_by_keyword(['.txt'], all_file_paths)
    for i in range(len(samples_cnt['threshold'])):
        folder = '/'.join(all_file_paths[0].split('/')[:-1])
        if not os.path.exists(os.path.join(folder, str(samples_cnt['threshold'][i]))):
            os.makedirs(os.path.join(folder, str(samples_cnt['threshold'][i])), exist_ok=True)
        for txt_path in all_txt_paths:
            # print(txt_path)
            with open(txt_path, 'r') as f:
                lines = f.readlines()
                lines = [line.strip() for line in lines]
            
            for line in lines:
                confidence = line.split(' ')[-1]
                if float(confidence) >= samples_cnt['threshold'][i]:
                    samples_cnt['num'][i] += 1
                    shutil.copy(txt_path, os.path.join(folder, str(samples_cnt['threshold'][i])))
                    shutil.copy(txt_path.replace('labels/', '').replace('.txt', '.bmp'), os.path.join(folder, str(samples_cnt['threshold'][i])))
                    break


if __name__ == '__main__':
    root_dir = ['/home/mao/workspace/yolov5/runs/detect/exp-conf-0.05']
    samples_cnt = {'threshold': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], 'num': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'percent': [0, 0, 0, 0, 0, 0, 0, 0, 0]}
    parse_predict_txt(root_dir, samples_cnt)
    for i in range(len(samples_cnt['threshold'])):
        samples_cnt['percent'][i] = samples_cnt['num'][i] * 1.0 / 46920 * 100
    print(samples_cnt)
    data = DataFrame(samples_cnt)  # 将字典转换成为数据框
    data.to_csv('cnt.csv', index=False)
