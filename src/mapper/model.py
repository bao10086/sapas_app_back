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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(11), primary_key=True)
    password = db.Column(db.String(20), nullable=False)


# ==============================================================
#  Table: ClassicProblem
# ==============================================================
class ClassicProblem(db.Model):
    __tablename__ = 'classic_problem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(200), nullable=False)


# ==============================================================
#  Table: Feedback
# ==============================================================
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False)
    info = db.Column(db.Text, nullable=False)
    is_solve = db.Column(db.Boolean, nullable=False)
    admin_feedback = db.Column(db.String(200))
    admin_feedback_time = db.Column(db.TIMESTAMP)
    delete = db.Column(db.Integer)


# ==============================================================
#  Table: LogError
# ==============================================================
class LogError(db.Model):
    __tablename__ = 'log_error'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.TIMESTAMP, nullable=False)
    info = db.Column(db.Text, nullable=False)
    delete = db.Column(db.Integer)


# ==============================================================
#  Table: LogLogin
# ==============================================================
class LogLogin(db.Model):
    __tablename__ = 'log_login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    device = db.Column(db.String(50), nullable=False)
    delete = db.Column(db.Integer)


# ==============================================================
#  Table: ModelFace
# ==============================================================
class ModelFace(db.Model):
    __tablename__ = 'model_face'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    upload_time = db.Column(db.TIMESTAMP, nullable=False)
    used = db.Column(db.Integer, nullable=False)
    delete = db.Column(db.Integer)


# ==============================================================
#  Table: ModelFingerprint
# ==============================================================
class ModelFingerprint(db.Model):
    __tablename__ = 'model_fingerprint'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    update_time = db.Column(db.TIMESTAMP)
    delete = db.Column(db.Integer)


# ==============================================================
#  Table: Notice
# ==============================================================
class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    user_ids = db.Column(db.Text)
    time = db.Column(db.TIMESTAMP)
    title = db.Column(db.String(255))


# ==============================================================
#  Table: Permissions
# ==============================================================
class Permissions(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)


# ==============================================================
#  Table: PwdFace
# ==============================================================
class PwdFace(db.Model):
    __tablename__ = 'pwd_face'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    delete = db.Column(db.Integer)


# ==============================================================
#  Table: PwdFingerprint
# ==============================================================
class PwdFingerprint(db.Model):
    __tablename__ = 'pwd_fingerprint'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    delete = db.Column(db.Integer)


# ==============================================================
#  Table: Role
# ==============================================================
class Role(db.Model):
    __tablename__ = 'role'
    name = db.Column(db.String(20), nullable=False)
    id = db.Column(db.Integer, primary_key=True, nullable=False)


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
    phone = db.Column(db.String(11), nullable=False)
    DOB = db.Column(db.Date)
    sex = db.Column(db.SmallInteger)
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    district = db.Column(db.String(50))
    register_time = db.Column(db.Date)
    image_path = db.Column(db.String(500))
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fingerprint_model_id = db.Column(db.Integer, db.ForeignKey("model_fingerprint.fingerprint_model_id",
                                                               ondelete='CASCADE'), nullable=False)
    delete = db.Column(db.Integer)


# ==============================================================
#  Table: UserRole
# ==============================================================
class UserRole(db.Model):
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id", ondelete='CASCADE'), primary_key=True, nullable=False)
