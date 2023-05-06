#!/usr/bin/env python
# encoding: utf-8

# 变形 [(user:pass)] 中的pass为其他格式
def transfer_passwd(user_pass_pair_list, options_dict):
    new_user_pass_pair_list = []

    for base_name, base_pass in user_pass_pair_list:
        print(base_name, base_pass)
        # 解析密码字符串
        # 需求：1、进行 leetcode 替换

    return new_user_pass_pair_list


if __name__ == '__main__':
    pair_list = [("admin","pass@12345")]
    options = {}
    transfer_passwd(pair_list, options)