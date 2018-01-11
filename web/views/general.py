#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
处理主页等一些常规性url处理
"""

from flask import Blueprint, render_template, request
from web.tools.cookie_factory import check_user_cookie
from web.tools.output_config_api import make_config_dict
from web.tools.aes import MyAES
from web import app

mod = Blueprint('general', __name__)


@mod.route('/')
@check_user_cookie(request)
def index():
    """主页"""
    return render_template('index.html')


@mod.route('/config_api')
def re_config_all():
    """返回加密后的全部config表信息"""
    aes = MyAES(app.config['AES_KEY'], app.config['AES_IV'])
    return aes.my_encrypt(str(make_config_dict()))


@mod.route('/config_api/<int:config_id>')
def re_config_one(config_id):
    """返回加密后的单个config表信息"""
    aes = MyAES(app.config['AES_KEY'], app.config['AES_IV'])
    return aes.my_encrypt(str(make_config_dict(config_id)))
