#!/usr/bin/env python
# encoding: utf-8

# 分割写法 分离用户名密码对
from libs.lib_dyna_rule.dyna_rule_tools import frozen_tuple_list, unfrozen_tuple_list


# 去除已经爆破过的元素
def remove_has_brute_user_pass_pair(name_pass_tuple_list, history_pair_str_list, str_link_symbol):
    # 去除已经爆破过的元素

    # 先将历史爆破记录转为 元组列表格式
    history_tuple_list = split_str_list_to_tuple(history_pair_str_list, str_link_symbol)
    # 去重 user_name_pass_pair_list 中 被  history_user_pass_tuple_list包含的元素
    history_tuple_list = frozen_tuple_list(history_tuple_list, link_symbol=str_link_symbol)
    name_pass_tuple_list = frozen_tuple_list(name_pass_tuple_list, link_symbol=str_link_symbol)

    if name_pass_tuple_list and history_tuple_list:
        name_pass_tuple_list = list(set(name_pass_tuple_list) - set(history_tuple_list))

    name_pass_tuple_list = unfrozen_tuple_list(name_pass_tuple_list, link_symbol=str_link_symbol)
    return name_pass_tuple_list


# 切割(账号<-->密码)字符串列表到(账号,密码)元组列表
def split_str_list_to_tuple(pair_str_list, str_link_symbol):
    # 切割(账号<-->密码)字符串列表到(账号,密码)元组列表
    tuple_list = []
    for pair_str in pair_str_list:
        user_name, user_pass = pair_str.split(str_link_symbol, 1)
        tuple_list.append((user_name, user_pass))
    return tuple_list


