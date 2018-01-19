#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""配置文件"""

__author__ = 'LiTian'

class Config(object):
    DEBUG = False
    SECRET_KEY = 'myt1@session0#key'
    #  sqlalchemy数据映射（ORM）数据库配置，mysql格式：'mysql://用户名:用户密码@地址:端口/数据库名?charset=编码'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/cluster_man?charset=utf8'
    COOKIE_NAME = 'YunrunClusterManagerSessionName'
    SALT = 'add@2some#t6salts!'
    AES_KEY = 'Test AES KEY 123'  # key和iv长度必须是16，24，32
    AES_IV = 'Test AES IV 1234'
    SQLALCHEMY_BINDS={  # 多数据库设置
        'cluster_user': 'mysql://root:root@localhost:3306/cluster_user?charset=utf8'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True


configs = {
    'default': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestingConfig,
}
