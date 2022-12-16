# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:31
# @Author : 曾佳宝
# @File : RolePermission.py
# @Software : PyCharm

class RolePermission(object):
    __role_id = 0
    __permission_id = 0

    @property
    def role_id(self):
        return self.__role_id

    @role_id.setter
    def role_id(self, role_id):
        self.__role_id = role_id

    @property
    def permission_id(self):
        return self.__permission_id

    @permission_id.setter
    def permission_id(self, permission_id):
        self.__permission_id = permission_id
