#!usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__)
app.config.from_object(__name__)

# flask-sqlalchemy的数据库配置
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/cluster_man?charset=utf8'

app.config.update(dict(
    SECRET_KEY='myt1@session0#key',
))
# flask配置文件（没有也不报错）
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=True)
    create_date = db.Column(db.DATETIME, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<Email %r>' % self.email


_re_email = re.compile(r'^(\w)+(\.\w)*@(\w)+((\.\w{2,3}){1,3})$')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        if not email or not _re_email.match(email):
            error = 'Invalid email'
        elif not password or len(password) > 50:
            error = 'Invalid password'
        else:
            new_use = Users(email=email, password=password, create_date=datetime.now())
            db.session.add(new_use)
            db.session.commit()
            flash('Signup complete!')
            # 设置 cookie 保存登陆信息
            response = make_response()
            response.set_cookie('email', email, max_age=21600)
            return redirect(url_for('index'))
    return render_template('signup.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


if __name__ == '__main__':
    # 删除全部表，创建全部表
    # db.drop_all()
    # db.create_all()
    app.run()