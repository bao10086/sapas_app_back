# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:29
# @Author : 曾佳宝
# @File : PwdFace.py
# @Software : PyCharm

class PwdFace(object):
    __face_id = 0
    __user_id = 0
    __face_name = ''
    __face_image_path = ''

    @property
    def face_id(self):
        return self.__face_id

    @face_id.setter
    def face_id(self, face_id):
        self.__face_id = face_id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def face_name(self):
        return self.__face_name

    @user_id.setter
    def face_name(self, face_name):
        self.__face_name = face_name

    @property
    def face_image_path(self):
        return self.__face_image_path

    @face_image_path.setter
    def face_image_path(self, face_image_path):
        self.__face_image_path = face_image_path
