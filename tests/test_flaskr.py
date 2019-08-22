#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/15 14:28 
# @File : test_flaskr.py
# @Software: PyCharm
# @Author : LiTian

import pytest
from web import app


@pytest.fixture()
def myt_client():
    app.config['TESTING'] = True
    app.app_context().push()
    with app.test_client() as client:
        yield client


def test_index(myt_client):
    rv = myt_client.get('/')
    assert bytes('聚类管理系统', encoding='utf-8') in rv.data


def test_user(myt_client):
    from web.tools.cookie_factory import recreate_database_and_admin
    recreate_database_and_admin(app, admin_password='123456', delect_table=True)  # 重建数据库和创建管理员
    rv = myt_client.post('/user/login', data={'username': 'root', 'password': '123456'}, follow_redirects=True)
    print(rv.data)
    assert rv.status_code == 200


if __name__ == '__main__':
    with app.test_client() as client:
        rv = client.get('/')
        print(rv)
