#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/15 14:28 
# @File : test_flaskr.py
# @Software: PyCharm
# @Author : LiTian

import pytest


def p(a):
    return a * 10


def test_p():
    assert p(3) == 30
    assert p(10) == 101