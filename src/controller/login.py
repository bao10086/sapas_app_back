# -*- coding = utf-8 -*-
# @Time : 2022/11/14 22:22
# @Author : 曾佳宝
# @File : login.py
# @Software : PyCharm
import os
import time

from flask import Blueprint, request

from src.mapper import user_mapper, error_log_mapper
from src.model import face
from src.model import fingerprint
from src.util import constant

blueprint = Blueprint('login', __name__, url_prefix="/login")


@blueprint.route("/find_phone", methods=['POST'])
def login():
    phone = request.form.get("user_phone")
    result = {'code': 200, 'data': '手机验证成功'}
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "手机验证" + result['data'])
    return result


@blueprint.route("/face", methods=['POST'])
def face_login():
    phone = request.form.get("user_phone")
    picture = request.files.get('face_picture')
    current_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    face_path = constant.PATH_FACE_TEST + phone + '_' + current_time + '.jpg'
    picture.save(face_path)
    result = {'code': 403, 'data': '人脸登录失败'}
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "人脸登录" + result['data'])
        return result
    if face.is_right_face(phone, face_path):
        os.remove(face_path)
        result['code'] = '200'
        result['data'] = '人脸登录成功'
        return result
    error_log_mapper.add_error(phone + result['data'])
    return result


@blueprint.route("/fingerprint", methods=['POST'])
def fingerprint_login():
    phone = request.form.get("user_phone")
    radio = request.files.get('fingerprint')
    current_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    fingerprint_path = constant.PATH_FINGER_TEST + phone + '_' + current_time + '.wav'
    result = {'code': 403, 'data': '指纹登录失败'}
    radio.save(fingerprint_path)
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "指纹登录" + result['data'])
        return result
    if fingerprint.is_right_fingerprint(phone, fingerprint_path):
        result['code'] = '200'
        result['data'] = '指纹登录成功'
        return result
    error_log_mapper.add_error(phone + result['data'])
    return result
