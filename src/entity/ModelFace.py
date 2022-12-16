# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:27
# @Author : 曾佳宝
# @File : ModelFace.py
# @Software : PyCharm

class ModelFace(object):
    __face_model_id = 0
    __user_id = 0
    __face_model_name = ''
    __face_model_path = ''
    __face_model_update_time = ''

    @property
    def face_model_id(self):
        return self.__face_model_id

    @face_model_id.setter
    def face_model_id(self, face_model_id):
        self.__face_model_id = face_model_id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def face_model_name(self):
        return self.__face_model_name

    @face_model_name.setter
    def face_model_name(self, face_model_name):
        self.__face_model_name = face_model_name

    @property
    def face_model_path(self):
        return self.__face_model_path

    @face_model_path.setter
    def face_model_path(self, face_model_path):
        self.__face_model_path = face_model_path

    @property
    def face_model_update_time(self):
        return self.__face_model_update_time

    @face_model_update_time.setter
    def face_model_update_time(self, face_model_update_time):
        self.__face_model_update_time = face_model_update_time
