# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:26
# @Author : 曾佳宝
# @File : LogLogin.py
# @Software : PyCharm

class LogLogin(object):
    __id = 0
    __user_id = 0
    __time = ''
    __address = ''
    __device = ''

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, login_log_id):
        self.__id = login_log_id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address

    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, device):
        self.__device = device
