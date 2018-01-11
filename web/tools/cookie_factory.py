#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
制作、解释、验证cookie
验证是否admin用户
重建数据库
"""

__author__ = 'LiTian'


import hashlib
import logging
import functools
from datetime import datetime
from flask import render_template
from web import app
from web.models import db, Users


def user2cookie(key, user):
    """根据user对象，制作cookie"""
    st = '%s^%s^%s' % (user.UserName, user.Password, key)
    li = [user.UserName, hashlib.sha1(st.encode('utf-8')).hexdigest()]
    return '^'.join(li)


def cookie2user(key, cookie):
    """解释cookie，返回user对象"""
    if not cookie:
        return None
    try:
        li = cookie.split('^')
        if len(li) != 2:
            print('invalid cookie length')
            return None
        username, sha1 = li
        user = Users.query.filter_by(UserName=username).first()
        if not user:
            print('invalid cookie user')
            return None
        st = '%s^%s^%s' % (user.UserName, user.Password, key)
        if sha1 != hashlib.sha1(st.encode('utf-8')).hexdigest():
            print('invalid cookie sha1')
            return None
        return user
    except Exception as e:
        logging.exception(e)
        return None


def check_user_cookie(re):
    """装饰器,用cookie来检查用户登录，每次request都检查"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*arg, **kw):
            db.session.remove()  # 清理flask_sqlalchemy缓存,不清理的话，会导致新加入的数据不能查询出来
            cookie = re.cookies.get(app.config['COOKIE_NAME'])
            agree = cookie2user(app.config['COOKIE_NAME'], cookie)
            if not agree:
                return render_template('user/login.html', error='登录已过期或用户信息已更改，请重新登录！')
            return func(*arg, **kw)
        return wrapper
    return decorator


def check_admin(re):
    """装饰器,跟check_user_cookie大致相同，但增加用cookie来检查权限"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*arg, **kw):
            cookie = re.cookies.get(app.config['COOKIE_NAME'])
            agree = cookie2user(app.config['COOKIE_NAME'], cookie)
            if not agree:
                return render_template('user/login.html', error='登录已过期或用户信息已更改，请重新登录！')
            elif agree.UserName != 'admin':
                return render_template('user/login.html', error='用户权限不足')
            return func(*arg, **kw)
        return wrapper
    return decorator


def recreate_database_and_admin(app, admin_password='123456', delect_table=False):
    """重建数据库和新建管理员"""
    if delect_table is True:
        db.drop_all(app=app)
    db.create_all(app=app)
    sha1_password = '%s:%s:%s' % ('admin', admin_password, app.config['SALT'])
    last_password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
    new_use = Users(UserName='admin', Password=last_password, CreateDate=datetime.now())
    with app.app_context():
        db.session.add(new_use)
        db.session.commit()
