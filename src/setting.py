# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:38
# @Author : 曾佳宝
# @File : setting.py
# @Software : PyCharm

SERVER_PORT = 8081
DEBUG = True
HOST = '1.15.114.189'
PORT = '3306'
DATABASE = 'sapas'
USERNAME = 'remote'
PASSWORD = '123456'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    db=DATABASE
)

SQLALCHEMY_ENCODING = "utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
