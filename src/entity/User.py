# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:31
# @Author : 曾佳宝
# @File : User.py
# @Software : PyCharm


class User(object):
    __user_phone = ''
    __user_DOB = ''
    __user_sex = 0
    __user_province = ''
    __user_city = ''
    __user_district = ''
    __user_register_time = ''
    __user_image_path = ''
    __user_id = 0
    __face_model_id = 0
    __fingerprint_model_id = 0

    @property
    def user_phone(self):
        return self.__user_phone

    @user_phone.setter
    def user_phone(self, user_phone):
        self.__user_phone = user_phone

    @property
    def user_dob(self):
        return self.__user_DOB

    @user_dob.setter
    def user_dob(self, user_dob):
        self.__user_DOB = user_dob

    @property
    def user_sex(self):
        return self.__user_sex

    @user_sex.setter
    def user_sex(self, user_sex):
        self.__user_sex = user_sex

    @property
    def user_province(self):
        return self.__user_province

    @user_province.setter
    def user_province(self, user_province):
        self.__user_province = user_province

    @property
    def user_city(self):
        return self.__user_city

    @user_city.setter
    def user_city(self, user_city):
        self.__user_city = user_city

    @property
    def user_district(self):
        return self.__user_district

    @user_district.setter
    def user_district(self, user_district):
        self.__user_district = user_district

    @property
    def user_register_time(self):
        return self.__user_register_time

    @user_register_time.setter
    def user_register_time(self, user_register_time):
        self.__user_register_time = user_register_time

    @property
    def user_image_path(self):
        return self.__user_image_path

    @user_image_path.setter
    def user_image_path(self, user_image_path):
        self.__user_image_path = user_image_path

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def face_model_id(self):
        return self.__face_model_id

    @face_model_id.setter
    def face_model_id(self, face_model_id):
        self.__face_model_id = face_model_id

    @property
    def fingerprint_model_id(self):
        return self.__fingerprint_model_id

    @fingerprint_model_id.setter
    def fingerprint_model_id(self, fingerprint_model_id):
        self.__fingerprint_model_id = fingerprint_model_id
