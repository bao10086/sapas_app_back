# -*- coding = utf-8 -*-
# @Time : 2022/11/24 15:35
# @Author : 曾佳宝
# @File : login_log_mapper.py
# @Software : PyCharm
from src.app import db
from src.mapper.model import LogLogin


def find_log_by_phone(user_id):
    try:
        logs = db.session.query(LogLogin).filter(LogLogin.user_id == user_id).all()
        return logs
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def add_login_log(log):
    try:
        log_db = LogLogin(user_id=log.user_id, login_time=log.login_time, login_device=log.login_device,
                          login_address=log.login_address)
        db.session.add(log_db)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
    return False
