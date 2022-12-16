# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:17
# @Author : 曾佳宝
# @File : Admin.py
# @Software : PyCharm

# 管理员类
class Admin(object):
    # private
    __admin_id = 0  # id
    __admin_account = ''  # 账号
    __admin_password = ''  # 密码
    __admin_name = ''  # 用户名
    __admin_image_path = ''  # 头像地址

    # 初始化管理员对象
    def __init__(self, account, password=None, name=None, image_path=None):
        self.__admin_account = account
        self.__admin_password = password
        self.__admin_name = name
        self.__admin_image_path = image_path

    @property
    def admin_id(self):
        return self.__admin_id

    @admin_id.setter
    def admin_id(self, admin_id):
        self.__admin_id = admin_id

    @property
    def admin_account(self):
        return self.__admin_account

    @admin_account.setter
    def admin_account(self, admin_account):
        self.__admin_account = admin_account

    @property
    def admin_password(self):
        return self.__admin_password

    @admin_password.setter
    def admin_password(self, admin_password):
        self.__admin_password = admin_password

    @property
    def admin_name(self):
        return self.__admin_name

    @admin_name.setter
    def admin_name(self, admin_name):
        self.__admin_name = admin_name

    @property
    def admin_image_path(self):
        return self.__admin_image_path

    @admin_image_path.setter
    def admin_image_path(self, admin_image_path):
        self.__admin_image_path = admin_image_path
