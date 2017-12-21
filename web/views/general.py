#!usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
from cookie_factory import check_user_cookie

mod = Blueprint('general', __name__)


@mod.route('/')
@check_user_cookie(request)
def index():
    return render_template('index.html')
