import os

from flask import Blueprint, request

from src.mapper import user_mapper, pwd_face_mapper, pwd_fingerprint_mapper, error_log_mapper
from src.model import fingerprint, face
from src.util import constant

blueprint = Blueprint('mapper', __name__, url_prefix="/pwd")


@blueprint.route('/del_pwd', methods=['POST'])
def del_model():
    # 得到参数
    phone = request.form.get('user_phone')
    pwd_type = request.form.get('pwd_type')
    pwd_name = request.form.get('pwd_name')

    result = {'code': 403, 'data': '设置失败'}
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "删除密码" + result['data'])
        return result
    user_id = user.id
    # 找到对应密码文件目录，并在数据库里执行删除操作
    if pwd_type == '1':  # 指纹声音模型
        pwd_path = pwd_fingerprint_mapper.del_pwd(user_id, pwd_name)
    else:  # 人脸模型
        pwd_path = pwd_face_mapper.del_pwd(user_id, pwd_name)
    # 删除对应文件
    if pwd_path is not None and os.path.isfile(pwd_path):
        os.remove(pwd_path)
        result['code'] = 200
        result['data'] = '删除成功'
    else:
        result['data'] = 404
        result['data'] = '密码不存在'
        error_log_mapper.add_error(phone + "删除密码" + result['data'])
    error_log_mapper.add_error(phone + "删除密码" + result['data'])
    return result


@blueprint.route('/add_pwd', methods=['POST'])
def add_pwd():
    # 得到参数
    phone = request.form.get('user_phone')
    pwd_type = request.form.get('pwd_type')
    pwd_file = request.files.get('pwd_file')

    result = {'code': 403, 'data': '设置失败'}
    pwd_name = phone
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "添加密码" + result['data'])
        return result
    user_id = user.id

    if pwd_type == '1':  # 指纹声音模型
        # 暂时的密码路径，需要之后获取pwd_id，以手机号/pwd_id.wav形式存储
        pwd_path = constant.PATH_FINGER_DB + phone + "/" + phone + ".wav"
        # 添加到数据库
        pwd_fingerprint_mapper.add_pwd(user_id, pwd_name, pwd_path)
        # 找到添加后的pwd_id
        pwd = pwd_fingerprint_mapper.find_fingerprint_pwd_by_user_id_and_path(user_id, pwd_path)
        print(pwd)
        pwd_id = pwd.id
        # 更新路径信息
        pwd_path = constant.PATH_FINGER_DB + phone + "/" + str(pwd_id) + '.wav'
        pwd_name = str(pwd_id)
        # 保存文件
        pwd_file.save(pwd_path)
        if os.path.isfile(pwd_path) is False:
            result['data'] = '保存密码失败'
            return result
        # 更新数据库
        pwd_fingerprint_mapper.update_path_and_name(pwd, pwd_path, pwd_name)
    else:  # 人脸模型
        # 暂时的密码路径，需要之后获取pwd_id，以手机号/pwd_id.jpg形式存储
        pwd_path = constant.PATH_FACE_DB + phone + "/" + phone + ".jpg"
        # 添加到数据库
        pwd_face_mapper.add_pwd(user_id, pwd_name, pwd_path)
        # 找到添加后的pwd_id
        pwd = pwd_face_mapper.find_face_pwd_by_user_id_and_path(user_id, pwd_path)
        pwd_id = pwd.id
        # 更新路径信息
        pwd_path = constant.PATH_FACE_DB + phone + "/" + str(pwd_id) + '.jpg'
        pwd_name = str(pwd_id)
        # 保存文件
        pwd_file.save(pwd_path)
        if os.path.isfile(pwd_path) is False:
            result['data'] = '保存密码失败'
            error_log_mapper.add_error(phone + "添加密码" + result['data'])
            return result
        # 更新数据库
        pwd_face_mapper.update_path_and_name(pwd, pwd_path, pwd_name)
    result['code'] = 200
    result['data'] = '添加成功'
    return result


@blueprint.route('/find_pwd', methods=['POST'])
def find_pwd():
    # 得到参数
    phone = request.form.get("user_phone")
    pwd_type = request.form.get("pwd_type")
    file = request.files.get("pwd_file")

    result = {'code': 403, 'data': '查找失败'}
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "找到密码" + result['data'])
        return result
    user_id = user.id
    if pwd_type == '1':  # 指纹声音模型
        res = fingerprint.find_name_by_phone(user_id, file)
    else:  # 人脸模型
        res = face.find_name_by_phone(user_id, file)
    if res is not None:
        result['code'] = 200
        result['data'] = '查找成功'
        result['name'] = res
        return result
    error_log_mapper.add_error(phone + "找到密码" + result['data'])
    return result


@blueprint.route('/get_pwd', methods=['POST'])
def get_pwd():
    phone = request.form.get("user_phone")
    pwd_type = request.form.get("pwd_type")
    result = {'code': 403, 'data': '查找失败'}
    # 查询用户
    user = user_mapper.find_user_by_phone(phone)
    if user is None:
        result['code'] = 404
        result['data'] = '用户不存在'
        error_log_mapper.add_error(phone + "获取密码" + result['data'])
        return result
    user_id = user.id

    if pwd_type == '1':  # 指纹声音模型
        res = pwd_fingerprint_mapper.get_pwd(user_id)
    else:
        res = pwd_face_mapper.get_pwd(user_id)
    if res is None:
        result['code'] = 404
        result['data'] = '密码不存在'
        error_log_mapper.add_error(phone + "获取密码" + result['data'])
    else:
        result['code'] = 200
        result['data'] = '查找成功'
        result['msg'] = res
        return result
    error_log_mapper.add_error(phone + "获取密码" + result['data'])
    return result
