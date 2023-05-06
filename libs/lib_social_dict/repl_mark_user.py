#!/usr/bin/env python
# encoding: utf-8

import itertools

# 替换基于用户名变量的密码
from libs.lib_social_dict.repl_const import *


# 替换基于用户名变量的密码 并且支持 在替换过程中对账号密码进行处理
def replace_mark_user_on_pass(user_pass_pair_list, mark_string, options_dict ):
    # 替换基于用户名变量的密码 并且支持 在替换过程中对账号密码进行处理
    new_user_pass_pair_list = []
    for base_name, base_pass in user_pass_pair_list:
        # base_name = str(user_pass[0])
        # base_pass = str(user_pass[1])

        # 生成其他账号密码
        user_name_list = []
        user_pass_list = []

        # 保留原始用户名
        if options_dict[SO_NAME_KEEP]:
            user_name_list.append(str(base_name))

        # 首字母大写用户名
        if options_dict[SO_NAME_CAPER]:
            user_name_list.append(str(base_name).capitalize())

        # 全部小写用户名
        if options_dict[SO_NAME_LOWER]:
            user_name_list.append(str(base_name).lower())

        # 全部大写用户名
        if options_dict[SO_NAME_UPPER]:
            user_name_list.append(str(base_name).upper())

        # 保留原始密码|同时进行原始用户名的替换
        if options_dict[SO_PASS_KEEP]:
            user_pass_list.append(base_pass.replace(mark_string, base_name))

        # 替换密码内的用户名标记
        if mark_string in base_pass:
            # 用户名首字母大写的密码
            if options_dict[SO_PASS_CAPER]:
                user_pass_list.append(base_pass.replace(mark_string, str(base_name).capitalize()))

            # 用户名全部小写的密码
            if options_dict[SO_PASS_LOWER]:
                user_pass_list.append(base_pass.replace(mark_string, str(base_name).lower()))

            # 用户名全部大写的密码
            if options_dict[SO_PASS_UPPER]:
                user_pass_list.append(base_pass.replace(mark_string, str(base_name).upper()))
        else:
            # 并非 仅处理密码中包含用户名变量的密码
            if not options_dict[SO_ONLY_MARK_PASS]:
                # 首字母大写的密码
                if options_dict[SO_PASS_CAPER]:
                    user_pass_list.append(str(base_pass).capitalize())

                # 全部小写的密码
                if options_dict[SO_PASS_LOWER]:
                    user_pass_list.append(str(base_pass).lower())

                # 全部大写的密码
                if options_dict[SO_PASS_UPPER]:
                    user_pass_list.append(str(base_pass).upper())

        # 去重和填充用户名密码元素
        user_name_list = list(set(user_name_list)) if user_name_list else [base_name]
        user_pass_list = list(set(user_pass_list)) if user_pass_list else [base_pass.replace(mark_string, base_name)]

        # 组合账户密码 并存入
        product_list = list(itertools.product(user_name_list, user_pass_list))
        new_user_pass_pair_list.extend(product_list)
    new_user_pass_pair_list = list(set(new_user_pass_pair_list))
    return new_user_pass_pair_list
