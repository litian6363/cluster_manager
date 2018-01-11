#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""配置文件"""


class Config(object):
    DEBUG = False
    SECRET_KEY = 'myt1@session0#key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/cluster_man?charset=utf8'
    COOKIE_NAME = 'YunrunClusterManagerSessionName'
    SALT = 'add@2some#t6salts!'
    AES_KEY = 'IamnotaherobutIs'  # key和iv长度必须是16，24，32
    AES_IV = 'ervedwithheroes.'
    SQLALCHEMY_BINDS={  # 多数据库设置
        'cluster_user': 'mysql://root:root@localhost:3306/cluster_user?charset=utf8'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SECRET_KEY = 'myt1@session0#key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/cluster_man?charset=utf8'
    COOKIE_NAME = 'YunrunClusterManagerSessionName'
    SALT = 'add@2some#t6salts!'
    AES_KEY = 'Test AES KEY 123'  # key和iv长度必须是16，24，32
    AES_IV = 'Test AES IV 1234'
    SQLALCHEMY_BINDS={  # 多数据库设置
        'cluster_user': 'mysql://root:root@localhost:3306/cluster_user?charset=utf8'
    }


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
