# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:11
# @Author : 曾佳宝
# @File : model.py
# @Software : PyCharm

from src.app import db


# ==============================================================
#  Table: Admin
# ==============================================================
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_account = db.Column(db.String(11), primary_key=True)
    admin_password = db.Column(db.String(20), nullable=False)
    admin_name = db.Column(db.String(20))
    admin_image_path = db.Column(db.String(50), nullable=False)


# ==============================================================
#  Table: ClassicProblem
# ==============================================================
class ClassicProblem(db.Model):
    __tablename__ = 'classic_problem'
    classic_problem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_problem_type = db.Column(db.String(200), nullable=False)


# ==============================================================
#  Table: Feedback
# ==============================================================
class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    feedback_time = db.Column(db.TIMESTAMP, nullable=False)
    feedback_info = db.Column(db.Text, nullable=False)
    feedback_is_solve = db.Column(db.Boolean, nullable=False)
    admin_feedback = db.Column(db.String(200))
    admin_feedback_time = db.Column(db.TIMESTAMP)


# ==============================================================
#  Table: LogError
# ==============================================================
class LogError(db.Model):
    __tablename__ = 'log_error'
    error_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    error_time = db.Column(db.TIMESTAMP, nullable=False)
    error_info = db.Column(db.Text, nullable=False)


# ==============================================================
#  Table: LogLogin
# ==============================================================
class LogLogin(db.Model):
    __tablename__ = 'log_login'
    login_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    login_time = db.Column(db.TIMESTAMP, nullable=False)
    login_address = db.Column(db.String(50), nullable=False)
    login_device = db.Column(db.String(50), nullable=False)


# ==============================================================
#  Table: ModelFace
# ==============================================================
class ModelFace(db.Model):
    __tablename__ = 'model_face'
    face_model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    face_model_name = db.Column(db.String(20), nullable=False)
    face_model_path = db.Column(db.String(50), nullable=False)
    face_model_update_time = db.Column(db.Date)


# ==============================================================
#  Table: ModelFingerprint
# ==============================================================
class ModelFingerprint(db.Model):
    __tablename__ = 'model_fingerprint'
    fingerprint_model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    fingerprint_model_name = db.Column(db.String(20), nullable=False)
    fingerprint_model_model_path = db.Column(db.String(50), nullable=False)
    fingerprint_model_update_time = db.Column(db.Date)


# ==============================================================
#  Table: Notice
# ==============================================================
class Notice(db.Model):
    __tablename__ = 'notice'
    notice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notice_info = db.Column(db.Text, nullable=False)
    user_ids = db.Column(db.Text, nullable=False)
    notice_time = db.Column(db.TIMESTAMP, nullable=False)
    notice_title = db.Column(db.String(255), nullable=False)


# ==============================================================
#  Table: Permissions
# ==============================================================
class Permissions(db.Model):
    __tablename__ = 'permissions'
    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(20), nullable=False)


# ==============================================================
#  Table: PwdFace
# ==============================================================
class PwdFace(db.Model):
    __tablename__ = 'pwd_face'
    face_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    face_name = db.Column(db.String(20), nullable=False)
    face_image_path = db.Column(db.String(50), nullable=False)


# ==============================================================
#  Table: PwdFingerprint
# ==============================================================
class PwdFingerprint(db.Model):
    __tablename__ = 'pwd_fingerprint'
    fingerprint_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    fingerprint_name = db.Column(db.String(20), nullable=False)
    fingerprint_path = db.Column(db.String(50), nullable=False)


# ==============================================================
#  Table: Role
# ==============================================================
class Role(db.Model):
    __tablename__ = 'role'
    role_name = db.Column(db.String(20), nullable=False)
    role_id = db.Column(db.Integer, primary_key=True, nullable=False)


# ==============================================================
#  Table: RolePermission
# ==============================================================
class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id", ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.permission_id", ondelete='CASCADE'),
                              primary_key=True)


# ==============================================================
#  Table: User
# ==============================================================
class User(db.Model):
    __tablename__ = 'user'
    user_phone = db.Column(db.String(11), nullable=False)
    user_DOB = db.Column(db.Date)
    user_sex = db.Column(db.SmallInteger)
    user_province = db.Column(db.String(50))
    user_city = db.Column(db.String(50))
    user_district = db.Column(db.String(50))
    user_register_time = db.Column(db.Date)
    user_image_path = db.Column(db.String(50))
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    fingerprint_model_id = db.Column(db.Integer, db.ForeignKey("model_fingerprint.fingerprint_model_id",
                                                               ondelete='CASCADE'), nullable=False)


# ==============================================================
#  Table: UserRole
# ==============================================================
class UserRole(db.Model):
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id", ondelete='CASCADE'), primary_key=True, nullable=False)
