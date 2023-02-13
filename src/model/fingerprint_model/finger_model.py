import math

import numpy as np
import torch.nn as nn


# 对外接口
def finger_class(nclass):
    model = Finger_Model(width_mult=1, n_class=nclass)
    return model


# 参数：
# 输入维度、输出维度、步幅
# 输出：
# 返回一个块
def conv_bn(input, output, stride):
    return nn.Sequential(
        nn.Conv2d(input, output, 3, stride, 1, bias=False),
        nn.BatchNorm2d(output),
        nn.ReLU6(inplace=True)
    )


# 1*1小卷积核
def conv_1x1_bn(input, output):
    return nn.Sequential(
        nn.Conv2d(input, output, 1, 1, 0, bias=False),
        nn.BatchNorm2d(output),
        nn.ReLU6(inplace=True)
    )


# 取整
def make_divisible(x, divisible_by=8):
    return int(np.ceil(x * 1. / divisible_by) * divisible_by)


# 倒置残差结构
# 主要参考mobilenet的倒置残差思想
class Inverted_Residual(nn.Module):
    def __init__(self, input, output, stride, expand_ratio):
        super(Inverted_Residual, self).__init__()
        self.stride = stride
        hidden_dim = int(input * expand_ratio)
        self.use_res_connect = self.stride == 1 and input == output

        if expand_ratio == 1:
            self.conv = nn.Sequential(

                nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True),
                nn.Conv2d(hidden_dim, output, 1, 1, 0, bias=False),
                nn.BatchNorm2d(output),
            )
        else:
            self.conv = nn.Sequential(
                nn.Conv2d(input, hidden_dim, 1, 1, 0, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True),
                # dw
                nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True),
                # pw-linear
                nn.Conv2d(hidden_dim, output, 1, 1, 0, bias=False),
                nn.BatchNorm2d(output),
            )

    def forward(self, x):
        if self.use_res_connect:
            return x + self.conv(x)
        else:
            return self.conv(x)


# 模型代码
class Finger_Model(nn.Module):
    # 初始化
    def __init__(self, n_class=7, input_size=224, width_mult=1.):
        super(Finger_Model, self).__init__()

        block = Inverted_Residual
        # 骨干网络的输入通道和输出通道
        input_channel = 32
        last_channel = 1280

        # 倒置残差内部结构
        interverted_residual_setting = [
            [1, 16, 1, 1],
            [6, 32, 3, 2],
            [6, 96, 3, 1],
            [6, 160, 3, 2],
            [6, 320, 1, 1],
        ]
        self.last_channel = make_divisible(last_channel * width_mult) if width_mult > 1.0 else last_channel
        self.features = [conv_bn(3, input_channel, 2)]
        # 构建倒置残差
        for t, c, n, s in interverted_residual_setting:
            output_channel = make_divisible(c * width_mult) if t > 1 else c
            for i in range(n):
                if i == 0:
                    self.features.append(block(input_channel, output_channel, s, expand_ratio=t))
                else:
                    self.features.append(block(input_channel, output_channel, 1, expand_ratio=t))
                input_channel = output_channel
        # 最后一层
        self.features.append(conv_1x1_bn(input_channel, self.last_channel))
        self.features = nn.Sequential(*self.features)

        # 分类数目
        self.classifier = nn.Linear(self.last_channel, n_class)

        self.initialize_weights()

    # 前向传播
    def forward(self, x):
        x = self.features(x)
        x = x.mean(3).mean(2)
        x = self.classifier(x)
        return x

    # 初始化权重
    def initialize_weights(self):

        for m in self.modules():
            # 卷积层
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
                if m.bias is not None:
                    m.bias.data.zero_()
            # 归一化层
            elif isinstance(m, nn.BatchNorm2d):

                m.weight.data.fill_(1)
                m.bias.data.zero_()
            # 线性层
            elif isinstance(m, nn.Linear):
                n = m.weight.size(1)
                m.weight.data.normal_(0, 0.01)
                m.bias.data.zero_()


if __name__ == '__main__':
    net = finger_class(n_class=2)
