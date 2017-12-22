#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
处理主页等一些常规性url处理
"""

from flask import Blueprint, render_template, request
from tools import check_user_cookie

mod = Blueprint('general', __name__)


@mod.route('/')
@check_user_cookie(request)
def index():
    return render_template('index.html')
