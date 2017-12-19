#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
网页主程序
"""

__author__ = 'LiTian'

import hashlib
import functools
from flask import Flask, request, g, redirect, url_for, abort, render_template, flash, make_response
from datetime import datetime
from web.cookie_factory import cookie2user, user2cookie
from web.extension_db import db
from web.models import Users, Config, DB, Kafka, KafkaHost, Program, SSDB


app = Flask(__name__)
# flask-sqlalchemy的数据库配置
db.init_app(app)

# flask config
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='myt1@session0#key',
    SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost:3306/cluster_man?charset=utf8',
    COOKIE_NAME='YunrunClusterManagerSessionName',
    SALT='add@2some#t6salts!',
))
# flask config 文件（没有也不警告）
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def check_user_cookie(re):
    """装饰器,用cookie来检查用户登录，每次request都检查"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*arg, **kw):
            cookie = re.cookies.get(app.config['COOKIE_NAME'])
            agree = cookie2user(app.config['COOKIE_NAME'], Users, cookie)
            if not agree:
                return render_template('login.html', error='未登陆或登陆已过期，请重新登陆！')
            return func(*arg, **kw)
        return wrapper
    return decorator


@app.route('/')
@check_user_cookie(request)
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
@check_user_cookie(request)
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        em = Users.query.filter_by(UserName=username).first()
        if not username or len(username) > 50 or '^' in username:
            error = '无效的用户名'
        elif not password or len(password) > 50:
            error = '无效的密码'
        elif em:
            error = '用户已存在'
        else:
            # 加密password
            sha1_password = '%s:%s:%s' % (username, password, app.config['SALT'])
            last_password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
            new_use = Users(UserName=username, Password=last_password, CreateDate=datetime.now())
            db.session.add(new_use)
            db.session.commit()
            flash('Signup complete!')
            # 设置 cookie 保存登陆信息
            response = make_response(redirect('/'))
            response.set_cookie(app.config['COOKIE_NAME'], user2cookie(app.config['COOKIE_NAME'], new_use), max_age=21600)
            new_use.Password = '******'
            return response
    return render_template('signup.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            error = '空的用户名或密码'
            return render_template('login.html', error=error)
        user = Users.query.filter_by(UserName=username).first()
        if not user:
            error = '用户不存在'
            return render_template('login.html', error=error)
        username_password_key = '%s:%s:%s' % (username, password, app.config['SALT'])
        sha1_password = hashlib.sha1(username_password_key.encode('utf-8')).hexdigest()
        if sha1_password != user.Password:
            error = '无效的密码'
            return render_template('login.html', error=error)
        # 设置 cookie 保存登陆信息
        response = make_response(redirect('/'))
        response.set_cookie(app.config['COOKIE_NAME'], user2cookie(app.config['COOKIE_NAME'], user), max_age=21600)
        user.Password = '******'
        return response
    return render_template('login.html')


@app.route('/logout')
def logout():
    response = make_response(redirect('login'))
    response.delete_cookie(app.config['COOKIE_NAME'])
    return response


tables = {'Config': Config, 'DB': DB, 'Kafka': Kafka, 'KafkaHost': KafkaHost, 'Program': Program, 'SSDB': SSDB, 'Users':Users}


@app.route('/configtool/', defaults={'table': 'Config'})
@app.route('/configtool/<table>')
@check_user_cookie(request)
def config_tool(table):
    """配置工具view"""
    if table not in tables:
        abort(401)
    data_list = tables[table].query.all()
    return render_template('config_tool/%s.html' % table, table=table, data_list=data_list)


@app.route('/configtool/<table>/add', methods=['GET'])
@check_user_cookie(request)
def config_add(table):
    """新增配置GET request 处理"""
    if table == 'Kafka':
        return render_template('config_tool_modify/%s.html' % table, table=table, kafkahost_all=KafkaHost.query.all())
    elif table == 'Config':
        five_table = {'DB': DB.query.all(), 'KafkaHost': KafkaHost.query.all(), 'Kafka': Kafka.query.all(),
                      'Program': Program.query.all(), 'SSDB': SSDB.query.all()}
        return render_template('config_tool_modify/%s.html' % table, table=table, five_table=five_table)
    else:
        return render_template('config_tool_modify/%s.html' % table, table=table)


@app.route('/configtool/<table>/add', methods=['POST'])
@check_user_cookie(request)
def config_add_api(table):
    """新增或修改配置API POST request 处理"""
    if table not in tables:
        abort(401)
    elif table == 'Config':
        ConfigInputID = request.form.get('ConfigInputID')
        ConfigInputDBID = request.form.get('ConfigInputDBID')
        ConfigInputKafkaHostID = request.form.get('ConfigInputKafkaHostID')
        ConfigInputKafkaID = request.form.get('ConfigInputKafkaID')
        ConfigInputProgramID = request.form.get('ConfigInputProgramID')
        ConfigInputSSDBID = request.form.get('ConfigInputSSDBID')
        ConfigInputSign = request.form.get('ConfigInputSign')
        old_config = Config.query.filter_by(ID=ConfigInputID).first()
        if old_config:  # 如果表中已有这个ID，则是修改
            old_config.DBID = ConfigInputDBID
            old_config.KafkaHostID = ConfigInputKafkaHostID
            old_config.KafkaID = ConfigInputKafkaID
            old_config.ProgramID = ConfigInputProgramID
            old_config.SSDBID = ConfigInputSSDBID
            old_config.Sign = ConfigInputSign
        else:  # 否则就是新增
            new_config = Config(DBID=ConfigInputDBID, KafkaHostID=ConfigInputKafkaHostID,
                                KafkaID=ConfigInputKafkaID, ProgramID=ConfigInputProgramID,
                                SSDBID=ConfigInputSSDBID, Sign=ConfigInputSign)
            db.session.add(new_config)
        db.session.commit()

    elif table == 'DB':
        DBInputID = request.form.get('DBInputID')
        DBInputLANIP = request.form.get('DBInputLANIP')
        DBInputIP = request.form.get('DBInputIP')
        DBInputUser = request.form.get('DBInputUser')
        DBInputPassword = request.form.get('DBInputPassword')
        old_db = DB.query.filter_by(ID=DBInputID).first()
        if old_db:
            old_db.LANIP = DBInputLANIP
            old_db.IP = DBInputIP
            old_db.User = DBInputUser
            old_db.Password = DBInputPassword
        else:
            new_db = DB(LANIP=DBInputLANIP, IP=DBInputIP, User=DBInputUser, Password=DBInputPassword)
            db.session.add(new_db)
        db.session.commit()

    elif table == 'Kafka':
        KafkaInputID = request.form.get('KafkaInputID')
        KafkaInputHostID = request.form.get('KafkaInputHostID')
        KafkaInputCustomerTopic = request.form.get('KafkaInputCustomerTopic')
        KafkaInputProducerTopic = request.form.get('KafkaInputProducerTopic')
        KafkaInputAnalyzeTopic = request.form.get('KafkaInputAnalyzeTopic')
        KafkaInputGroupName = request.form.get('KafkaInputGroupName')
        KafkaInputAutoCommit = request.form.get('KafkaInputAutoCommit')
        KafkaInputFromBegin = request.form.get('KafkaInputFromBegin')
        KafkaInputDesc = request.form.get('KafkaInputDesc')
        old_kafka = Kafka.query.filter_by(ID=KafkaInputID).first()
        if old_kafka:
            old_kafka.HostID = KafkaInputHostID
            old_kafka.CustomerTopic = KafkaInputCustomerTopic
            old_kafka.ProducerTopic = KafkaInputProducerTopic
            old_kafka.AnalyzeTopic = KafkaInputAnalyzeTopic
            old_kafka.GroupName = KafkaInputGroupName
            old_kafka.AutoCommit = KafkaInputAutoCommit
            old_kafka.FromBegin = KafkaInputFromBegin
            old_kafka.Desc = KafkaInputDesc
        else:
            new_kafka = Kafka(HostID=KafkaInputHostID, CustomerTopic=KafkaInputCustomerTopic,
                              ProducerTopic=KafkaInputProducerTopic, AnalyzeTopic=KafkaInputAnalyzeTopic,
                              GroupName=KafkaInputGroupName, AutoCommit=KafkaInputAutoCommit,
                              FromBegin=KafkaInputFromBegin, Desc=KafkaInputDesc, Addon=datetime.now())
            db.session.add(new_kafka)
        db.session.commit()

    elif table == 'KafkaHost':
        KafkahostInputID = request.form.get('KafakahostInputID')
        KafkahostInputHost = request.form.get('KafakahostInputHost')
        KafkahostInputDesc = request.form.get('KafakahostInputDesc')
        old_kafkahost = KafkaHost.query.filter_by(ID=KafkahostInputID).first()
        if old_kafkahost:
            old_kafkahost.Host = KafkahostInputHost
            old_kafkahost.Desc = KafkahostInputDesc
        else:
            new_kafkahost = KafkaHost(Host=KafkahostInputHost, Desc=KafkahostInputDesc, Addon=datetime.now())
            db.session.add(new_kafkahost)
        db.session.commit()

    elif table == 'Program':
        ProgramInputID = request.form.get('ProgramInputID')
        ProgramInputMaxKwsCount = request.form.get('ProgramInputMaxKwsCount')
        ProgramInputMaxEntityCount = request.form.get('ProgramInputMaxEntityCount')
        ProgramInputExpired = request.form.get('ProgramInputExpired')
        ProgramInputSSDBExpired = request.form.get('ProgramInputSSDBExpired')
        ProgramInputDesc = request.form.get('ProgramInputDesc')
        old_program = Program.query.filter_by(ID=ProgramInputID).first()
        if old_program:
            old_program.MaxKwsCount = ProgramInputMaxKwsCount
            old_program.MaxEntityCount = ProgramInputMaxEntityCount
            old_program.Expired = ProgramInputExpired
            old_program.SSDBExpired = ProgramInputSSDBExpired
            old_program.Desc = ProgramInputDesc
        else:
            new_program = Program(MaxKwsCount=ProgramInputMaxKwsCount, MaxEntityCount=ProgramInputMaxEntityCount,
                                  Expired=ProgramInputExpired, SSDBExpired=ProgramInputSSDBExpired,
                                  Desc=ProgramInputDesc, Addon=datetime.now())
            db.session.add(new_program)
        db.session.commit()
        return redirect(url_for('config_tool', table=table))

    elif table == 'SSDB':
        SSDBInputID = request.form.get('SSDBInputID')
        SSDBInputLANIP = request.form.get('SSDBInputLANIP')
        SSDBInputDesc = request.form.get('SSDBInputDesc')
        old_ssdb = SSDB.query.filter_by(ID=SSDBInputID).first()
        if old_ssdb:
            old_ssdb.LANIP = SSDBInputLANIP
            old_ssdb.Desc = SSDBInputDesc
        else:
            new_ssdb = SSDB(LANIP=SSDBInputLANIP, Desc=SSDBInputDesc, Addon=datetime.now())
            db.session.add(new_ssdb)
        db.session.commit()
    return redirect(url_for('config_tool', table=table))


def recreate_database_and_admin(app, admin_password):
    """重建数据库和管理员"""
    db.drop_all(app=app)
    db.create_all(app=app)
    sha1_password = '%s:%s:%s' % ('admin', admin_password, app.config['SALT'])
    last_password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
    new_use = Users(UserName='admin', Password=last_password, CreateDate=datetime.now())
    with app.app_context():
        db.session.add(new_use)
        db.session.commit()


if __name__ == '__main__':
    # recreate_database_and_admin(app, '123456')  # 重建数据库然后创建管理员（第一次搭建时用）
    app.run()
