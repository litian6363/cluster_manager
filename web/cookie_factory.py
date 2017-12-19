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


# 定义选取数量（每一页都会选取相应选取数量的数据库中日志出来显示）
class Page(object):
    def __init__(self, item_count, page_index=1, page_size=10):  # 参数依次是：数据库博客总数，初始页，一页显示博客数
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)  # 可以显示的最大页数
        if (item_count == 0) or (page_index > self.page_count):  # 假如数据库没有博客或开始页大于最大可显示页（到最后了）
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index  # 初始页
            self.offset = self.page_size * (page_index - 1)  # 当前页数，应从数据库的那个序列博客开始显示
            self.limit = self.page_size  # 当前页数，应从数据库的那个序列博客结束像素
        self.has_next = self.page_index < self.page_count  # 有否下一页
        self.has_previous = self.page_index > 1  # 有否上一页

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % \
               (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__
