# -*- coding = utf-8 -*-
# @Time : 2022/11/24 15:21
# @Author : 曾佳宝
# @File : login_log.py
# @Software : PyCharm
import time

from flask import Blueprint, request

from src.entity.LogLogin import LogLogin
from src.mapper import user_mapper, login_log_mapper, error_log_mapper

blueprint = Blueprint('login_log', __name__, url_prefix="/login_log")


@blueprint.route("/get_login_log", methods=['POST'])
def get_login_log():
    # 获取参数
    date = request.form.get("date")
    phone = request.form.get("phone")

    result = {'code': 200, 'data': '获取成功'}
    # 查找用户id
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "获取登录日志" + result['data'])
        return result
    user_id = user.id
    print('用户', phone, '正在获取登录日志信息')

    logs = login_log_mapper.find_log_by_phone(user_id)
    logs_data = []
    for log in logs:
        print(log.time)
        if date in str(log.time):
            return_data = {'device': log.device, 'time': log.time.strftime('%Y-%m-%d %H:%M:%S'),
                           'position': log.address}
            logs_data.append(return_data)
    result['logs'] = logs_data
    return result


@blueprint.route("/add_login_log", methods=['POST'])
def add_login_log():
    # 获取参数
    phone = request.form.get("phone")
    device = request.form.get("device")
    position = request.form.get("position")

    result = {'code': 403, 'data': '添加失败'}
    # 查找用户id
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "新增登录日志" + result['data'])
        return result
    user_id = user.id
    print('用户', phone, '正在写入登录日志')

    log = LogLogin()
    log.user_id = user_id
    log.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log.address = position
    log.device = device
    if login_log_mapper.add_login_log(log):
        result['code'] = 200
        result['data'] = '添加成功'
        return result
    error_log_mapper.add_error(phone + "新增登录日志" + result['data'])
    return result
