#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
处理用户注册登录等等有关用户信息的url
"""

import hashlib
from datetime import datetime
from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for
from web.tools import user2cookie, check_user_cookie, check_admin
from web.models import Users, db
from web import app

mod = Blueprint('user', __name__, url_prefix='/user')


@mod.route('/signup', methods=['GET', 'POST'])
@check_admin(request)
def signup():
    """用户注册"""
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
            flash('注册成功！')
            # 设置 cookie 保存登陆信息
            response = make_response(redirect('/'))
            response.set_cookie(app.config['COOKIE_NAME'], user2cookie(app.config['COOKIE_NAME'], new_use), max_age=21600)
            new_use.Password = '******'
            return response
    return render_template('user/signup.html', error=error)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            error = '空的用户名或密码'
            return render_template('user/login.html', error=error)
        user = Users.query.filter_by(UserName=username).first()
        if not user:
            error = '用户不存在'
            return render_template('user/login.html', error=error)
        username_password_key = '%s:%s:%s' % (username, password, app.config['SALT'])
        sha1_password = hashlib.sha1(username_password_key.encode('utf-8')).hexdigest()
        if sha1_password != user.Password:
            error = '无效的密码'
            return render_template('user/login.html', error=error)
        # 设置 cookie 保存登陆信息
        response = make_response(redirect('/'))
        response.set_cookie(app.config['COOKIE_NAME'], user2cookie(app.config['COOKIE_NAME'], user), max_age=21600)
        flash('登录成功！')
        return response
    return render_template('user/login.html')


@mod.route('/logout')
def logout():
    """用户登出"""
    response = make_response(redirect(url_for('user.login')))
    response.delete_cookie(app.config['COOKIE_NAME'])
    return response


@mod.route('/manager')
@check_admin(request)
def manager():
    """用户管理"""
    page = request.args.get('page', 1, type=int)
    pagination = Users.query.paginate(page, per_page=10, error_out=False)
    data_list = pagination.items
    return render_template('user/users_manager.html', table=Users, data_list=data_list, pagination=pagination)


@mod.route('/modify/<int:user_id>', methods=['GET'])
@check_admin(request)
def modify(user_id):
    """展示user修改form表单"""
    modify_user = Users.query.filter_by(ID=user_id).first()
    return render_template('user/users_modify.html', item=modify_user)


@mod.route('/modify/', methods=['POST'])
@check_admin(request)
def modify_api():
    """修改用户数据API"""
    users_input_id = request.form.get('UsersInputID')
    users_input_username = request.form.get('UsersInputUserName')
    users_input_password = request.form.get('UsersInputPassword')
    old_user = Users.query.filter_by(ID=users_input_id).first()
    if old_user and users_input_username and users_input_password and'^' not in users_input_username:
        if old_user.UserName == 'admin':
            flash('不要修改admin名字！', category='error')
        else:
            old_user.UserName = users_input_username
        sha1_password = '%s:%s:%s' % (users_input_username, users_input_password, app.config['SALT'])
        last_password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
        old_user.Password = last_password
    else:
        flash('用户名密码不能为空；用户名不能包含<^>字符', category='error')
    try:
        db.session.commit()
        flash('用户更新成功！')
    except Exception as e:
        flash('用户修改失败，错误信息：%s' % e, category='error')
    return redirect(url_for('user.manager'))


@mod.route('/delete/<user_id>')
@check_admin(request)
def delete(user_id):
    """删除数据"""
    delete_item = Users.query.filter_by(ID=user_id).first()
    if delete_item:
        if delete_item.UserName == 'admin':
            flash('不要删除admin...', category='error')
        else:
            try:
                db.session.delete(delete_item)
                db.session.commit()
                flash('删除成功！')
            except Exception as e:
                flash('删除失败，错误信息：%s' % e, category='error')
    return redirect(url_for('user.manager'))
