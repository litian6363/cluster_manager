#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
制作和解释cookie
"""

__author__ = 'LiTian'


import hashlib
import logging


def user2cookie(key, user):
    """根据user对象，制作cookie"""
    st = '%s^%s^%s' % (user.UserName, user.Password, key)
    li = [user.UserName, hashlib.sha1(st.encode('utf-8')).hexdigest()]
    return '^'.join(li)


def cookie2user(key, Users, cookie):
    """解释cookie，返回user对象"""
    if not cookie: return None
    try:
        li = cookie.split('^')
        if len(li) != 2:
            print('invalid cookie length')
            return None
        username, sha1 = li
        user = Users.query.filter_by(UserName=username).first()
        if not user:
            print('invalid cookie user')
            return None
        st = '%s^%s^%s' % (user.UserName, user.Password, key)
        if sha1 != hashlib.sha1(st.encode('utf-8')).hexdigest():
            print('invalid cookie sha1')
            return None
        return True
    except Exception as e:
        logging.exception(e)
        return None

