#!usr/bin/env python3
# -*- coding: utf-8 -*-

from web import app
from web.cookie_factory import recreate_database_and_admin

if __name__ == '__main__':
    # recreate_database_and_admin(app, admin_password='123456')  # 重建数据库和创建管理员
    app.run(debug=True)
