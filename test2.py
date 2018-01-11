#!usr/bin/env python3
# -*- coding: utf-8 -*-


from web.tools.output_config_api import make_config_dict
from web import app

# with app.app_context():
#     for a in Users.query.all():
#         print(a.to_dict())

# with app.app_context():
#     re_dict = dict()
#     for r in Config.query.all():
#         value_dict = dict()
#         value_dict['DB'] = DB.query.filter_by(ID=r.DBID).first().to_dict()
#         value_dict['KafkaHost'] = KafkaHost.query.filter_by(ID=r.KafkaHostID).first().to_dict()
#         value_dict['Kafka'] = Kafka.query.filter_by(ID=r.KafkaID).first().to_dict()
#         value_dict['Program'] = Program.query.filter_by(ID=r.ProgramID).first().to_dict()
#         value_dict['SSDB'] = SSDB.query.filter_by(ID=r.SSDBID).first().to_dict()
#         value_dict['Sign'] = r.Sign
#         value_dict['Addon'] = r.Addon
#         re_dict.setdefault(r.ID, value_dict)

# with app.app_context():
#     re_dict = {}
#     for r in Config.query.all():
#         value_dict = {
#             'DB': DB.query.filter_by(ID=r.DBID).first().to_dict(),
#             'KafkaHost': KafkaHost.query.filter_by(ID=r.KafkaHostID).first().to_dict(),
#             'Kafka': Kafka.query.filter_by(ID=r.KafkaID).first().to_dict(),
#             'Program': Program.query.filter_by(ID=r.ProgramID).first().to_dict(),
#             'SSDB': SSDB.query.filter_by(ID=r.SSDBID).first().to_dict(),
#             'Sign': r.Sign,
#             'Addon': r.Addon,
#         }
#         re_dict.setdefault(r.ID, value_dict)
#

with app.app_context():
    re_dict = make_config_dict()

print(type(re_dict))
print(re_dict[6])

{u'info': [{u'name': u'URUN\u5185\u90e8', u'sn': u'0001', u'id': u'4f5815ff02b8752db500000b', u'cityid': u'4d8af8a31d41c80f910000db', u'departmentid': u'4d8b096d4ba9f5153c96821d', u'parentid': u'0', u'productid': u'0', u'provinceid': u'4d8af8a31d41c80f910000da', u'addon': u'2012-03-08 10:10:41'}], u'status': u'True'}




