# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
from cmath import cos
import copy
import datetime
import difflib
import importlib
import inspect
import json
from logging import getLogger
from math import sin, asin, sqrt
import random
import re
import sys
import time
from urllib.parse import parse_qs
import uuid

from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
# from numpy.core._multiarray_umath import radians
from rest_framework.request import Request
# import xmltodict

# =========== section 单例装饰器 start ==================


_instance = {}


# 过滤list内容，白名单、黑名单、别名
def format_list_handle(param_list, filter_filed_list=None, remove_filed_list=None, alias_dict=None, remove_repeat=True):
    """
    过滤list内容
    :param param_list: 传入 param_list
    :param filter_filed_list: 需要的字段
    :param remove_filed_list: 需要删除的列表
    :param alias_dict: 元素起别名
    :return:param_list： 处理后的 param_list
    """
    if not param_list:
        return param_list
    # 类型判断 过滤字段
    if filter_filed_list and isinstance(filter_filed_list, list):
        param_list = [i for i in param_list if i in filter_filed_list]

    # 类型判断， 剔除字段
    if remove_filed_list and isinstance(remove_filed_list, list):
        param_list = [j for j in param_list if not j in remove_filed_list]

    # 类型判断 字段转换
    if alias_dict and isinstance(alias_dict, dict):
        param_list = [alias_dict.get(k, k) for k in param_list]

    # 进行去重
    if remove_repeat:
        param_list = list(set(param_list))

    return param_list
