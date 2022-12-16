# -*- coding = utf-8 -*-
# @Time : 2022/11/15 22:20
# @Author : 曾佳宝
# @File : pwd_fingerprint_mapper.py
# @Software : PyCharm

from src.app import db
from src.mapper.model import PwdFingerprint


def find_fingerprint_pwd_by_user_id(user_id):
    try:
        fingerprint_pwd = db.session.query(PwdFingerprint).filter(PwdFingerprint.user_id == user_id).first()
        if fingerprint_pwd is not None:
            return fingerprint_pwd
        else:
            return None
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def add_pwd(user_id, fingerprint_name, fingerprint_path):
    try:
        pwd = db.session.query(PwdFingerprint).filter_by(user_id=user_id, fingerprint_name=fingerprint_name).first()
        if pwd is not None:
            return False
        pwd_fingerprint_db = PwdFingerprint(user_id=user_id, fingerprint_name=fingerprint_name,
                                            fingerprint_path=fingerprint_path)
        db.session.add(pwd_fingerprint_db)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
    return False


def del_pwd(user_id, name):
    try:
        pwd = db.session.query(PwdFingerprint).filter_by(user_id=user_id, fingerprint_name=name).first()
        print(pwd)
        if pwd is None:
            return None
        path = pwd.fingerprint_path
        db.session.delete(pwd)
        db.session.commit()
        return path
    except Exception as e:
        print(e)
        db.session.rollback()
    return None


def get_pwd(user_id):
    try:
        models = db.session.query(PwdFingerprint).filter(PwdFingerprint.user_id == user_id).all()
        if models is None:
            return None
        result = []
        for pwd in models:
            result.append(pwd.fingerprint_name)
        return result
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def find_fingerprint_pwd_by_user_id_and_path(user_id, path):
    try:
        pwd = db.session.query(PwdFingerprint).filter_by(user_id=user_id, face_image_path=path).first()
        if pwd is not None:
            return pwd
        return None
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def update_path(pwd, path):
    try:
        pwd.face_image_path = path
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    return None
