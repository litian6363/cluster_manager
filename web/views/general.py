#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
处理主页等一些通用路由处理
"""

__author__ = 'LiTian'

from flask import Blueprint, render_template, request
from web.tools.cookie_factory import check_user_cookie


mod = Blueprint('general', __name__)


@mod.route('/')
@check_user_cookie(request)
def index():
    """主页"""
    return render_template('index.html')
