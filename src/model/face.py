# -*- coding = utf-8 -*-
# @Time : 2022/11/14 22:22
# @Author : 曾佳宝
# @File : face_model.py
# @Software : PyCharm

from src.model.face_model.infer import infer


def is_right_face(phone, path):
    # pre_phone = infer()
    # print(pre_phone)
    # print(phone)
    #
    # if pre_phone == phone:
    #     return True
    # return False
    return True


def find_name_by_phone(phone, file):
    print(phone, file)
    return '默认'


if __name__ == '__main__':
    is_right_face('dadada')
