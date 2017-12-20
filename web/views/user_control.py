#!usr/bin/env python3
# -*- coding: utf-8 -*-


import hashlib
from datetime import datetime
from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for
from web.cookie_factory import user2cookie, check_user_cookie
from web.models import Users, db
# from web.extension_db import db
from web import app

mod = Blueprint('user', __name__)


@mod.route('/')
@check_user_cookie(request)
def index():
    return render_template('index.html')


@mod.route('/signup', methods=['GET', 'POST'])
@check_user_cookie(request)
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        em = Users.query.filter_by(UserName=username).first()
        if not username or len(username) > 50 or '^' in username:
            error = '无效的用户名'
        elif not password or len(password) > 50:
            error = '无效的密码'
        elif em:
            error = '用户已存在'
        else:
            # 加密password
            sha1_password = '%s:%s:%s' % (username, password, app.config['SALT'])
            last_password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
            new_use = Users(UserName=username, Password=last_password, CreateDate=datetime.now())
            db.session.add(new_use)
            db.session.commit()
            flash('Signup complete!')
            # 设置 cookie 保存登陆信息
            response = make_response(redirect(url_for('user.index')))
            response.set_cookie(app.config['COOKIE_NAME'], user2cookie(app.config['COOKIE_NAME'], new_use), max_age=21600)
            new_use.Password = '******'
            return response
    return render_template('signup.html', error=error)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            error = '空的用户名或密码'
            return render_template('login.html', error=error)
        user = Users.query.filter_by(UserName=username).first()
        if not user:
            error = '用户不存在'
            return render_template('login.html', error=error)
        username_password_key = '%s:%s:%s' % (username, password, app.config['SALT'])
        sha1_password = hashlib.sha1(username_password_key.encode('utf-8')).hexdigest()
        if sha1_password != user.Password:
            error = '无效的密码'
            return render_template('login.html', error=error)
        # 设置 cookie 保存登陆信息
        response = make_response(redirect(url_for('user.index')))
        response.set_cookie(app.config['COOKIE_NAME'], user2cookie(app.config['COOKIE_NAME'], user), max_age=21600)
        return response
    return render_template('login.html')


@mod.route('/logout')
def logout():
    response = make_response(redirect(url_for('user.login')))
    response.delete_cookie(app.config['COOKIE_NAME'])
    return response
