# -*- coding = utf-8 -*-
# @Time : 2022/12/31 14:29
# @Author : 曾佳宝
# @File : model_fingerprint_mapper.py
# @Software : PyCharm
import time

from src.app import db
from src.mapper import error_log_mapper
from src.mapper.model import ModelFingerprint


def add_model(user_id, name, fingerprint_path):
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        model = ModelFingerprint(user_id=user_id, name=name, path=fingerprint_path, update_time=current_time, deleted=0)
        db.session.add(model)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return False
