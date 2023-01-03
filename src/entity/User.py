# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:31
# @Author : 曾佳宝
# @File : User.py
# @Software : PyCharm


class User(object):
    __phone = ''
    __DOB = ''
    __sex = 0
    __province = ''
    __city = ''
    __district = ''
    __register_time = ''
    __image_path = ''
    __id = 0
    __face_pwd_path = ''
    __fingerprint_pwd_path = ''
    __fingerprint_model_path = ''

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    @property
    def dob(self):
        return self.__DOB

    @dob.setter
    def dob(self, dob):
        self.__DOB = dob

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, sex):
        self.__sex = sex

    @property
    def province(self):
        return self.__province

    @province.setter
    def province(self, province):
        self.__province = province

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    @property
    def district(self):
        return self.__district

    @district.setter
    def district(self, district):
        self.__district = district

    @property
    def register_time(self):
        return self.__register_time

    @register_time.setter
    def register_time(self, register_time):
        self.__register_time = register_time

    @property
    def image_path(self):
        return self.__image_path

    @image_path.setter
    def image_path(self, image_path):
        self.__image_path = image_path

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, user_id):
        self.__id = user_id

    @property
    def face_pwd_path(self):
        return self.__face_pwd_path

    @face_pwd_path.setter
    def face_model_id(self, face_pwd_path):
        self.__face_pwd_path = face_pwd_path

    @property
    def fingerprint_pwd_path(self):
        return self.__fingerprint_pwd_path

    @fingerprint_pwd_path.setter
    def fingerprint_pwd_path(self, fingerprint_pwd_path):
        self.__fingerprint_pwd_path = fingerprint_pwd_path

    @property
    def fingerprint_model_path(self):
        return self.__fingerprint_model_path

    @fingerprint_model_path.setter
    def fingerprint_model_path(self, fingerprint_model_path):
        self.__fingerprint_model_path = fingerprint_model_path
