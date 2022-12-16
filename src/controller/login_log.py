# -*- coding = utf-8 -*-
# @Time : 2022/11/24 15:21
# @Author : 曾佳宝
# @File : login_log.py
# @Software : PyCharm
import re
import time

from flask import Blueprint, request

from src.entity.LogLogin import LogLogin
from src.mapper import user_mapper, login_log_mapper, notice_mapper

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
        return result
    user_id = user.user_id
    print('用户', phone, '正在获取登录日志信息')

    logs = login_log_mapper.find_log_by_phone(user_id)
    logs_data = []
    for log in logs:
        if date in str(log.login_time):
            return_data = {'device': log.login_device, 'time': log.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                           'position': log.longitude_and_latitude}
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
        return result
    user_id = user.user_id
    print('用户', phone, '正在写入登录日志')

    log = LogLogin()
    log.user_id = user_id
    log.login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log.longitude_and_latitude = position
    log.login_device = device
    if login_log_mapper.add_login_log(log):
        result['code'] = 200
        notices = notice_mapper.get_notice_by_id(user_id)
        data = []
        if notices is None:
            result['data'] = '通知为空'
            return result
        for notice in notices:
            regex = re.compile("(?:[|,)" + str(user_id) + "(?:,|])")
            if regex.findall(notice.user_ids):
                print(notice.user_ids)
                notice_data = {'title': notice.notice_title, 'info': notice.notice_info, 'time': notice.notice_time}
                data.append(notice_data)
        result['data'] = data
        return result
    return result
