#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LiTian'

from gevent import monkey
monkey.patch_all()

from web import app

app = app
app.app_context().push()

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 5000
    from web.tools.cookie_factory import recreate_database_and_admin
    recreate_database_and_admin(app, admin_password='123456', delect_table=True)  # 重建数据库和创建管理员

    # 直接运行时，gevent所需，
    from gevent import pywsgi
    server = pywsgi.WSGIServer((ip, port), app)
    print('运行web服务：'+ ip + '：' + str(port))
    server.serve_forever()
