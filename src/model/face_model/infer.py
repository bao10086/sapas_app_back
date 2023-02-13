import os
import time

import cv2
import numpy as np
import torch
from PIL import ImageDraw, ImageFont, Image  # 图像处理模块

from src.model.face_model.detection.face_detect import MTCNN

# from src.model.face_model.utils.utils import add_arguments, print_arguments
threshold = 0.6
mobilefacenet_model_path = 'save_model/mobilefacenet.pth'
mtcnn_model_path = 'save_model/mtcnn'


# parser = argparse.ArgumentParser(description=__doc__)
# add_arg = functools.partial(add_arguments, argparser=parser)
# add_arg('image_path', str, 'dataset/test.jpg', '预测图片文件夹路径')
# add_arg('face_db_path', str, 'face_db', '人脸库路径')
# add_arg('threshold', float, 0.6, '判断相识度的阈值')
# add_arg('mobilefacenet_model_path', str, 'save_model/mobilefacenet.pth',
#         'MobileFaceNet预测模型的路径')  # mobilefacenet人脸识别
# add_arg('mtcnn_model_path', str, 'save_model/mtcnn', 'MTCNN预测模型的路径')  # MTCNN用来获取人脸边界框和人脸特征点的位置
# args = parser.parse_args()
# print_arguments(args)


# threshold
class Predictor:
    def __init__(self, mtcnn_model_path, mobilefacenet_model_path, face_db_path, threshold=0.7):
        # 加载人脸检测模型
        self.threshold = threshold
        self.mtcnn = MTCNN(model_path=mtcnn_model_path)
        self.device = torch.device("cpu")

        # 加载人脸识别模型
        self.model = torch.jit.load(mobilefacenet_model_path, )
        self.model.to(self.device)
        self.model.eval()

        self.faces_db = self.load_face_db(face_db_path)

    def load_face_db(self, face_db_path):
        faces_db = {}
        for path in os.listdir(face_db_path):
            name = os.path.basename(path).split('.')[0]  # 得到图片名称
            image_path = os.path.join(face_db_path, path)  # 得到图片路径
            # decode从网络流中回复图像 encode压缩数据 方便传播
            img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
            # MTCNN的返回
            imgs, _ = self.mtcnn.infer_image(img)
            if imgs is None or len(imgs) > 1:
                print('人脸库中的 %s 图片包含不是1张人脸，自动跳过该图片' % image_path)
                continue

            imgs = self.process(imgs)
            feature = self.infer(imgs[0])
            faces_db[name] = feature[0][0]
        return faces_db

    @staticmethod
    # 将图片转换格式 归一化
    def process(imgs):
        imgs1 = []
        for img in imgs:
            img = img.transpose((2, 0, 1))
            img = (img - 127.5) / 127.5
            imgs1.append(img)
        return imgs1

    # 预测图片
    def infer(self, imgs):
        assert len(imgs.shape) == 3 or len(imgs.shape) == 4
        if len(imgs.shape) == 3:
            imgs = imgs[np.newaxis, :]
        # TODO 不知为何不支持多张图片预测
        '''
        imgs = torch.tensor(imgs, dtype=torch.float32, device=self.device)
        features = self.model(img)
        features = features.detach().cpu().numpy()
        '''
        features = []
        for i in range(imgs.shape[0]):
            img = imgs[i][np.newaxis, :]
            img = torch.tensor(img, dtype=torch.float32, device=self.device)
            # 执行预测
            feature = self.model(img)
            feature = feature.detach().cpu().numpy()
            features.append(feature)
        return features

    def recognition(self, image_path):
        img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
        s = time.time()
        imgs, boxes = self.mtcnn.infer_image(img)
        print('人脸检测时间：%dms' % int((time.time() - s) * 1000))
        if imgs is None:
            return None, None
        imgs = self.process(imgs)
        imgs = np.array(imgs, dtype='float32')
        s = time.time()
        features = self.infer(imgs)
        print('人脸识别时间：%dms' % int((time.time() - s) * 1000))
        names = []
        probs = []
        for i in range(len(features)):
            feature = features[i][0]
            results_dict = {}
            for name in self.faces_db.keys():
                feature1 = self.faces_db[name]
                prob = np.dot(feature, feature1) / (np.linalg.norm(feature) * np.linalg.norm(feature1))
                results_dict[name] = prob
            results = sorted(results_dict.items(), key=lambda d: d[1], reverse=True)
            print('人脸对比结果：', results)
            result = results[0]
            prob = float(result[1])
            probs.append(prob)
            if prob > self.threshold:
                name = result[0]
                names.append(name)
            else:
                names.append('unknow')
        return boxes, names

    def add_text(self, img, text, left, top, color=(0, 0, 0), size=20):
        if isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('simfang.ttf', size)
        draw.text((left, top), text, color, font=font)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 画出人脸框和关键点
    def draw_face(self, image_path, boxes_c, names):
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
        if boxes_c is not None:
            for i in range(boxes_c.shape[0]):
                bbox = boxes_c[i, :4]
                name = names[i]
                corpbbox = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
                # 画人脸框
                cv2.rectangle(img, (corpbbox[0], corpbbox[1]),
                              (corpbbox[2], corpbbox[3]), (255, 0, 0), 1)
                # 判别为人脸的名字
                # print("starting")
                img = self.add_text(img, name, corpbbox[0], corpbbox[1] - 15, color=(0, 0, 255), size=12)
        cv2.imshow("result", img)
        cv2.waitKey(0)


def infer(phone, path):
    start = time.time()
    # "./src/model/face_model/face_db/" 是服务器上的地址
    face_db_path_new = "./src/model/face_model/face_db/" + phone
    # face_db_path_new = 'face_db'

    predictor = Predictor(mtcnn_model_path, mobilefacenet_model_path, face_db_path_new,
                          threshold=threshold)
    boxes, names = predictor.recognition(path)
    if names is None:
        return False
    print('预测的人脸位置：', boxes.astype(np.int_).tolist())
    print('识别的人脸名称：', names[0])
    print('总识别时间：%dms' % int((time.time() - start) * 1000))
    # predictor.draw_face(args.image_path, boxes, names)
    for name in names:
        if name != "unknow":
            return True
    return False


if __name__ == '__main__':
    infer()
