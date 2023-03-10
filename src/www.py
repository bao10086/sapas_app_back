# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:39
# @Author : 曾佳宝
# @File : www.py
# @Software : PyCharm

# HTTP模块相关初始化
from src.app import app
from src.controller import feedback
from src.controller import login
from src.controller import login_log
from src.controller import notice
from src.controller import pwd
from src.controller import register
from src.controller import user_information

app.register_blueprint(login.blueprint)
app.register_blueprint(register.blueprint)
app.register_blueprint(pwd.blueprint)
app.register_blueprint(user_information.blueprint)
app.register_blueprint(feedback.blueprint)
app.register_blueprint(login_log.blueprint)
app.register_blueprint(notice.blueprint)
