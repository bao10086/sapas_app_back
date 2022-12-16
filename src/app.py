# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:37
# @Author : 曾佳宝
# @File : app.py
# @Software : PyCharm

from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import pymysql


class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)
        self.config.from_pyfile('setting.py')

        db.init_app(self)


pymysql.install_as_MySQLdb()
db = SQLAlchemy()
app = Application(__name__)
manager = Manager(app)
