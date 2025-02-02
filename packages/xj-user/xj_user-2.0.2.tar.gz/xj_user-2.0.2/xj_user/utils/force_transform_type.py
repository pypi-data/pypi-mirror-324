# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
import datetime
from parse_json import parse_json


# 强制转换类型数据
def force_transform_type(variable=None, var_type: str = None, default=None, **kwargs):
    """
    强制转换类型，转换规则如下：
    1.变量为空使用默认值返回。认为是空值判断。
    2.转换类型为空则，返回输入变量。认为不需要进行类型转换。
    3.无法转换则返回默认值，转换失败，数据存在问题则饭hi默认值。
    :param default: 数据为空或无法转换的时候返回默认值
    :param variable: 变量
    :param var_type: 转换类型 str|int|bool|float|dict|list|date
    :return: transform_variable, is_err
    """
    if variable is None:  # 为空时候，则返回默认值
        return default, None
    if not var_type:  # 转换类型为空，则不进行转换
        return variable, None
    # 强制类型转换
    try:
        if var_type == "str":
            return variable if isinstance(variable, str) else str(variable), None
        elif var_type == "int":
            return variable if isinstance(variable, int) else int(variable), None
        elif var_type == "bool":
            if variable in (None, '', [], (), {}):
                return None, None
            if variable in (True, False):
                return bool(variable), None
            if variable in ('t', 'True', '1'):
                return True, None
            if variable in ('f', 'False', '0'):
                return False, None
            return None, "'" + str(variable) + "'" + "不是一个有效的布尔类型数据"
        elif var_type == "float":
            return variable if isinstance(variable, float) else float(variable), None
        elif var_type == "only_dict":
            # 不包括列表
            variable = parse_json(variable)
            if isinstance(variable, dict):
                return variable, None
            return default, str(variable) + "无法转换为json格式"
        elif var_type == "dict":
            # 字典包括列表字典
            variable = parse_json(variable)
            if isinstance(variable, dict) or isinstance(variable, list):
                return variable, None
            return default, str(variable) + "无法转换为json格式"
        elif var_type == "list":
            variable = parse_json(variable)
            if isinstance(variable, list):
                return variable, None
            return default, str(variable) + "无法转换为list格式"
        elif var_type == "list_int":
            variable = parse_json(variable)
            result = []
            if isinstance(variable, list):
                for i in variable:
                    # 过滤掉非int类型
                    i, is_pass = force_transform_type(variable=i, var_type="int")
                    if is_pass:
                        continue
                    result.append(i)
                return result, None
            return default, str(variable) + "无法转换为list格式"
        elif var_type == "date":
            format_map = {
                '%Y-%m-%d': "%Y-%m-%d 00:00:00",
                '%Y-%m-%d %H': '%Y-%m-%d %H:00:00',
                '%Y-%m-%d %H:%M': '%Y-%m-%d %H:%M:00',
                '%Y-%m-%d %H:%M:%S': '%Y-%m-%d %H:%M:%S'
            }
            for format_input, format_output in format_map.items():
                try:
                    return datetime.datetime.strptime(variable, format_input).strftime(format_output), None
                except ValueError:
                    pass
            raise ValueError
        else:  # 如果指派的类型不存在，默认值非空则返回默认值，否则原样返回
            return variable if default is None else default, str(var_type) + "不是一个有效的转换类型"
    except TypeError:
        return default, "'" + str(variable) + "'" + "不是一个有效的" + str(var_type) + "类型数据"
    except ValueError:
        return default, "'" + str(variable) + "'" + "不是一个有效的" + str(var_type) + "类型数据"
