#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
处理用户注册登录等等有关用户信息的url
"""

__author__ = 'LiTian'

import hashlib
from datetime import datetime
from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for
from web.tools.cookie_factory import user2cookie, check_admin
from web.models import Users, db
from web import app

mod = Blueprint('user', __name__, url_prefix='/user')


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
        username_password_salt = '%s:%s:%s' % (username, password, app.config['SALT'])
        sha1_password = hashlib.sha1(username_password_salt.encode('utf-8')).hexdigest()
        if sha1_password != user.Password:
            error = '无效的密码'
            return render_template('user/login.html', error=error)
        # 设置 cookie 保存登陆信息
        response = make_response(redirect('/'))
        response.set_cookie(app.config['COOKIE_NAME'],
                            user2cookie(app.config['COOKIE_NAME'], user, request.remote_addr),
                            max_age=21600,
                            httponly=True)
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


@mod.route('/signup', methods=['GET'])
@check_admin(request)
def signup():
    """用户注册,展示form表单"""
    return render_template('user/users_modify.html')


@mod.route('/modify/<int:user_id>', methods=['GET'])
@check_admin(request)
def modify(user_id):
    """展示user修改form表单"""
    modify_user = Users.query.filter_by(ID=user_id).first()
    return render_template('user/users_modify.html', item=modify_user)


@mod.route('/modify/', methods=['POST'])
@check_admin(request)
def modify_api():
    """修改或新增用户"""
    users_input_id = request.form.get('UsersInputID').strip()
    users_input_username = request.form.get('UsersInputUserName').strip()
    users_input_password = request.form.get('UsersInputPassword').strip()
    users_input_password_again = request.form.get('UsersInputAgainPassword').strip()

    old_user = Users.query.filter_by(ID=users_input_id).first()
    item = Users(UserName=users_input_username, Password=users_input_password)

    # 验证输入信息
    if not users_input_username or len(users_input_username) > 50 or '^' in users_input_username or ':' in users_input_username:
        flash('无效的用户名', category='error')
        return render_template('user/users_modify.html', item=item)
    elif not users_input_password or len(users_input_password) > 50 or '^' in users_input_password or ':' in users_input_password:
        flash('无效的密码', category='error')
        return render_template('user/users_modify.html', item=item)
    elif users_input_password != users_input_password_again:
        flash('两次密码不相同', category='error')
        return render_template('user/users_modify.html', item=item)
    elif old_user and old_user.UserName == 'admin' and users_input_username != 'admin':  # 拒绝修改admin用户名
        flash('不能修改admin用户名', category='error')
        return render_template('user/users_modify.html', item=item)

    # 加密password
    username_password_salt = '%s:%s:%s' % (users_input_username, users_input_password, app.config['SALT'])
    sha1_password = hashlib.sha1(username_password_salt.encode('utf-8')).hexdigest()

    # 如果存在用户即修改
    if old_user:
        old_user.UserName = users_input_username
        old_user.Password = sha1_password

    # 不存在用户即新增
    else:
        new_use = Users(UserName=users_input_username, Password=sha1_password, CreateDate=datetime.now())
        db.session.add(new_use)

    try:
        db.session.commit()
        flash('用户更新成功！')
    except Exception as e:
        flash('用户更新失败，错误信息：%s' % e, category='error')
        return render_template('user/users_modify.html', item=item)
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

