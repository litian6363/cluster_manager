#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
制作和解释cookie
"""

__author__ = 'Li Tian'


import hashlib
import logging
from web.flaskr import app, Users


# 根据user对象，制作cookie
def user2cookie(user):
    st = '%s^%s^%s' % (user.email, user.password, app.config['SECRET_KEY'])
    li = [user.email, hashlib.sha1(st.encode('utf-8')).hexdigest()]
    return '^'.join(li)


# 解释cookie，返回user对象
def cookie2user(cookie):
    if not cookie: return None
    try:
        li = cookie.split('^')
        if len(li) != 3:
            logging.info('invalid cookie length')
            return None
        email, sha1 = li
        user = Users.query.filter_by(Users.email == email).first()
        if user:
            logging.info('invalid cookie user')
            return None
        st = '%s^%s^%s' % (user.email, user.password, app.config['SECRET_KEY'])
        if sha1 != hashlib.sha1(st.encode('utf-8')).hexdigest():
            logging.info('invalid cookie sha1')
            return None
        user.password = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None
