# coding:UTF-8
from os import pread
import torch
import cv2


import sys
sys.path.append('./rddc2020/yolov5')
from rddc2020.yolov5.utils.datasets import *
from rddc2020.yolov5.utils.general import *


class Detector():
    def __init__(
            self,
            weight_path='/Users/bytedance/Documents/JiangnaProject/rddc2020/yolov5/weights/IMSC/last_100_100_640_16.pt',
            img_size=640):
        self.model = torch.load(weight_path)['model'].float().fuse().eval()
        self.img_size = img_size

    def infer(self, path):
        img = cv2.imread(path)
        assert img is not None, 'Image Not Found ' + path

        h, w, _ = img.shape
        # Padded resize
        img = letterbox(img, new_shape=self.img_size)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).float()
        img /= 255.0
        img = img.unsqueeze(0)
        pred = self.model(img)[0]
        pred = non_max_suppression(pred, 0.22, 0.99, agnostic=True)
        try:
            pred = pred[0].numpy()  # (x1, y1, x2, y2, conf, cls)
        except:
            pred = np.asarray([])
        return pred, h, w


if __name__ == '__main__':
    weight_path = '/Users/bytedance/Documents/JiangnaProject/rddc2020/yolov5/weights/IMSC/last_100_100_640_16.pt'
    img_size = 640
    detector = Detector(weight_path, img_size)
    print(detector.infer('/Users/bytedance/Downloads/道路病害/2018年检测数据/G303B-0039+743062-0006+251373.jpg'))
