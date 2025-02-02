# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
import uuid


# 生成随机字符串，2千万次重复两次。
def get_short_id(length=8):
    """
    生成随机字符串，2千万次重复两次。
    :param length:
    :return: 随机字符串
    """
    length = 8 if length > 8 else length
    dictionary = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    ]
    random_id = str(uuid.uuid4()).replace("-", '')  # 注意这里需要用uuid4
    buffer = []
    for i in range(0, length):
        start = i * 4
        end = i * 4 + 4
        val = int(random_id[start:end], 16)
        buffer.append(dictionary[val % 62])
    return "".join(buffer)
