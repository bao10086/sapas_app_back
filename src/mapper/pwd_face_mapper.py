# -*- coding = utf-8 -*-
# @Time : 2022/11/15 22:02
# @Author : 曾佳宝
# @File : pwd_face_mapper.py
# @Software : PyCharm

from src.app import db
from src.mapper import error_log_mapper
from src.mapper.model import PwdFace


def find_face_pwd_by_user_id(user_id):
    try:
        face_pwd = db.session.query(PwdFace).filter_by(user_id=user_id, deleted=0).first()
        if face_pwd is not None:
            return face_pwd
        else:
            return None
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def add_pwd(user_id, face_name, face_image_path):
    try:
        pwd_face_db = PwdFace(user_id=user_id, name=face_name, image_path=face_image_path, deleted=0)
        db.session.add(pwd_face_db)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return False


def del_pwd(user_id, pwd_name):
    try:
        pwd = db.session.query(PwdFace).filter_by(user_id=user_id, name=pwd_name, deleted=0).first()
        print(pwd)
        if pwd is None:
            return None
        pwd_path = pwd.image_path
        pwd.deleted = 1
        db.session.commit()
        return pwd_path
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def get_pwd(user_id):
    try:
        models = db.session.query(PwdFace).filter_by(user_id=user_id, deleted=0).all()
        if models is None:
            return None
        result = []
        for pwd in models:
            result.append(pwd.name)
        print(result)
        return result
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def find_face_pwd_by_user_id_and_path(user_id, path):
    try:
        pwd = db.session.query(PwdFace).filter_by(user_id=user_id, image_path=path, deleted=0).first()
        return pwd
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def update_path_and_name(pwd, path, name):
    try:
        pwd.image_path = path
        pwd.name = name
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None
