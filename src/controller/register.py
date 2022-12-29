import json
import os
import random
import threading
import time

from flask import Blueprint, request

import cpca
import src.util.zhenzismsclient as smsclient
from src.entity.User import User
from src.mapper import pwd_face_mapper
from src.mapper import pwd_fingerprint_mapper
from src.mapper import user_mapper
from src.util import constant
from src.model.fingerprint_model import finger_reg
blueprint = Blueprint('register', __name__, url_prefix="/register")

users = []
finger_phone = ''
finger_file_name = ''


@blueprint.route('/send_code', methods=['POST'])
def send_code():
    # 得到参数
    phone = request.form.get("phone")

    res = {'code': 403, 'data': '设置失败'}
    if user_mapper.find_user_by_phone(phone) is not None:
        res['code'] = 403
        res['data'] = '用户已存在'
        return res
    client = smsclient.ZhenziSmsClient('https://sms_developer.zhenzikj.com', 112416,
                                       'a2e555e7-f7d9-4046-9518-73b9b06fef76')
    code = str(random.randint(1000, 9999))
    params = {'number': phone, 'templateId': '10495', 'templateParams': [code, '1']}
    res = json.loads(client.send(params))
    new_user = User()
    print(phone)
    for user in users:
        if user.phone == phone:
            res['code'] = 200
            res['data'] = '用户重新注册'
            res['secret'] = code
            print('用户重新注册：', phone)
            return res
    new_user.phone = phone
    print(new_user.phone)
    users.append(new_user)
    print('users添加新用户', phone)
    res['secret'] = code
    print(res)
    return res


@blueprint.route('/set_user_information', methods=['POST'])
def set_information():
    # 得到参数
    image = request.files.get("user_image")
    phone = request.form.get("user_phone")
    sex = request.form.get("user_sex")
    birthday = request.form.get("user_DOB")
    position = request.form.get("user_position")

    # 获取省、市、区
    location_str = [position]
    df = cpca.transform(location_str)
    province = df.iat[0, 0]
    city = df.iat[0, 1]
    district = df.iat[0, 2]

    # 头像路径名：手机号码，例如：15973958319.jpg
    image_path = constant.PATH + 'image/' + phone + '.jpg'
    result = {'code': 404, 'data': '找不到用户'}
    # 查询用户
    for user in users:
        if user.phone == phone:
            print('用户', phone, '正在设置个人信息')
            user.image_path = image_path
            user.sex = sex
            user.dob = birthday
            user.province = province
            user.city = city
            user.district = district
            image.save(image_path)
            if os.path.isfile(image_path) is False:
                result['data'] = '保存头像失败'
                return result
            result['code'] = 200
            result['data'] = '添加成功'
            return result
    return result


def train_finger_model():
    print(finger_phone)
    # print(finger_file_name)
    finger_reg.finger_reg_main(str(finger_file_name), str(finger_phone))


def test_thread():
    time.sleep(11)


@blueprint.route('/register_fingerprint_model', methods=['POST'])
def register_fingerprint_model():
    # 获取参数
    phone = request.form.get("user_phone")
    file = request.files.get("fingerprint_file")

    result = {'code': 403, 'data': '添加失败'}
    # 指纹路径名：手机号码，例如：15973958319.jpg
    fingerprint_path = constant.PATH_FINGER_DB + phone + '/1.wav'
    os.makedirs(constant.PATH_FINGER_DB + phone, exist_ok=True)
    print('用户', phone, '注册中')
    global finger_phone
    finger_phone = phone
    global finger_file_name
    finger_file_name = '1.wav'
    # 查询用户
    for user in users:
        if user.phone == phone:
            print('用户', phone, '正在注册指纹')
            user.fingerprint_model_id = fingerprint_path
            file.save(fingerprint_path)
            thread = threading.Thread(target=train_finger_model)
            thread.start()
            if os.path.isfile(fingerprint_path) is False:
                result['data'] = '保存指纹失败'
                return result

            result['code'] = 200
            result['data'] = '添加成功'
            return result
    return result


@blueprint.route('/register_face_model', methods=['POST'])
def register_face_model():
    # 获取参数
    phone = request.form.get("user_phone")
    file = request.files.get("face_file")

    result = {'code': 403, 'data': '添加失败'}
    # 人脸路径名：手机号码+名字，例如：15973958319_默认.jpg
    face_path = constant.PATH_FACE_DB + phone + '.jpg'
    file.save(face_path)
    if os.path.isfile(face_path) is False:
        result['data'] = '保存人脸失败'
        return result
    print('用户', phone, '注册中')
    # 查询用户
    for user in users:
        if user.phone == phone:
            print('用户', phone, '正在注册人脸')
            if user_mapper.add_user(user):  # 添加用户成功
                # 找到数据库对应的user_id
                user_db = user_mapper.find_user_by_phone(phone)
                user_id = user_db.id

                # 指纹路径名：手机号码+pwd_id，例如：15973958319_1.jpg
                fingerprint_path = user.fingerprint_model_id
                # 存入数据库
                if pwd_fingerprint_mapper.add_pwd(user_id, '默认', fingerprint_path) is False:
                    return result

                # 存入数据库
                if pwd_face_mapper.add_pwd(user_id, '默认', face_path):
                    # 设置成功返回值
                    result['code'] = 200
                    result['data'] = '添加成功'
                    users.remove(user)
                    return result
                return result
    result['code'] = 404
    result['data'] = '用户不在注册列表'
    return result
