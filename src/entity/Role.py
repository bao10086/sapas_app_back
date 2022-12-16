# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:30
# @Author : 曾佳宝
# @File : Role.py
# @Software : PyCharm

class Role(object):
    __role_name = ''
    __role_id = 0

    @property
    def role_name(self):
        return self.__role_name

    @role_name.setter
    def role_name(self, role_name):
        self.__role_name = role_name

    @property
    def role_id(self):
        return self.__role_id

    @role_id.setter
    def role_id(self, role_id):
        self.__role_id = role_id
