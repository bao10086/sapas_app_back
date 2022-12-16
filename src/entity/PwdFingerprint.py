# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:30
# @Author : 曾佳宝
# @File : PwdFingerprint.py
# @Software : PyCharm

class PwdFingerprint(object):
    __fingerprint_id = 0
    __user_id = 0
    __fingerprint_name = ''
    __fingerprint_path = ''

    @property
    def fingerprint_id(self):
        return self.__fingerprint_id

    @fingerprint_id.setter
    def fingerprint_id(self, fingerprint_id):
        self.__fingerprint_id = fingerprint_id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def fingerprint_name(self):
        return self.__fingerprint_name

    @fingerprint_name.setter
    def fingerprint_name(self, fingerprint_name):
        self.__fingerprint_name = fingerprint_name

    @property
    def fingerprint_path(self):
        return self.__fingerprint_path

    @fingerprint_path.setter
    def fingerprint_path(self, fingerprint_path):
        self.__fingerprint_path = fingerprint_path
