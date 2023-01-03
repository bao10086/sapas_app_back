# -*- coding = utf-8 -*-
# @Time : 2022/11/15 19:13
# @Author : 曾佳宝
# @File : user_information.py
# @Software : PyCharm
import base64

import cpca
from flask import Blueprint, request

from src.entity.User import User
from src.mapper import user_mapper, error_log_mapper
from src.util import constant

blueprint = Blueprint('user', __name__, url_prefix="/user")


@blueprint.route('/get_information', methods=['POST'])
def get_information():
    phone = request.form.get("phone")

    result = {'code': 403, 'data': '设置失败'}
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        print('找不到用户', phone)
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + result['data'])
        return result
    # 获取头像信息
    print(user.image_path)
    with open(user.image_path, 'rb') as f:
        data = base64.b64encode(f.read())
    # 获取返回信息
    msg = {'image': str(data), 'sex': user.sex, 'birthday': user.DOB.strftime('%Y-%m-%d'),
           'position': user.province + user.city + user.district}
    result['msg'] = msg
    result['code'] = 200
    result['data'] = '返回成功'
    print(result)
    return result


@blueprint.route('/set_information', methods=['POST'])
def set_information():
    # 获取参数
    phone = request.form.get("user_phone")
    image = request.files.get("user_image")
    position = request.form.get("user_position")
    sex = request.form.get("user_sex")
    birthday = request.form.get("user_DOB")

    # 根据前端传来的位置信息获取省、市、区
    location = [position]
    df = cpca.transform(location)
    province = df.iat[0, 0]
    city = df.iat[0, 1]
    district = df.iat[0, 2]
    print(province, city, district)

    # 保存头像（手机号码，例如：15973958319.jpg）
    image_path = constant.PATH + 'image/' + phone + '.jpg'
    image.save(image_path)
    result = {'code': 403, 'data': '设置失败'}

    # 判断用户是否存在
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '找不到用户'
        error_log_mapper.add_error(phone + "设置用户信息" + result['data'])
        return result
    print('用户', phone, '正在更新个人信息')

    # 更新数据库操作
    new_user = User()
    new_user.phone = phone
    new_user.sex = sex
    new_user.province = province
    new_user.city = city
    new_user.district = district
    new_user.dob = birthday
    if user_mapper.update_user_information(new_user) is False:
        return result
    result['code'] = 200
    result['data'] = '更新成功'
    return result
