# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:26
# @Author : 曾佳宝
# @File : LogError.py
# @Software : PyCharm

class LogError(object):
    __error_log_id = 0
    __error_time = ''
    __error_info = ''

    @property
    def error_log_id(self):
        return self.__error_log_id

    @error_log_id.setter
    def error_log_id(self, error_log_id):
        self.__error_log_id = error_log_id

    @property
    def error_time(self):
        return self.__error_time

    @error_time.setter
    def error_time(self, error_time):
        self.__error_time = error_time

    @property
    def error_info(self):
        return self.__error_info

    @error_info.setter
    def error_info(self, error_info):
        self.__error_info = error_info
