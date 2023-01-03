import json
import os
import random
import threading
import time

from flask import Blueprint, request

import cpca
import src.util.zhenzismsclient as smsclient
from src.entity.User import User
from src.mapper import pwd_face_mapper, error_log_mapper, model_fingerprint_mapper
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
    if res['code'] != 0:  # 写入错误日志
        error_log_mapper.add_error(phone + "发送短信验证码失败:" + res['data'])
    new_user = User()
    print(phone)
    for user in users:
        if user.phone == phone:
            res['code'] = 0
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
                error_log_mapper.add_error(phone + result['data'])
                return result
            result['code'] = 200
            result['data'] = '添加成功'
            return result
    error_log_mapper.add_error(phone + result['data'])
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

    result = {'code': 403, 'data': '添加指纹密码失败'}
    # 指纹密码路径名：手机号码，例如：15973958318.wav(暂时路径)
    fingerprint_pwd_path = constant.PATH_FINGER_DB + phone + '/' + phone + '.wav'
    file.save(fingerprint_pwd_path)
    fingerprint_model_path = constant.PATH_FINGER_MODEL_DB + phone + '.pth'
    file.save(fingerprint_model_path)
    os.makedirs(constant.PATH_FINGER_DB + phone, exist_ok=True)
    print('用户', phone, '注册指纹中')
    global finger_phone
    finger_phone = phone
    global finger_file_name
    finger_file_name = phone + '.wav'
    # 查询用户
    for user in users:
        if user.phone == phone:
            print('用户', phone, '正在注册指纹')
            user.fingerprint_pwd_path = fingerprint_pwd_path
            user.fingerprint_model_path = fingerprint_model_path
            thread = threading.Thread(target=train_finger_model)
            thread.start()
            # 检验指纹文件是否保存成功
            if os.path.isfile(fingerprint_pwd_path) is False:
                result['data'] = '保存指纹密码失败'
                error_log_mapper.add_error(phone + result['data'])
                return result
            # 检验指纹模型是否保存成功
            if os.path.isfile(fingerprint_model_path) is False:
                result['data'] = '保存指纹模型失败'
                error_log_mapper.add_error(phone + result['data'])
                return result
            result['code'] = 200
            result['data'] = '添加成功'
            return result
    result['data'] = '注册列表中不存在该用户'
    error_log_mapper.add_error(phone + result['data'])
    return result


@blueprint.route('/register_face_model', methods=['POST'])
def register_face_model():
    # 获取参数
    phone = request.form.get("user_phone")
    file = request.files.get("face_file")

    result = {'code': 403, 'data': '添加人脸数据失败'}
    # 人脸路径名：0，例如：0.jpg(暂时路径)
    face_path = constant.PATH_FACE_DB + phone + '/0.jpg'
    print('用户', phone, '注册中')
    # 查询用户
    for user in users:
        if user.phone == phone:
            print('用户', phone, '正在注册人脸')
            if user_mapper.add_user(user):  # 添加用户成功
                # 找到数据库对应的user_id
                user_db = user_mapper.find_user_by_phone(phone)
                user_id = user_db.id

                # 指纹密码路径名：手机号码/0，例如：15973958319/0.wav
                fingerprint_pwd_path = user.fingerprint_pwd_path
                # 存入数据库
                if pwd_fingerprint_mapper.add_pwd(user_id, '默认', fingerprint_pwd_path) is False:
                    error_log_mapper.add_error(phone + result['data'])
                    return result
                # 找到指纹密码对应的pwd_id
                fingerprint_pwd = pwd_fingerprint_mapper.find_fingerprint_pwd_by_user_id_and_path(user_id,
                                                                                                  fingerprint_pwd_path)
                fingerprint_pwd_id = fingerprint_pwd.id
                fingerprint_new_pwd_path = constant.PATH_FINGER_DB + phone + '/' + str(fingerprint_pwd_id) + '.wav'
                # 修改密码文件名
                os.rename(fingerprint_pwd_path, fingerprint_new_pwd_path)
                # 更新指纹密码路径
                pwd_fingerprint_mapper.update_path(fingerprint_pwd, fingerprint_new_pwd_path)

                # 指纹模型路径名：手机号码，例如：15973958319.pth
                fingerprint_model_path = user.fingerprint_model_path
                # 存入数据库
                if model_fingerprint_mapper.add_model(user_id, phone, fingerprint_model_path) is False:
                    error_log_mapper.add_error(phone + result['data'])
                    return result

                # 人脸密码存入数据库
                if pwd_face_mapper.add_pwd(user_id, '默认', face_path):
                    # 找到人脸密码对应的pwd_id
                    face_pwd = pwd_face_mapper.find_face_pwd_by_user_id_and_path(user_id, face_path)
                    face_pwd_id = face_pwd.id
                    face_path = constant.PATH_FACE_DB + phone + '/' + str(face_pwd_id) + '.jpg'
                    os.makedirs(constant.PATH_FACE_DB + phone)
                    # 更新人脸密码路径
                    pwd_face_mapper.update_path(face_pwd, face_path)
                    # 保存人脸密码
                    file.save(face_path)
                    if os.path.isfile(face_path) is False:
                        result['data'] = '保存人脸失败'
                        error_log_mapper.add_error(phone + result['data'])
                        return result

                    # 设置成功返回值
                    result['code'] = 200
                    result['data'] = '添加成功'
                    users.remove(user)
                    return result
                error_log_mapper.add_error(phone + result['data'])
                return result
    result['code'] = 404
    result['data'] = '用户不在注册列表'
    error_log_mapper.add_error(phone + result['data'])
    return result
