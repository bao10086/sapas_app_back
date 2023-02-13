# -*- coding = utf-8 -*-
# @Time : 2023/2/6 21:43
# @Author : 曾佳宝
# @File : notice.py
# @Software : PyCharm

import re

from flask import Blueprint, request

from src.mapper import error_log_mapper, notice_mapper, user_mapper

blueprint = Blueprint('notice', __name__, url_prefix="/notice")


@blueprint.route("/get_notice", methods=['POST'])
def get_notice():
    # 获取参数
    phone = request.form.get("phone")

    result = {'code': 200, 'data': '获取成功'}
    # 查找用户id
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "获取通知" + result['data'])
        return result
    user_id = user.id
    print('用户', phone, '正在获取通知信息')
    notices = notice_mapper.get_notice_by_id(user_id)
    data = []
    if notices is None:
        result['data'] = '通知为空'
        return result
    for notice in notices:
        regex = re.compile("(\[|,)" + str(user_id) + "(,|\])")
        if regex.findall(notice.user_ids):
            print(notice.user_ids)
            print(notice.time)
            notice_data = {'title': notice.title, 'info': notice.info,
                           'time': notice.time.strftime('%Y-%m-%d %H:%M:%S')}
            data.append(notice_data)
    result['data'] = data
    return result
