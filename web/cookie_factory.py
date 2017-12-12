#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
在flask中制作和解释cookie
"""

__author__ = 'LiTian'


import hashlib
import logging


def user2cookie(key, user):
    """根据user对象，制作cookie"""
    st = '%s^%s^%s' % (user.email, user.password, key)
    li = [user.email, hashlib.sha1(st.encode('utf-8')).hexdigest()]
    return '^'.join(li)


def cookie2user(key, Users, cookie):
    """解释cookie，返回user对象"""
    if not cookie: return None
    try:
        li = cookie.split('^')
        if len(li) != 2:
            print('invalid cookie length')
            return None
        email, sha1 = li
        user = Users.query.filter_by(email=email).first()
        if not user:
            print('invalid cookie user')
            return None
        st = '%s^%s^%s' % (user.email, user.password, key)
        if sha1 != hashlib.sha1(st.encode('utf-8')).hexdigest():
            print('invalid cookie sha1')
            return None
        user.password = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None
