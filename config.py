#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""配置文件"""

__author__ = 'LiTian'


class Config(object):
    """默认配置"""
    DEBUG = False
    SECRET_KEY = 'myt1@session0#key'  # flask session key，越复杂越好
    #  sqlalchemy数据映射（ORM）数据库配置，mysql格式：'mysql://用户名:用户密码@地址:端口/数据库名?charset=编码'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/cluster_man?charset=utf8'
    COOKIE_NAME = 'YunrunClusterManagerSessionName'
    SALT = 'add@2some#t6salts!'  # 数据库加密用到的salt
    AES_KEY = 'Test8AES8KEY8123'  # AES加密，key和iv长度必须是( 16,24,32 )其中之一
    AES_IV = 'Test8AES8IV81234'
    SQLALCHEMY_BINDS = {  # 多数据库设置
        'cluster_user': 'mysql://root:root@localhost:3306/cluster_user?charset=utf8'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 生产部署时要关闭


class ProductionConfig(Config):
    """生产配置"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """开发配置"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


configs = {
    'default': Config,
    'production': ProductionConfig,
    'development': DevelopmentConfig
}
