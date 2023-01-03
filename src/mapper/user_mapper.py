# -*- coding = utf-8 -*-
# @Time : 2022/11/15 19:14
# @Author : 曾佳宝
# @File : user_mapper.py
# @Software : PyCharm

import time

from src.app import db
from src.mapper import error_log_mapper
from src.mapper.model import User


def add_user(user):
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        user_db = User(phone=user.phone, DOB=user.dob, sex=user.sex, province=user.province, city=user.city,
                       district=user.district, register_time=current_time, image_path=user.image_path,
                       fingerprint_model_id=1, deleted=0)
        db.session.add(user_db)
        db.session.commit()
        return True
    except Exception as e:
        db.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return False


def find_user_by_phone(phone):
    try:
        user = db.session.query(User).filter_by(phone=phone, deleted=0).first()
        if user is not None:
            return user
        else:
            return None
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def update_user_information(new_user):
    try:
        user = db.session.query(User).filter_by(phone=new_user.phone, deleted=0).first()
        user.sex = new_user.sex
        user.DOB = new_user.dob
        user.province = new_user.province
        user.city = new_user.city
        user.district = new_user.district
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
        return False


def insert_image(phone, image_path):
    try:
        user = db.session.query(User).filter_by(user_phone=phone, deleted=0).first()
        user.image_path = image_path
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return False
