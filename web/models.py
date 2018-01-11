#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
存放sqlalchemy模型的地方
"""


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def to_dict(self):
    """将查询结果转换成dict"""
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


db.Model.to_dict = to_dict  # 将to_dict()绑定到父类，让下面的模型都可以用到。


class Users(db.Model):
    __bind_key__ = 'cluster_user'
    __tablename__ = 'users'

    ID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    CreateDate = db.Column(db.DATETIME, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<UserName %r>' % self.UserName


class Config(db.Model):
    __tablename__ = 'config'

    ID = db.Column(db.Integer, primary_key=True)
    DBID = db.Column(db.Integer, db.ForeignKey('db.ID'), nullable=False)
    KafkaHostID = db.Column(db.Integer, db.ForeignKey('kafkahost.ID'), nullable=False)
    KafkaID = db.Column(db.Integer, db.ForeignKey('kafka.ID'), nullable=False)
    ProgramID = db.Column(db.Integer, db.ForeignKey('program.ID'), nullable=False)
    SSDBID = db.Column(db.Integer, db.ForeignKey('ssdb.ID'), nullable=False)
    Sign = db.Column(db.String(120), nullable=False)
    Addon = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<Config %r>' % self.Sign


class DB(db.Model):
    __tablename__ = 'db'

    ID = db.Column(db.Integer, primary_key=True)
    LANIP = db.Column(db.String(32), nullable=False)
    IP = db.Column(db.String(32), nullable=False)
    User = db.Column(db.String(16), nullable=False)
    Password = db.Column(db.String(32), nullable=False)
    Addon = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<Database %r>' % self.IP


class Kafka(db.Model):
    __tablename__ = 'kafka'

    ID = db.Column(db.Integer, primary_key=True)
    HostID = db.Column(db.Integer, db.ForeignKey('kafkahost.ID'), nullable=False)
    CustomerTopic = db.Column(db.String(32), nullable=False)
    ProducerTopic = db.Column(db.String(32), nullable=False)
    AnalyzeTopic = db.Column(db.String(32), nullable=False)
    GroupName = db.Column(db.String(32), nullable=False)
    AutoCommit = db.Column(db.Integer, default=0, nullable=False)
    FromBegin = db.Column(db.Integer, default=0, nullable=False)
    Desc = db.Column(db.String(120), nullable=False)
    Addon = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<Kafka %r>' % self.Desc


class KafkaHost(db.Model):
    __tablename__ = 'kafkahost'

    ID = db.Column(db.Integer, primary_key=True)
    Host = db.Column(db.String(200), nullable=False)
    Desc = db.Column(db.String(120), nullable=False)
    Addon = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<KafkaHost %r>' % self.Desc


class Program(db.Model):
    __tablename__ = 'program'

    ID = db.Column(db.Integer, primary_key=True)
    MaxKwsCount = db.Column(db.Integer, nullable=False)
    MaxEntityCount = db.Column(db.Integer, nullable=False)
    Expired = db.Column(db.Integer, nullable=False)
    SSDBExpired = db.Column(db.Integer, nullable=False)
    Desc = db.Column(db.String(120), nullable=False)
    Addon = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<Program %r>' % self.Desc


class SSDB(db.Model):
    __tablename__ = 'ssdb'

    ID = db.Column(db.Integer, primary_key=True)
    LANIP = db.Column(db.String(32), nullable=False)
    Desc = db.Column(db.String(120), nullable=False)
    Addon = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return '<SSDB %r>' % self.Desc

