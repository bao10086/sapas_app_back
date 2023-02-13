# -*- coding = utf-8 -*-
# @Time : 2022/11/24 15:30
# @Author : 曾佳宝
# @File : feedback.py
# @Software : PyCharm

from flask import Blueprint, request

from src.mapper import user_mapper, feedback_mapper, error_log_mapper

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
        error_log_mapper.add_error(phone + "添加反馈" + result['data'])
        return result
    print('用户', phone, '正在反馈信息')
    user_id = user.id

    # 将反馈信息插入数据库
    if feedback_mapper.add_feedback(user_id, message):
        print('添加反馈信息成功！')
        result['code'] = 200
        result['data'] = '添加成功！'
        return result
    error_log_mapper.add_error(phone + result['data'])
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
        error_log_mapper.add_error(phone + "获取反馈" + result['data'])
        return result
    print('用户', phone, '正在访问反馈信息')
    user_id = user.id

    feedback_list = feedback_mapper.find_by_user_id(user_id)
    if feedback_list is None:
        result['code'] = 404
        result['data'] = '反馈为空'
        error_log_mapper.add_error(phone + "人脸登录" + result['data'])
        return result
    body_list = []
    # 遍历所有查找的反馈信息
    for feedback in feedback_list:
        # 添加进返回数组
        body = {"time": feedback.time.strftime('%Y-%m-%d %H:%M:%S'), "info": feedback.info,
                "is_solve": feedback.is_feedbackd, "reply": feedback.admin_feedback}
        if feedback.admin_feedback_time is not None:
            body["reply_time"] = feedback.admin_feedback_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            body["reply_time"] = feedback.admin_feedback_time
        body_list.append(body)
    result['code'] = 200
    result['data'] = '查找成功'
    result['body'] = body_list
    return result


@blueprint.route("/del_feedback", methods=['POST'])
def del_feedback():
    # 获得用户的手机号和反馈信息
    phone = request.form.get("phone")
    message = request.form.get("message")

    result = {'code': 403, 'data': '删除反馈失败'}
    # 获取用户id
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "删除反馈" + result['data'])
        return result
    print('用户', phone, '正在删除反馈信息')
    user_id = user.id

    # 将反馈信息插入数据库
    if feedback_mapper.del_feedback(user_id, message):
        print('删除反馈信息成功！')
        result['code'] = 200
        result['data'] = '删除成功！'
        return result
    error_log_mapper.add_error(phone + result['data'])
    return result
