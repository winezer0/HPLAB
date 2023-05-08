#!/usr/bin/env python
# encoding: utf-8


# 判断列表内的元素是否存在有包含在字符串内的
import json


def list_ele_in_str(list_=None, str_=None, default=False):
    if list_ is None:
        list_ = []

    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag


def freeze_headers(headers={}):
    """
    将字典转为字符串
    :param headers:
    :return:
    """
    if isinstance(headers, dict):
        headers = json.dumps(headers, sort_keys=True)
    return headers


def unfreeze_headers(headers=""):
    """
    将字符串转为字典
    :param headers:
    :return:
    """
    if isinstance(headers, str):
        headers = json.loads(headers)
    return headers
