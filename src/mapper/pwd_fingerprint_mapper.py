# -*- coding = utf-8 -*-
# @Time : 2022/11/15 22:20
# @Author : 曾佳宝
# @File : pwd_fingerprint_mapper.py
# @Software : PyCharm

from src.app import db
from src.mapper import error_log_mapper
from src.mapper.model import PwdFingerprint


def find_fingerprint_pwd_by_user_id(user_id):
    try:
        fingerprint_pwd = db.session.query(PwdFingerprint).filter_by(user_id=user_id, delete=0).first()
        if fingerprint_pwd is not None:
            return fingerprint_pwd
        else:
            return None
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def add_pwd(user_id, fingerprint_name, fingerprint_path):
    try:
        pwd_fingerprint_db = PwdFingerprint(user_id=user_id, name=fingerprint_name,
                                            path=fingerprint_path, deleted=0)
        db.session.add(pwd_fingerprint_db)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
        error_log_mapper.add_error(e)
    return False


def del_pwd(user_id, name):
    try:
        pwd = db.session.query(PwdFingerprint).filter_by(user_id=user_id, name=name, deleted=0).first()
        print(pwd)
        if pwd is None:
            return None
        path = pwd.path
        pwd.deleted = 1
        db.session.commit()
        return path
    except Exception as e:
        print(e)
        db.session.rollback()
        error_log_mapper.add_error(e)
    return None


def get_pwd(user_id):
    try:
        models = db.session.query(PwdFingerprint).filter_by(user_id=user_id, deleted=0).all()
        if models is None:
            return None
        result = []
        for pwd in models:
            result.append(pwd.name)
        return result
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def find_fingerprint_pwd_by_user_id_and_path(user_id, path):
    try:
        pwd_fingerprint = db.session.query(PwdFingerprint).filter_by(user_id=user_id, path=path, deleted=0).first()
        return pwd_fingerprint
    except Exception as e:
        print(e)
        db.session.rollback()
        error_log_mapper.add_error(e)
    return None


def update_path_and_name(pwd, path, name):
    try:
        pwd.path = path
        pwd.name = name
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None
