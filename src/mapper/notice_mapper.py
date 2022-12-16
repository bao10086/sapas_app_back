# -*- coding = utf-8 -*-
# @Time : 2022/12/16 13:04
# @Author : 曾佳宝
# @File : notice_mapper.py
# @Software : PyCharm
from src.app import db
from src.mapper.model import Notice


def get_notice_by_id(user_id):
    try:
        notices = db.session.query(Notice).all()
        return notices
    except Exception as e:
        db.session.rollback()
        print(e)
    return None
