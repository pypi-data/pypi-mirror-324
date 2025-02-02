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


def filter_fields_handler(
        default_field_list: list = None,
        input_field_expression: 'str|list' = None,
        split_char: str = ";",
        all_field_list: list = None
) -> list:
    """
    过滤字段处理器
    使用：服务提供者只需要提供一个默认字段的列表或者符号分割的字符串，然后再把前端传进来的字段表达式传进来即可
    :param all_field_list: 全部合法性字段
    :param default_field_list: 默认字段列表,或者是符号分割的字符串
    :param input_field_expression: 字段处理表达式。"***filed_1;filed_2;;filed_2;!!!filed_1;filed_2;" 或者"filed_1;filed_2"或者 [filed_1,filed_2;]
    :param split_char: 拆分字符串,默认使用分号。
    :return: ["field_1",.....]
    """
    # all_field_list 与 default_field_list 因为是在服务层调用，所以强制列表类型
    if all_field_list is None or not isinstance(all_field_list, list):
        all_field_list = []
    if default_field_list is None or not isinstance(default_field_list, list):
        default_field_list = []
    # 处理默认字段
    default_field_list = default_field_list.split(split_char) if isinstance(default_field_list, str) else default_field_list or all_field_list

    # ========== 处理字段处理表达式 ==========
    # 如果没有传递字段表达式，默认字段不为空。则返回默认字段
    if input_field_expression is None:
        return default_field_list

    # 字段表达式字符串的情况
    elif isinstance(input_field_expression, str):
        if not re.search("[***|!!!]", input_field_expression):
            return format_list_handle(param_list=input_field_expression.split(split_char), filter_filed_list=all_field_list)
        # 加法或者减法原则
        default_field_hash = {i: "" for i in default_field_list}
        add_filed_expression = re.search("[***][^(!!!)]*", input_field_expression)
        sub_filed_expression = re.search("[!!!][^(***)]*", input_field_expression)
        if add_filed_expression:
            add_filed_list = add_filed_expression.group().replace("***", "").split(split_char)
            for i in add_filed_list:
                default_field_hash.update({i: ""})
        if sub_filed_expression:
            sub_filed_list = sub_filed_expression.group().replace("!!!", "").split(split_char)
            for i in sub_filed_list:
                default_field_hash.pop(i, None)
        return format_list_handle(param_list=[i for i in list(default_field_hash.keys()) if i], filter_filed_list=all_field_list)

    # 如果是列表则代表用户使用自定义的字段列表，不使用默认的字段列表
    elif isinstance(input_field_expression, list):
        return format_list_handle(param_list=input_field_expression, filter_filed_list=all_field_list)

    # input_field_expression的类型都不符合，则返回default_field_list
    else:
        return default_field_list
    # ========== 处理字段处理表达式 ==========
