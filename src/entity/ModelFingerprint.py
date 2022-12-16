# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:28
# @Author : 曾佳宝
# @File : ModelFingerprint.py
# @Software : PyCharm

class ModelFingerprint(object):
    __fingerprint_model_id = 0
    __user_id = 0
    __fingerprint_model_name = ''
    __fingerprint_model_model_path = ''
    __fingerprint_model_update_time = ''

    @property
    def fingerprint_model_id(self):
        return self.__fingerprint_model_id

    @fingerprint_model_id.setter
    def fingerprint_model_id(self, fingerprint_model_id):
        self.__fingerprint_model_id = fingerprint_model_id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def fingerprint_model_name(self):
        return self.__fingerprint_model_name

    @fingerprint_model_name.setter
    def fingerprint_model_name(self, fingerprint_model_name):
        self.__fingerprint_model_name = fingerprint_model_name

    @property
    def fingerprint_model_model_path(self):
        return self.__fingerprint_model_model_path

    @fingerprint_model_model_path.setter
    def fingerprint_model_model_path(self, fingerprint_model_model_path):
        self.__fingerprint_model_model_path = fingerprint_model_model_path

    @property
    def fingerprint_model_update_time(self):
        return self.__fingerprint_model_update_time

    @fingerprint_model_update_time.setter
    def fingerprint_model_update_time(self, fingerprint_model_update_time):
        self.__fingerprint_model_update_time = fingerprint_model_update_time
