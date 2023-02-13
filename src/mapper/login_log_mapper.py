# -*- coding = utf-8 -*-
# @Time : 2022/11/24 15:35
# @Author : 曾佳宝
# @File : login_log_mapper.py
# @Software : PyCharm
from src.app import db
from src.mapper import error_log_mapper
from src.mapper.model import LogLogin


def find_log_by_phone(user_id):
    try:
        logs = db.session.query(LogLogin).filter(LogLogin.user_id == user_id).all()
        return logs
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def add_login_log(log):
    try:
        log_db = LogLogin(user_id=log.user_id, time=log.time, device=log.device,
                          address=log.address, deleted=0)
        db.session.add(log_db)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return False
