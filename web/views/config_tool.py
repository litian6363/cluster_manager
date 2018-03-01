#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
处理 配置工具 里面的路由
"""

__author__ = 'LiTian'

from datetime import datetime
from flask import Blueprint, request, render_template, abort, redirect, url_for, flash
from web.models import db, Config, DB, Kafka, KafkaHost, Program, SSDB, Type
from web.tools.cookie_factory import check_user_cookie
from web.tools.aes import MyAES
from web import app

mod = Blueprint('configtool', __name__, url_prefix='/configtool')


tables = {'Config': Config, 'DB': DB, 'Kafka': Kafka, 'KafkaHost': KafkaHost,
          'Program': Program, 'SSDB': SSDB, 'Type': Type}


@mod.route('/<table>')
@check_user_cookie(request)
def config_tool(table):
    """查看配置数据"""
    if table not in tables:
        abort(404)

    page = request.args.get('page', 1, type=int)
    pagination = tables[table].query.paginate(page, per_page=10, error_out=False)
    if table == 'Config':
        data_list = list(map(lambda r: r.to_dict(), pagination.items))  # 将sqlalchemy查询结果转换成dict
        for row in data_list:  # 将ID转换成对应表的sqlalchemy对象，然后将对象转变为dict
            row['DB'] = DB.query.filter_by(ID=row['DBID']).first().to_dict()
            row['KafkaHost'] = KafkaHost.query.filter_by(ID=row['KafkaHostID']).first().to_dict()
            row['Kafka'] = Kafka.query.filter_by(ID=row['KafkaID']).first().to_dict()
            row['Program'] = Program.query.filter_by(ID=row['ProgramID']).first().to_dict()
            row['SSDB'] = SSDB.query.filter_by(ID=row['SSDBID']).first()
            row['HistorySSDB'] = SSDB.query.filter_by(ID=row['HistorySSDBID']).first()
            if row['SSDB']:
                row['SSDB'] = row['SSDB'].to_dict()
            row['Type'] = Type.query.filter_by(ID=row['TypeID']).first().to_dict()
        return render_template('config_tool_view/%s.html' % table, table=table, data_list=data_list, pagination=pagination)

    elif table == 'Kafka':
        data_list = list(map(lambda r: r.to_dict(), pagination.items))  # 将sqlalchemy查询结果转换成dict
        for row in data_list:  # 将ID转换成对应的描述
            row['HostID'] = str(row['HostID']) + ':' + KafkaHost.query.filter_by(ID=row['HostID']).first().Desc
        return render_template('config_tool_view/%s.html' % table, table=table, data_list=data_list,
                               pagination=pagination)

    else:
        data_list = pagination.items
        return render_template('config_tool_view/%s.html' % table, table=table, data_list=data_list, pagination=pagination)


@mod.route('/<table>/add', methods=['GET'])
@check_user_cookie(request)
def config_add(table):
    """新增数据，展示form表单，GET request"""
    if table not in tables:
        abort(404)

    elif table == 'Kafka':
        return render_template('config_tool_modify/%s.html' % table, table=table, kafkahost_all=KafkaHost.query.all())
    elif table == 'Config':
        tables_query = {'DB': DB.query.all(), 'KafkaHost': KafkaHost.query.all(), 'Kafka': Kafka.query.all(),
                      'Program': Program.query.all(), 'SSDB': SSDB.query.all(), 'Type': Type.query.all()}
        return render_template('config_tool_modify/%s.html' % table, table=table, tables_query=tables_query)
    else:
        return render_template('config_tool_modify/%s.html' % table, table=table)


@mod.route('/<table>/delete/<int:item_id>')
@check_user_cookie(request)
def config_delete(table, item_id):
    """删除数据"""
    delete_item = tables[table].query.filter_by(ID=item_id).first()
    if delete_item:
        try:
            db.session.delete(delete_item)
            db.session.commit()
            flash('删除成功！')
        except Exception as e:
            flash('删除失败，错误信息：%s' % e, category='error')
    return redirect(url_for('configtool.config_tool', table=table))


@mod.route('/<table>/<int:item_id>', methods=['GET'])
@check_user_cookie(request)
def config_modify(table, item_id):
    """修改数据，展示form表单"""
    modify_item = tables[table].query.filter_by(ID=item_id).first()
    if table == 'Kafka':
        return render_template('config_tool_modify/%s.html' % table, table=table,
                               kafkahost_all=KafkaHost.query.all(), item=modify_item)
    elif table == 'Config':
        tables_query = {'DB': DB.query.all(), 'KafkaHost': KafkaHost.query.all(), 'Kafka': Kafka.query.all(),
                      'Program': Program.query.all(), 'SSDB': SSDB.query.all(), 'Type': Type.query.all()}
        return render_template('config_tool_modify/%s.html' % table, table=table, tables_query=tables_query, item=modify_item)
    else:
        return render_template('config_tool_modify/%s.html' % table, table=table, item=modify_item)


@mod.route('/<table>/modify', methods=['POST'])
@check_user_cookie(request)
def config_add_api(table):
    """接收和处理新增或修改的form表单，POST request """
    if table not in tables:
        abort(404)
    elif table == 'Config':
        congig_modify()
    elif table == 'DB':
        db_modify()
    elif table == 'Kafka':
        kafka_modify()
    elif table == 'KafkaHost':
        kafkahost_modify()
    elif table == 'Program':
        program_modify()
    elif table == 'SSDB':
        ssdb_modify()
    elif table == 'Type':
        type_modify()
    try:
        db.session.commit()
        flash('数据更新成功！')
    except Exception as e:
        flash('数据更新失败，错误信息：%s' % e, category='error')
    return redirect(url_for('configtool.config_tool', table=table))


def congig_modify():
    """Config表表单处理"""
    ConfigInputID = request.form.get('ConfigInputID')
    ConfigInputDBID = request.form.get('ConfigInputDBID')
    ConfigInputKafkaHostID = request.form.get('ConfigInputKafkaHostID')
    ConfigInputKafkaID = request.form.get('ConfigInputKafkaID')
    ConfigInputProgramID = request.form.get('ConfigInputProgramID')
    ConfigInputSSDBID = request.form.get('ConfigInputSSDBID')
    if not ConfigInputSSDBID:
        ConfigInputSSDBID = None
    ConfigInputHistorySSDBID = request.form.get('ConfigInputHistorySSDBID')
    ConfigInputTypeID = request.form.get('ConfigInputTypeID')
    ConfigInputSign = request.form.get('ConfigInputSign')
    old_config = Config.query.filter_by(ID=ConfigInputID).first()
    if old_config:  # 如果表中已有这个ID，则是修改
        old_config.DBID = ConfigInputDBID
        old_config.KafkaHostID = ConfigInputKafkaHostID
        old_config.KafkaID = ConfigInputKafkaID
        old_config.ProgramID = ConfigInputProgramID
        old_config.TypeID = ConfigInputTypeID
        old_config.SSDBID = ConfigInputSSDBID
        old_config.HistorySSDBID = ConfigInputHistorySSDBID
        old_config.Sign = ConfigInputSign
    else:  # 否则就是新增
        new_config = Config(DBID=ConfigInputDBID, KafkaHostID=ConfigInputKafkaHostID, KafkaID=ConfigInputKafkaID,
                            ProgramID=ConfigInputProgramID, SSDBID=ConfigInputSSDBID, HistorySSDBID=ConfigInputHistorySSDBID, TypeID=ConfigInputTypeID,
                            Sign=ConfigInputSign, Addon=datetime.now())
        db.session.add(new_config)


def db_modify():
    """DB表表单处理"""
    DBInputID = request.form.get('DBInputID')
    DBInputLANIP = request.form.get('DBInputLANIP')
    DBInputIP = request.form.get('DBInputIP')
    DBInputUser = request.form.get('DBInputUser')
    DBInputPassword = request.form.get('DBInputPassword')
    DBInputName = request.form.get('DBInputName')
    # AES加密password
    if DBInputPassword:
        my_aes = MyAES(app.config['AES_KEY'], app.config['AES_IV'])
        aes_DBInputPassword = my_aes.my_encrypt(DBInputPassword)
    DBInputDesc = request.form.get('DBInputDesc')
    old_db = DB.query.filter_by(ID=DBInputID).first()
    if old_db:
        old_db.LANIP = DBInputLANIP
        old_db.IP = DBInputIP
        old_db.User = DBInputUser
        if DBInputPassword:
            old_db.Password = aes_DBInputPassword
        old_db.Name = DBInputName
        old_db.Desc = DBInputDesc
    else:
        new_db = DB(LANIP=DBInputLANIP, IP=DBInputIP, User=DBInputUser, Password=aes_DBInputPassword, Name=DBInputName, Desc=DBInputDesc, Addon=datetime.now())
        db.session.add(new_db)


def kafka_modify():
    """Kafka表表单处理"""
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


def kafkahost_modify():
    """KafkaHost表表单处理"""
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


def program_modify():
    """Program表表单处理"""
    ProgramInputID = request.form.get('ProgramInputID')
    ProgramInputDay = request.form.get('ProgramInputDay')
    ProgramInputMaxKwsCount = request.form.get('ProgramInputMaxKwsCount')
    ProgramInputMaxEntityCount = request.form.get('ProgramInputMaxEntityCount')
    ProgramInputExpired = request.form.get('ProgramInputExpired')
    ProgramInputSSDBExpired = request.form.get('ProgramInputSSDBExpired')
    ProgramInputHSSDBExpired = request.form.get('ProgramInputHSSDBExpired')
    ProgramInputSkipSiteTypes = request.form.get('ProgramInputSkipSiteTypes')
    ProgramInputIsNeedStatistic = request.form.get('ProgramInputIsNeedStatistic')
    ProgramInputIsNeedDB = request.form.get('ProgramInputIsNeedDB')
    ProgramInputSaveUnfit = request.form.get('ProgramInputSaveUnfit')
    ProgramInputDesc = request.form.get('ProgramInputDesc')
    old_program = Program.query.filter_by(ID=ProgramInputID).first()
    if old_program:
        old_program.Day = ProgramInputDay
        old_program.MaxKwsCount = ProgramInputMaxKwsCount
        old_program.MaxEntityCount = ProgramInputMaxEntityCount
        old_program.Expired = ProgramInputExpired
        old_program.SSDBExpired = ProgramInputSSDBExpired
        old_program.HSSDBExpired = ProgramInputHSSDBExpired
        old_program.SkipSiteTypes = ProgramInputSkipSiteTypes
        old_program.IsNeedStatistic = ProgramInputIsNeedStatistic
        old_program.IsNeedDB = ProgramInputIsNeedDB
        old_program.SaveUnfit = ProgramInputSaveUnfit
        old_program.Desc = ProgramInputDesc
    else:
        new_program = Program(Day=ProgramInputDay, MaxKwsCount=ProgramInputMaxKwsCount,
                              MaxEntityCount=ProgramInputMaxEntityCount, Expired=ProgramInputExpired,
                              SSDBExpired=ProgramInputSSDBExpired, HSSDBExpired = ProgramInputHSSDBExpired,
                              SkipSiteTypes=ProgramInputSkipSiteTypes,IsNeedStatistic=ProgramInputIsNeedStatistic,
                              IsNeedDB=ProgramInputIsNeedDB, SaveUnfit = ProgramInputSaveUnfit,
                              Desc=ProgramInputDesc, Addon=datetime.now())
        db.session.add(new_program)


def ssdb_modify():
    """SSDB表表单处理"""
    SSDBInputID = request.form.get('SSDBInputID')
    SSDBInputLANIP = request.form.get('SSDBInputLANIP')
    SSDBInputPort = request.form.get('SSDBInputPort')
    SSDBInputDesc = request.form.get('SSDBInputDesc')
    old_ssdb = SSDB.query.filter_by(ID=SSDBInputID).first()
    if old_ssdb:
        old_ssdb.LANIP = SSDBInputLANIP
        old_ssdb.Port = SSDBInputPort
        old_ssdb.Desc = SSDBInputDesc
    else:
        new_ssdb = SSDB(LANIP=SSDBInputLANIP,Port = SSDBInputPort, Desc=SSDBInputDesc, Addon=datetime.now())
        db.session.add(new_ssdb)


def type_modify():
    """Type表表单处理"""
    TypeInputID = request.form.get('TypeInputID')
    TypeInputCode = request.form.get('TypeInputCode')
    TypeInputDesc = request.form.get('TypeInputDesc')
    old_type = Type.query.filter_by(ID=TypeInputID).first()
    if old_type:
        old_type.Code = TypeInputCode
        old_type.Desc = TypeInputDesc
    else:
        new_type = Type(Code=TypeInputCode, Desc=TypeInputDesc, Addon=datetime.now())
        db.session.add(new_type)
