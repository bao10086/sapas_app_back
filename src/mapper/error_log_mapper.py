# -*- coding = utf-8 -*-
# @Time : 2022/12/31 13:43
# @Author : 曾佳宝
# @File : error_log_mapper.py
# @Software : PyCharm
import time

from src.app import db
from src.mapper.model import LogError


def add_error(msg):
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        error = LogError(time=current_time, info=msg, deleted=0)
        db.session.add(error)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        add_error(e)
        print(e)
