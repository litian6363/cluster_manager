#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
监控页面路由
"""

__author__ = 'LiTian'

# import random
# from flask import Blueprint, request, render_template
# from web.tools.cookie_factory import check_user_cookie
# from pyecharts import Scatter3D
# from pyecharts.constants import DEFAULT_HOST
# from pyecharts.utils import json_dumps
#
#
# mod = Blueprint('monitor', __name__, url_prefix='/monitor')
#
#
# @mod.route('/')
# @check_user_cookie(request)
# def index():
#     s3d = scatter3d()
#     return render_template(
#         'monitor/index.html',
#         chart_id=s3d.chart_id,
#         my_width='100%',
#         my_height=600,
#         my_option=json_dumps(s3d.options),
#         host=DEFAULT_HOST,
#         script_list=s3d.get_js_dependencies(),
#     )
#
#
# def scatter3d():
#     data1 = [generate_3d_random_point() for _ in range(100)]
#     data2 = [generate_3d_random_point() for _ in range(100)]
#     data3 = [generate_3d_random_point() for _ in range(100)]
#     range_color = [
#         '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
#         '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'
#     ]
#     scatter3d = Scatter3D('Hello pyecharts!!!', width=1200, height=600)
#     scatter3d.add('aaaa', data1, is_visualmap=True, visual_range_color=range_color)
#     scatter3d.add('bbbb', data2, is_visualmap=True, visual_range_color=range_color)
#     scatter3d.add('cccc', data3, is_visualmap=True, visual_range_color=range_color)
#     return scatter3d
#
#
# def generate_3d_random_point():
#     return [
#         random.randint(0, 100),
#         random.randint(0, 100),
#         random.randint(0, 100),
#     ]
