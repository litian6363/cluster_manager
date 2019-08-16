#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""配置文件"""

__author__ = 'LiTian'


class Config(object):
    """默认配置"""
    DEBUG = False
    SECRET_KEY = 'myt1@session0#key'  # flask session key，越复杂越好
    #  sqlalchemy数据映射（ORM）数据库配置，mysql格式：'mysql://用户名:用户密码@地址:端口/数据库名?charset=编码'
    SQLALCHEMY_DATABASE_URI = 'mysql://travis@127.0.0.1:3306/cluster?charset=utf8'
    COOKIE_NAME = 'YunrunClusterManagerSessionName'
    SALT = 'add@2some#t6salts!'  # 数据库加密用到的salt
    AES_KEY = 'Test8AES8KEY8123'  # AES加密，key和iv长度必须是( 16,24,32 )其中之一
    AES_IV = 'Test8AES8IV81234'
    SQLALCHEMY_BINDS = {  # 多数据库设置
        'cluster_user': 'mysql://travis@127.0.0.1:3306/cluster_user?charset=utf8'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 跟踪对象修改，生产部署时要关闭
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_timeout': 3}  # 连接池超时秒数


class ProductionConfig(Config):
    """生产配置"""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """开发配置"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


# 在这里选启用那个配置
configs = {
    'use': DevelopmentConfig
}
