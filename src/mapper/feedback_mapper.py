# -*- coding = utf-8 -*-
# @Time : 2022/11/24 15:36
# @Author : 曾佳宝
# @File : feedback_mapper.py
# @Software : PyCharm
import time

from src.app import db
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
        feedback = Feedback(user_id=user_id, feedback_time=current_time, feedback_info=message,
                            feedback_is_solve=0)
        db.session.add(feedback)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
    return False


def find_feedback_by_user_id_and_path(user_id, path):
    try:
        feedback = db.session.query(Feedback).filter_by(user_id=user_id, feedback_image_folder_path=path).first()
        return feedback
    except Exception as e:
        db.session.rollback()
        print(e)
    return None


def find_by_user_id(user_id):
    try:
        feedback_list = db.session.query(Feedback).filter(Feedback.user_id == user_id).all()
        return feedback_list
    except Exception as e:
        db.session.rollback()
        print(e)
    return None
