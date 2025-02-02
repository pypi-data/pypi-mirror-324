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


# 写入日志
def write_to_log(level="info", prefix="系统异常", content="", err_obj=None):
    """
    写入日志, 注意仅仅支持python3.0以上版本
    :param level: 写入错误日志等级
    :param prefix: 提示错误类型
    :param content: 错误内容
    :param err_obj: try except 捕捉到的错误对象
    :return: data, err_msg
    """
    logger = getLogger('log')
    try:
        if not err_obj is None:
            logger.error(
                '---' + prefix + ":" + str(err_obj) + ";" +
                (" content:" + str(content) + ";" if content else "") +
                " line:" + str(err_obj.__traceback__.tb_lineno) + ";" +
                " file:" + str(err_obj.__traceback__.tb_frame.f_globals["__file__"]) + ";" +
                " datetime:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + ";"
            )
        elif level == "info":
            logger.error('---' + prefix + ":" + str(content))
        elif level == "error":
            logger.error('---' + prefix + ":" + str(content))
        return True, None
    except Exception as err:
        return False, str(err)
