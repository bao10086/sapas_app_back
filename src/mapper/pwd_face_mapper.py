# -*- coding = utf-8 -*-
# @Time : 2022/11/15 22:02
# @Author : 曾佳宝
# @File : pwd_face_mapper.py
# @Software : PyCharm

from src.app import db
from src.mapper.model import PwdFace


def find_face_pwd_by_user_id(user_id):
    try:
        face_pwd = db.session.query(PwdFace).filter(PwdFace.user_id == user_id).first()
        if face_pwd is not None:
            return face_pwd
        else:
            return None
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def add_pwd(user_id, face_name, face_image_path):
    try:
        pwd = db.session.query(PwdFace).filter_by(user_id=user_id, face_name=face_name).first()
        if pwd is not None:
            return False
        pwd_face_db = PwdFace(user_id=user_id, face_name=face_name, face_image_path=face_image_path)
        db.session.add(pwd_face_db)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
    return False


def del_pwd(user_id, pwd_name):
    try:
        pwd = db.session.query(PwdFace).filter_by(user_id=user_id, face_name=pwd_name).first()
        print(pwd)
        if pwd is None:
            return None
        pwd_path = pwd.fingerprint_path
        db.session.delete(pwd)
        db.session.commit()
        return pwd_path
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def get_pwd(user_id):
    try:
        models = db.session.query(PwdFace).filter(PwdFace.user_id == user_id).all()
        if models is None:
            return None
        result = []
        for pwd in models:
            result.append(pwd.face_name)
        print(result)
        return result
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def find_face_pwd_by_user_id_and_path(user_id, path):
    try:
        pwd = db.session.query(PwdFace).filter_by(user_id=user_id, fingerprint_path=path).first()
        return pwd
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def update_path(pwd, path):
    try:
        pwd.fingerprint_path = path
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    return None
