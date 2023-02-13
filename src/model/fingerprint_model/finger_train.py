import argparse
import os

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from src.model.fingerprint_model.finger_model import finger_class

# 待传入参数
# 决定模型保存路径
# user_id=0
# 训练数据路径
# data_set=""
# 类别数
# class_num=0


# 依据设备选择执行
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

device = "cpu"


# 参数设置
def parse_opt():
    parser = argparse.ArgumentParser()

    # parser.add_argument("--img-dir",type=str,default="./data",help="train image path") #数据集的路径
    parser.add_argument("--imgsz", type=int, default=224, help="image size")  # 图像尺寸
    parser.add_argument("--epochs", type=int, default=5, help="train epochs")  # 训练批次
    parser.add_argument("--batch-size", type=int, default=4, help="train batch-size")  # batch-size
    parser.add_argument("--class_num", type=int, default=1, help="class num")  # 类别数
    parser.add_argument("--lr", type=float, default=0.001, help="Init lr")  # 学习率初始值
    parser.add_argument("--m", type=float, default=0.9, help="optimer momentum")  # 动量
    parser.add_argument("--save-dir", type=str,
                        default="D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/src/model/fingerprint_model/models/fingermodel/",
                        help="save models dir")  # 保存模型路径
    opt = parser.parse_known_args()[0]
    return opt


# 训练finger模型
class Finger_Train():
    def __init__(self, opt, user_id, img_dir, class_cnt):
        # 用户id
        self.user_id = user_id
        # 参数设置
        self.epochs = opt.epochs
        self.batch_size = opt.batch_size
        self.class_num = opt.class_num
        self.imgsz = opt.imgsz
        # 图片路径
        self.img_dir = img_dir
        # 预测时使用模型路径
        self.save_dir = opt.save_dir
        # 学习率
        self.lr = opt.lr
        # momentum
        self.moment = opt.m
        # 导入网络结构
        self.model = finger_class(nclass=self.class_num)
        # loss
        self.cross = nn.CrossEntropyLoss()
        # 优化器
        self.optimzer = optim.SGD((self.model.parameters()), lr=self.lr, momentum=self.moment, weight_decay=0.0004)

        # 训练集、验证集、类别
        self.trainx, self.valx, self.category = self.process()
        print("监测到类别： %s  " % str(self.category))

    def __call__(self):
        best_acc = 0
        self.model.train(True)

        # 开始训练
        for epoch in range(self.epochs):
            optimzer1 = self.lrfn(epoch, self.optimzer)

            print("------------正在进行第 %d 个epoch------------" % (epoch + 1))
            # 开始训练
            # 该轮epoch内的loss,acc,correct_cnt
            epoch_loss = 0.0  # 损失
            epoch_num = 0.0  # 训练的个数
            correct_cnt = 0.0  # 分类正确的个数

            for i, data in enumerate(self.trainx):
                # 导入数据
                inputs, label = data

                inputs, label = inputs.to(device), label.to(device)

                # 训练
                optimzer1.zero_grad()
                output = self.model(inputs)
                loss = self.cross(output, label)
                loss.backward()
                optimzer1.step()
                epoch_loss += loss.item()  # 损失累加
                values, pred = torch.max(output.data, 1)
                # predict = torch.softmax(output.data, dim=1)
                # print(predict)
                # print("label.data")
                # print(label.data)
                # print("pred")
                # print(pred)
                epoch_num += label.size(0)  # 求总共的训练个数
                correct_cnt += pred.eq(label.data).sum()  # 截止当前预测正确的个数

            train_acc = correct_cnt / epoch_num
            print('Epoch:{} | Loss:{} | Acc:{}'.format(epoch + 1, epoch_loss / len(self.trainx), train_acc))

            print("----------测试集正在进行第 {} 个epoch----------".format(epoch + 1))
            with torch.no_grad():
                correct_num = 0.
                total = 0.
                for inputs, labels in self.valx:
                    inputs, labels = inputs.to(device), labels.to(device)

                    outputs = self.model(inputs)
                    _, pred = torch.max(outputs.data, 1)
                    # +print(pred)
                    total += labels.size(0)
                    correct_num += pred.eq(labels).sum()
                test_acc = correct_num / total
                print("批次%d的验证集准确率" % (epoch + 1), test_acc)
                if best_acc < test_acc:
                    best_acc = test_acc
                    # start_time=(time.strftime("%m%d",time.localtime()))
                    save_weight = self.save_dir + os.sep + self.user_id
                    os.makedirs(save_weight, exist_ok=True)
                    torch.save(self.model.state_dict(), save_weight + os.sep + "best.pth")

    # 数据处理
    def process(self):
        # 数据增强
        data_transforms = {
            'train': transforms.Compose([
                transforms.Resize((self.imgsz, self.imgsz)),
                transforms.CenterCrop((self.imgsz, self.imgsz)),
                transforms.RandomHorizontalFlip(p=0.2),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ]),
            "val": transforms.Compose([
                transforms.Resize((self.imgsz, self.imgsz)),
                transforms.CenterCrop((self.imgsz, self.imgsz)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
        }

        # 定义图像生成器
        image_datasets = {x: datasets.ImageFolder(os.path.join(self.img_dir, x), data_transforms[x]) for x in
                          ['train', 'val']}
        # 载入训练集和验证集
        trainx = DataLoader(image_datasets["train"], batch_size=self.batch_size, shuffle=True, drop_last=True)
        valx = DataLoader(image_datasets["val"], batch_size=self.batch_size, shuffle=True, drop_last=True)
        # testx=DataLoader(image_datasets["test"], batch_size=1, shuffle=False, drop_last=False)
        category = image_datasets["train"].class_to_idx
        return trainx, valx, category

    # 学习率设置
    def lrfn(self, num_epoch, optimzer):
        lr_start = 0.00001
        max_lr = 0.0004
        lr_up_epoch = 10
        lr_sustain_epoch = 5
        lr_exp = .8
        if num_epoch < lr_up_epoch:
            lr = (max_lr - lr_start) / lr_up_epoch * num_epoch + lr_start
        elif num_epoch < lr_up_epoch + lr_sustain_epoch:
            lr = max_lr
        else:
            lr = (max_lr - lr_start) * lr_exp ** (num_epoch - lr_up_epoch - lr_sustain_epoch) + lr_start
        for param_group in optimzer.param_groups:
            param_group['lr'] = lr
        return optimzer


def finger_train_main(user_phone, img_dir, class_cnt=1):
    opt = parse_opt()
    models = Finger_Train(opt, user_id=user_phone, img_dir=img_dir, class_cnt=class_cnt)
    models()
