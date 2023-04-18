#!/usr/bin/env python
# encoding: utf-8

import itertools


# 替换基于用户名变量的密码
from libs.lib_social_dict.social_const import *


def replace_mark_user_name_base(user_pass_pair_list, mark_string):
    # 替换基于用户名变量的密码
    new_user_pass_pair_list = []
    for user_pass in user_pass_pair_list:
        name_ = user_pass[0]
        pass_ = user_pass[1]
        if mark_string in pass_:
            pass_ = str(pass_).replace(mark_string, name_)
        new_user_pass_pair_list.append((name_, pass_))

    return new_user_pass_pair_list


# 替换基于用户名变量的密码 并且支持 在替换过程中对账号密码进行处理
def replace_mark_user_name_itertools(user_pass_pair_list,
                                     mark_string,
                                     options_dict={}
                                     ):
    # 替换基于用户名变量的密码 并且支持 在替换过程中对账号密码进行处理
    new_user_pass_pair_list = []
    for user_pass in user_pass_pair_list:
        base_name = str(user_pass[0])
        base_pass = str(user_pass[1])

        # 生成其他账号密码
        user_name_list = []
        user_pass_list = []

        # 首字母大写用户名
        if options_dict[SO_NAME_CAPER]:
            user_name_list.append(str(base_name).capitalize())

        # 全部小写用户名
        if options_dict[SO_NAME_LOWER]:
            user_name_list.append(str(base_name).lower())

        # 全部大写用户名
        if options_dict[SO_NAME_UPPER]:
            user_name_list.append(str(base_name).upper())

        # 替换密码内的用户名标记
        if mark_string not in base_pass:
            new_user_pass_pair_list.append((str(base_name), base_pass))

            # 仅处理密码中包含用户名变量的密码
            if not options_dict[SO_ONLY_REPL_MARK_PASS]:
                # 首字母大写的密码
                if options_dict[SO_PASS_CAPER]:
                    user_pass_list.append(str(base_pass).capitalize())

                # 全部小写的密码
                if options_dict[SO_PASS_LOWER]:
                    user_pass_list.append(str(base_pass).lower())

                # 全部大写的密码
                if options_dict[SO_PASS_UPPER]:
                    user_pass_list.append(str(base_pass).upper())

        else:
            # 添加普通替换
            new_user_pass_pair_list.append((base_name, base_pass.replace(mark_string, base_name)))

            # 用户名首字母大写的密码
            if options_dict[SO_PASS_CAPER]:
                user_pass_list.append(base_pass.replace(mark_string, str(base_name).capitalize()))

            # 用户名全部小写的密码
            if options_dict[SO_PASS_LOWER]:
                user_pass_list.append(base_pass.replace(mark_string, str(base_name).lower()))

            # 用户名全部大写的密码
            if options_dict[SO_PASS_UPPER]:
                user_pass_list.append(base_pass.replace(mark_string, str(base_name).upper()))

        # 去重和填充用户名密码元素
        if user_name_list:
            user_name_list = list(set(user_name_list))
        else:
            user_name_list.append(base_name)

        if user_pass_list:
            user_pass_list = list(set(user_pass_list))
        else:
            user_pass_list.append(base_pass.replace(mark_string, base_name))

        # 组合账户密码 并存入
        product_list = list(itertools.product(user_name_list, user_pass_list))
        new_user_pass_pair_list.extend(product_list)

    return new_user_pass_pair_list
