# -*- coding = utf-8 -*-
# @Time : 2022/11/24 15:30
# @Author : 曾佳宝
# @File : feedback.py
# @Software : PyCharm

from flask import Blueprint, request

from src.mapper import user_mapper, feedback_mapper

blueprint = Blueprint('feedback', __name__, url_prefix="/feedback")


@blueprint.route("/add_feedback", methods=['POST'])
def add_feedback():
    # 获得用户的手机号和反馈信息
    phone = request.form.get("phone")
    message = request.form.get("message")

    result = {'code': 403, 'data': '反馈失败'}
    # 获取用户id
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        return result
    print('用户', phone, '正在反馈信息')
    user_id = user.user_id

    # 将反馈信息插入数据库
    if feedback_mapper.add_feedback(user_id, message):
        # 找到插入位置的feedback_id
        feedback = feedback_mapper.find_feedback_by_user_id_and_path(user_id)
        if feedback is None:
            return result

        print('添加反馈信息成功！')
        result['code'] = 200
        result['data'] = '添加成功！'
        return result
    return result


@blueprint.route("/get_feedback", methods=['POST'])
def get_feedback():
    # 获得用户的手机号
    phone = request.form.get("phone")
    result = {'code': 403, 'data': '反馈失败'}

    # 获取用户id
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        return result
    print('用户', phone, '正在访问反馈信息')
    user_id = user.user_id

    feedback_list = feedback_mapper.find_by_user_id(user_id)
    if feedback_list is None:
        result['code'] = 200
        result['data'] = '反馈为空'
        return result
    body_list = []
    # 遍历所有查找的反馈信息
    for feedback in feedback_list:
        # 添加进返回数组
        body = {"time": feedback.feedback_time.strftime('%Y-%m-%d %H:%M:%S'), "info": feedback.feedback_info,
                "is_solve": feedback.feedback_is_solve, "reply": feedback.admin_feedback,
                "reply_time": feedback.admin_feedback_time}
        body_list.append(body)
    result['code'] = 200
    result['data'] = '查找成功'
    result['body'] = body_list
    return result
