# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
import datetime
from .j_transform_type import JTransformType

# 处理字典：白名单、黑名单、别名、移除空值、筛选类型
def format_params_handle(
        param_dict: dict,
        filter_filed_list: list = None,
        remove_filed_list: list = None,
        alias_dict: dict = None,
        split_list: list = None,
        split_char: str = ";",
        is_remove_null: bool = True,
        is_remove_empty: bool = False,
        date_format_dict: dict = None,
        is_validate_type: bool = False,
) -> dict:
    """
    字段筛选并替换成别名
    :param is_validate_type: 是否验证数据合法性
    :param param_dict: 参数值
    :param filter_filed_list: 字段白名单，如:["id":int]
    :param remove_filed_list: 字段黑名单,["id",....]
    :param alias_dict: 别名字典, {"id":"user_id"}
    :param split_char: 字符串拆分依据
    :param split_list: 拆分字符换,该参数为了适配使用符号分割成列表。["id_list",....]
    :param is_remove_null:  是否把带有None的值移除掉
    :param is_remove_empty: 是否移除value类型等于False的字段,移除"",0,"0",None
    :param date_format_dict: 日期格式化 日期列表，{field：(from_format,to_format),}如：{"field":("%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M:%S")}
    :return: param_dict
    """
    # 转换的数据类型不符合，直接返回出去
    if not isinstance(param_dict, dict):
        raise ValueError("param_dict 必须是字典格式")
    # 过滤字段并且得数据类型映射
    new_filter_filed_list = []  # 拆分字段类型的白名单
    must_type_map = {}  # 从白名单中拆分出字段与类型的映射
    if filter_filed_list and isinstance(filter_filed_list, list):
        for i in filter_filed_list:
            key_type_list = i.split("|", 1)
            [key, key_type] = key_type_list if len(key_type_list) == 2 else [key_type_list[0], None]  # 如果为类型None，则默认是字符串
            must_type_map[key] = key_type
            new_filter_filed_list.append(key)
        param_dict = {k: v for k, v in param_dict.copy().items() if k in new_filter_filed_list and (not is_remove_empty or v) and (not is_remove_null or not v is None)}
    # 剔除字段
    if remove_filed_list and isinstance(remove_filed_list, list):
        param_dict = {k: v for k, v in param_dict.copy().items() if not k in remove_filed_list and (not is_remove_empty or v) and (not is_remove_null or not v is None)}
    # 字段拆分
    if split_list and isinstance(split_list, list):
        param_dict = {k: (str(v).split(split_char) if k in split_list and not isinstance(v, list) else v) for k, v in param_dict.copy().items()}
    # 类型转换
    if must_type_map and isinstance(must_type_map, dict):
        for k, v in param_dict.copy().items():
            v, is_err = JTransformType.to(v, must_type_map.get(k, None))
            if is_err and not is_validate_type:
                param_dict.pop(k)
            elif is_err and is_validate_type:
                raise ValueError(k + ":" + is_err)
            else:
                # 覆盖掉转换的值
                param_dict[k] = v

    # 日期字段格式转换
    if date_format_dict and isinstance(date_format_dict, dict):
        for k, v in param_dict.copy().items():
            if not date_format_dict.get(k):
                continue
            try:
                from_format, to_format = date_format_dict[k]
                if not isinstance(v, datetime.datetime) and isinstance(v, str):
                    parse_date_obj = datetime.datetime.strptime(v, from_format)
                else:
                    parse_date_obj = v
                param_dict[k] = parse_date_obj.strftime(to_format)
            except Exception as e:
                pass

    # 别名替换
    if alias_dict and isinstance(alias_dict, dict):
        param_dict = {alias_dict.get(k, k): v for k, v in param_dict.copy().items()}

    return param_dict
