# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:29
# @Author : 曾佳宝
# @File : Permissions.py
# @Software : PyCharm

class Permissions(object):
    __permission_id = 0
    __permission_name = ''

    @property
    def permission_id(self):
        return self.__permission_id

    @permission_id.setter
    def permission_id(self, permission_id):
        self.__permission_id = permission_id

    @property
    def permission_name(self):
        return self.__permission_name

    @permission_name.setter
    def permission_name(self, permission_name):
        self.__permission_name = permission_name
