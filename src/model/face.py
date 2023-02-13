# -*- coding = utf-8 -*-
# @Time : 2022/11/14 22:22
# @Author : 曾佳宝
# @File : face_model.py
# @Software : PyCharm

from src.model.face_model.infer import infer


def is_right_face(phone, path):
    # 传手机号和登录时用来检测的人脸地址
    return infer(phone, path)


if __name__ == '__main__':
    is_right_face('dadada')
