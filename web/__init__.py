#!usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from models import db

app = Flask(__name__)
# flask-sqlalchemy的数据库配置
db.init_app(app)

# flask config
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='myt1@session0#key',
    SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost:3306/cluster_man?charset=utf8',
    COOKIE_NAME='YunrunClusterManagerSessionName',
    SALT='add@2some#t6salts!',
))
# # flask config 文件（没有也不警告）
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from web.views import config_tool, user_control
app.register_blueprint(config_tool.mod)
app.register_blueprint(user_control.mod)

