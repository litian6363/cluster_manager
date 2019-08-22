#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建flask对象
"""

from flask import Flask
from .models import db
from config import configs
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
# 载入配置
app.config.from_object(configs['use'])

# flask-sqlalchemy的数据库配置
db.init_app(app)

# 加载 blueprint 进 app
from web.views import config_tool, user_control, general

app.register_blueprint(config_tool.mod)  # 配置工具
app.register_blueprint(user_control.mod)  # 用户管理
app.register_blueprint(general.mod)  # 通用

# 数据获取接口
# from web.views import config_api
# app.register_blueprint(config_api.mod)

# 监控界面
# from web.views import monitor
# app.register_blueprint(monitor.mod)
