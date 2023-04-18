#!/usr/bin/env python
# encoding: utf-8

import re


def has_chinese_func(string):
    # 存在中文
    return bool(re.search("[\u4e00-\u9fa5]", string))


# 判断字符中是否存在数字
def has_digit_func(string):
    for char in str(string):
        if char.isdigit():
            return True
    return False


# 判断字符中是否存在大写字母
def has_upper_func(string):
    for char in str(string):
        if char.isupper():
            return True
    return False


# 判断字符中是否存在小写字母
def has_lower_func(string):
    for char in str(string):
        if char.islower():
            return True
    return False


# 判断字符串中是否存在符号
def has_symbol_func(string):
    for char in str(string):
        if char in set('!@#$%^&*()_-+={}[]|\:;"<>,.?/~`'):
            return True
    return False


# 判断字符串中 数字、大写、小写、符号的情况
def analyse_string_per_char(string):
    # 分析字符串,判断是否包含指定的元素
    has_digit = has_digit_func(string)
    has_upper = has_upper_func(string)
    has_lower = has_lower_func(string)
    has_symbol = has_symbol_func(string)
    return has_digit, has_upper, has_lower, has_symbol


# 统计字符串中 数字、大写、小写、符号、其他的数量
def statistic_char_frequency(string):
    # 统计每种类型的符号数量
    upper_count = 0
    lower_count = 0
    symbol_count = 0
    digit_count = 0
    other_count = 0
    for letter in string:
        letter = str(letter)
        if letter.isupper():
            upper_count += 1
        elif letter.islower():
            lower_count += 1
        elif letter.isdigit():
            digit_count += 1
        elif letter in set('!@#$%^&*()_-+={}[]|\:;"<>,.?/~`'):
            symbol_count += 1
        else:
            other_count += 1
    return upper_count, lower_count, symbol_count, digit_count, other_count


def format_rule_list(tuple_list):
    tuple_list = [
        (bool(has_digit), bool(has_upper), bool(has_lower), bool(has_symbol))
        for has_digit, has_upper, has_lower, has_symbol in tuple_list
    ]
    return tuple_list



