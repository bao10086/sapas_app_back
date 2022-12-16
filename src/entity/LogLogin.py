# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:26
# @Author : 曾佳宝
# @File : LogLogin.py
# @Software : PyCharm

class LogLogin(object):
    __login_log_id = 0
    __user_id = 0
    __login_time = ''
    __login_address = ''
    __login_device = ''

    @property
    def login_log_id(self):
        return self.__login_log_id

    @login_log_id.setter
    def login_log_id(self, login_log_id):
        self.__login_log_id = login_log_id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def login_time(self):
        return self.__login_time

    @login_time.setter
    def login_time(self, login_time):
        self.__login_time = login_time

    @property
    def login_address(self):
        return self.__login_address

    @login_address.setter
    def login_address(self, login_address):
        self.__login_address = login_address

    @property
    def login_device(self):
        return self.__login_device

    @login_device.setter
    def login_device(self, login_device):
        self.__login_device = login_device
