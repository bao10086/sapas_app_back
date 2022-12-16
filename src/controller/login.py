# -*- coding = utf-8 -*-
# @Time : 2022/11/14 22:22
# @Author : 曾佳宝
# @File : login.py
# @Software : PyCharm

from flask import Blueprint, request

from src.mapper import user_mapper
from src.model import face_model
from src.model import fingerprint
from src.model import face

blueprint = Blueprint('login', __name__, url_prefix="/login")
from src.util import constant


@blueprint.route("/face", methods=['POST'])
def face_login():
    print(11111)
    phone = request.form.get("user_phone")
    picture = request.files.get('face_picture')
    face_path = constant.PATH_FACE_TEST + 'test.jpg'
    picture.save(face_path)
    print('**************************************')
    result = {'code': 403, 'data': '人脸登录失败'}
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        return result
    if face.is_right_face(phone):
        result['code'] = '200'
        result['data'] = '人脸登录成功'
        return result
    return result


@blueprint.route("/fingerprint", methods=['POST'])
def fingerprint_login():
    phone = request.form.get("user_phone")
    radio = request.files.get('fingerprint_model')
    result = {'code': 403, 'data': '指纹登录失败'}
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        return result
    if fingerprint.is_right_fingerprint(phone, radio):
        result['code'] = '200'
        result['data'] = '指纹登录成功'
        return result
    return result
