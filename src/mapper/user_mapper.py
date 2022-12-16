# -*- coding = utf-8 -*-
# @Time : 2022/11/15 19:14
# @Author : 曾佳宝
# @File : user_mapper.py
# @Software : PyCharm

import time

from src.app import db
from src.mapper.model import User


def add_user(user):
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        user_db = User(user_phone=user.user_phone, user_DOB=user.user_dob, user_sex=user.user_sex,
                       user_province=user.user_province, user_city=user.user_city, user_district=user.user_district,
                       user_register_time=current_time, user_image_path=user.user_image_path, fingerprint_model_id=1)
        db.session.add(user_db)
        db.session.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
    return False


def find_user_by_phone(phone):
    try:
        user = db.session.query(User).filter(User.user_phone == phone).first()
        if user is not None:
            return user
        else:
            return None
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def update_user_information(new_user):
    try:
        user = db.session.query(User).filter(User.user_phone == new_user.user_phone).first()
        user.user_sex = new_user.user_sex
        user.user_DOB = new_user.user_dob
        user.user_province = new_user.user_province
        user.user_city = new_user.user_city
        user.user_district = new_user.user_district
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def insert_image(phone, image_path):
    try:
        user = db.session.query(User).filter(User.user_phone == phone).first()
        user.user_image_path = image_path
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
    return False
