#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
网页主程序
"""

__author__ = 'LiTian'

import re
import hashlib
from flask import Flask, request, g, redirect, url_for, abort, render_template, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from web.cookie_factory import cookie2user, user2cookie

app = Flask(__name__)
# flask-sqlalchemy的数据库配置
db = SQLAlchemy(app)

# flask config
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='myt1@session0#key',
    SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost:3306/cluster_man?charset=utf8',
    COOKIE_NAME='YunrunClusterManagerSessionName',
))
# flask config 文件（没有也不警告）
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# 模板
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=True)
    create_date = db.Column(db.DATETIME, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<Email %r>' % self.email


_re_email = re.compile(r'^(\w)+(\.\w)*@(\w)+((\.\w{2,3}){1,3})$')


# 装饰器,检查cookie
def check_user_cookie(re):
    def decorator(func):
        def wrapper(*arg, **kw):
            cookie = re.cookies.get(app.config['COOKIE_NAME'])
            user = cookie2user(app.config['COOKIE_NAME'], Users, cookie)
            if not user:
                return render_template('login.html', error='Login expired, please login again!')
            return func(*arg, **kw)
        return wrapper
    return decorator


@app.route('/')
@check_user_cookie(request)
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        em = Users.query.filter_by(email=email).first()
        if not email or not _re_email.match(email):
            error = 'Invalid email'
        elif not password or len(password) > 50:
            error = 'Invalid password'
        elif em:
            error = 'Email is exist'
        else:
            # 加密password
            sha1_password = '%s:%s:%s' % (email, password, 'add@2some#t6salts!')
            last_password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
            new_use = Users(email=email, password=last_password, create_date=datetime.now())
            db.session.add(new_use)
            db.session.commit()
            flash('Signup complete!')
            # 设置 cookie 保存登陆信息
            response = make_response(redirect(url_for('index')))
            response.set_cookie(app.config['COOKIE_NAME'], user2cookie(app.config['COOKIE_NAME'], new_use), max_age=21600)
            new_use.password = '******'
            return response
    return render_template('signup.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        if not email or not password:
            error = 'Null email or password!'
            return render_template('login.html', error=error)
        user = Users.query.filter_by(email=email).first()
        if not user:
            error = 'Email not exist!'
            return render_template('login.html', error=error)
        email_password_key = '%s:%s:%s' % (email, password, 'add@2some#t6salts!')
        sha1_password = hashlib.sha1(email_password_key.encode('utf-8')).hexdigest()
        if sha1_password != user.password:
            error = 'Invalid password '
            return render_template('login.html', error=error)
        # 设置 cookie 保存登陆信息
        response = make_response(render_template('index.html'))
        response.set_cookie(app.config['COOKIE_NAME'], user2cookie(app.config['COOKIE_NAME'], user), max_age=21600)
        user.password = '******'
        return response
    return render_template('login.html')


@app.route('/logout')
def logout():
    response = make_response(render_template('login.html'))
    response.delete_cookie(app.config['COOKIE_NAME'])
    return response


if __name__ == '__main__':
    app.run()
