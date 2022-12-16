# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:32
# @Author : 曾佳宝
# @File : UserRole.py
# @Software : PyCharm

class UserRole(object):
    __user_id = 0
    __role_id = 0

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def role_id(self):
        return self.__role_id

    @role_id.setter
    def role_id(self, role_id):
        self.__role_id = role_id
