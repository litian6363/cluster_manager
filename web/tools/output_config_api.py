#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
根据Config表的配置搜索并返回对应的数据
"""

__author__ = 'LiTian'

from web.models import Config, DB, Kafka, KafkaHost, Program, SSDB


def make_config_dict(config_id=None):
    """根据Config表里面的参数，来查询相对应的表和值，并以dict格式来返回"""
    re_dict = {}
    if isinstance(config_id, int):  # 在有提供ID的时候，返回一行数据
        r = Config.query.filter_by(ID=config_id).first()
        if isinstance(r, Config):
            re_dict = {
                'DB': DB.query.filter_by(ID=r.DBID).first().to_dict(),
                'KafkaHost': KafkaHost.query.filter_by(ID=r.KafkaHostID).first().to_dict(),
                'Kafka': Kafka.query.filter_by(ID=r.KafkaID).first().to_dict(),
                'Program': Program.query.filter_by(ID=r.ProgramID).first().to_dict(),
                'SSDB': SSDB.query.filter_by(ID=r.SSDBID).first().to_dict(),
                'Sign': r.Sign,
                'Addon': r.Addon,
            }
        else:
            re_dict = None
    else:  # 没有提供ID的话，返回全部
        for r in Config.query.all():
            row_dict = {
                'DB': DB.query.filter_by(ID=r.DBID).first().to_dict(),
                'KafkaHost': KafkaHost.query.filter_by(ID=r.KafkaHostID).first().to_dict(),
                'Kafka': Kafka.query.filter_by(ID=r.KafkaID).first().to_dict(),
                'Program': Program.query.filter_by(ID=r.ProgramID).first().to_dict(),
                'SSDB': SSDB.query.filter_by(ID=r.SSDBID).first().to_dict(),
                'Sign': r.Sign,
                'Addon': r.Addon,
            }
            re_dict.setdefault(r.ID, row_dict)
    return re_dict

