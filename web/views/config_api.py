#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
返回Config表中的数据的API
"""

__author__ = 'LiTian'

from flask import Blueprint
from web.tools.output_config_api import make_config_dict
from web.tools.aes import MyAES
from web import app


mod = Blueprint('configapi', __name__, url_prefix='/config_api')


@mod.route('/')
def re_config_all():
    """返回加密后的全部config表信息"""
    aes = MyAES(app.config['AES_KEY'], app.config['AES_IV'])
    return aes.my_encrypt(str(make_config_dict()))


@mod.route('/<int:config_id>')
def re_config_one(config_id):
    """返回加密后的单个config表信息"""
    try:
        config_dict = make_config_dict(config_id)
    except Exception as e:
        return str(e)
    aes = MyAES(app.config['AES_KEY'], app.config['AES_IV'])
    return aes.my_encrypt(str(config_dict))
