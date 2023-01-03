# -*- coding = utf-8 -*-
# @Time : 2022/11/24 15:36
# @Author : 曾佳宝
# @File : feedback_mapper.py
# @Software : PyCharm
import time

from src.app import db
from src.mapper import error_log_mapper
from src.mapper.model import Feedback


def add_feedback(user_id, message):
    """
    添加反馈信息
    :param user_id: 用户id
    :param message: 具体反馈信息
    :return:
    """
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        feedback = Feedback(user_id=user_id, time=current_time, info=message,
                            is_solve=0, deleted=0)
        db.session.add(feedback)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return False


def find_by_user_id(user_id):
    try:
        feedback_list = db.session.query(Feedback).filter(Feedback.user_id == user_id).all()
        return feedback_list
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return None


def del_feedback(user_id, message):
    try:
        feedback = db.session.query(Feedback).filter_by(user_id=user_id, info=message, deleted=0).first()
        if feedback is None:
            return False
        feedback.deleted = 1
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_log_mapper.add_error(e)
        print(e)
    return False
