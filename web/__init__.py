#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建flask对象
"""

from flask import Flask
from .models import db
from config import configs

app = Flask(__name__)
# flask config
app.config.from_object(configs['default'])

# flask-sqlalchemy的数据库配置
db.init_app(app)


# 加载 blueprint 进 app
from web.views import config_tool, user_control, general, config_api, monitor
app.register_blueprint(config_tool.mod)
app.register_blueprint(user_control.mod)
app.register_blueprint(general.mod)
app.register_blueprint(config_api.mod)
app.register_blueprint(monitor.mod)
