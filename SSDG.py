#!/usr/bin/env python
# encoding: utf-8

import argparse

from libs.lib_chinese_encode.chinese_encode import tuple_list_chinese_encode_by_char
from libs.lib_chinese_pinyin.chinese_list_to_alphabet_list import dict_chinese_to_dict_alphabet
from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str
from libs.lib_dyna_rule.base_rule_parser import base_rule_render_list
from libs.lib_dyna_rule.dyna_rule_tools import cartesian_product_merging, unfrozen_tuple_list
from libs.lib_dyna_rule.dyna_rule_tools import frozen_tuple_list
from libs.lib_dyna_rule.set_basic_var import set_base_var_dict
from libs.lib_dyna_rule.set_depend_var import set_dependent_var_dict
from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_write import write_lines
from libs.lib_filter_srting.filter_call import format_string_list, format_tuple_list
from libs.lib_log_print.logger_printer import set_logger, output, LOG_INFO
from libs.lib_social_dict.repl_mark_user_call import replace_mark_user_on_pass
from setting_total import *


# 分割写法 基于 用户名和密码规则生成 元组列表
def social_rule_handle_in_steps_two_list(target_url, default_name_list=None, default_pass_list=None):
    mode = "mode1"
    step = 0

    # 读取账号文件
    if default_name_list:
        output(f"[*] 已输入默认账号列表 {default_name_list} 忽略读取账号字典文件", level=LOG_INFO)
        name_list = default_name_list
    else:
        output(f"[*] 读取账号字典文件 {GB_USER_NAME_FILE}...", level=LOG_INFO)
        name_list = read_file_to_list(GB_USER_NAME_FILE, encoding=file_encoding(GB_USER_NAME_FILE), de_strip=True, de_weight=True)

    # 读取密码文件
    if default_pass_list:
        output(f"[*] 已输入默认密码列表 {default_pass_list} 忽略读取密码字典文件", level=LOG_INFO)
        pass_list = default_pass_list
    else:
        output(f"[*] 读取密码字典文件 {GB_USER_NAME_FILE}...", level=LOG_INFO)
        pass_list = read_file_to_list(GB_USER_PASS_FILE, encoding=file_encoding(GB_USER_PASS_FILE), de_strip=True, de_weight=True)

    output(f"[*] 读取账号|密码文件完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

    # 动态规则解析
    name_list, _, _ = base_rule_render_list(name_list)
    pass_list, _, _ = base_rule_render_list(pass_list)
    output(f"[*] 动态规则解析完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

    # 进行格式化
    name_list = format_string_list(string_list=name_list, options_dict=GB_FILTER_OPTIONS_NAME)
    pass_list = format_string_list(string_list=pass_list, options_dict=GB_FILTER_OPTIONS_PASS)
    output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)
    # 写入当前结果
    step += 1
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.render_base.name.txt"), name_list)
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.render_base.pass.txt"), pass_list)

    # 获取基本变量字典
    base_var_replace_dict = set_base_var_dict(GB_BASE_VAR_DIR, GB_DICT_SUFFIX, GB_BASE_VAR_REPLACE_DICT)
    output(f"[*] 基本变量字典获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

    base_var_replace_dict = set_base_var_dict(GB_BASE_DYNA_DIR, GB_DICT_SUFFIX, base_var_replace_dict)
    output(f"[*] 动态基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

    # 对账号列表依赖的 基本变量字典中的列表值进行中文处理
    name_base_var_replace_dict = set_base_var_dict(GB_BASE_NAME_DIR, GB_DICT_SUFFIX, base_var_replace_dict)
    output(f"[*] 账号基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

    pass_base_var_replace_dict = set_base_var_dict(GB_BASE_PASS_DIR, GB_DICT_SUFFIX, base_var_replace_dict)
    output(f"[*] 密码基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

    # 进行基本变量字典替换 及 其中的中文词汇处理
    if GB_CHINESE_TO_PINYIN:
        # 对账号列表依赖的 基本变量字典中的列表值进行中文处理
        name_base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=name_base_var_replace_dict,
                                                                   options_dict=GB_CHINESE_OPTIONS_NAME,
                                                                   store_chinese=GB_STORE_CHINESE)
        # 对密码列表依赖的 基本变量字典中的列表值进行中文处理
        pass_base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=pass_base_var_replace_dict,
                                                                   options_dict=GB_CHINESE_OPTIONS_PASS,
                                                                   store_chinese=GB_STORE_CHINESE)

        output(f"[*] 中文列表处理转换完成 name_base_var_replace_dict:{len(str(name_base_var_replace_dict))}", level=LOG_INFO)
        output(f"[*] 中文列表处理转换完成 pass_base_var_replace_dict:{len(str(pass_base_var_replace_dict))}", level=LOG_INFO)

        # 基本变量替换
        name_list, _, _ = replace_list_has_key_str(name_list, name_base_var_replace_dict)
        pass_list, _, _ = replace_list_has_key_str(pass_list, pass_base_var_replace_dict)
    else:
        # 基本变量替换
        name_list, _, _ = replace_list_has_key_str(name_list, name_base_var_replace_dict)
        pass_list, _, _ = replace_list_has_key_str(pass_list, pass_base_var_replace_dict)
    output(f"[*] 基本变量替换完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

    # 进行格式化
    name_list = format_string_list(string_list=name_list, options_dict=GB_FILTER_OPTIONS_NAME)
    pass_list = format_string_list(string_list=pass_list, options_dict=GB_FILTER_OPTIONS_PASS)
    output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)
    # 写入当前结果
    step += 1
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.replace_base.name.txt"), name_list)
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.replace_base.pass.txt"), pass_list)

    # 获取因变量
    dependent_var_replace_dict = set_dependent_var_dict(target_url=target_url,
                                                        base_dependent_dict=GB_DEPENDENT_VAR_REPLACE_DICT,
                                                        ignore_ip_format=GB_IGNORE_IP_FORMAT,
                                                        symbol_replace_dict=GB_SYMBOL_REPLACE_DICT,
                                                        not_allowed_symbol=GB_NOT_ALLOW_SYMBOL)
    output(f"[*] 获取因变量完成 dependent_var_replace_dict:{dependent_var_replace_dict}")

    # 因变量替换
    name_list, _, _ = replace_list_has_key_str(name_list, dependent_var_replace_dict)
    pass_list, _, _ = replace_list_has_key_str(pass_list, dependent_var_replace_dict)
    output(f"[*] 因变量替换完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}")

    # 进行格式化
    name_list = format_string_list(string_list=name_list, options_dict=GB_FILTER_OPTIONS_NAME)
    pass_list = format_string_list(string_list=pass_list, options_dict=GB_FILTER_OPTIONS_PASS)
    output(f"[*] 列表过滤格式化完成 name_list:{len(name_list)} | pass_list:{len(pass_list)}", level=LOG_INFO)

    # 写入当前结果
    step += 1
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.replace_dependent.name.txt"), name_list)
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.replace_dependent.pass.txt"), pass_list)

    # 组合用户名列表和密码列表
    name_pass_pair_list = cartesian_product_merging(name_list, pass_list)
    output(f"[*] 组合账号密码列表完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 进行格式化
    name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
    output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
    # 写入当前结果
    step += 1
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.cartesian.pair.txt"),
                frozen_tuple_list(name_pass_pair_list, link_symbol=":"))

    # 对基于用户名变量的密码做替换处理
    name_pass_pair_list = replace_mark_user_on_pass(name_pass_pair_list,
                                                    mark_string=GB_USER_NAME_MARK,
                                                    options_dict=GB_SOCIAL_OPTIONS_DICT)
    output(f"[*] 用户名变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 进行格式化
    name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
    output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 写入当前结果
    step += 1
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.replace_mark.pair.txt"),
                frozen_tuple_list(name_pass_pair_list, link_symbol=":"))

    # 对元组列表进行 中文编码处理
    if GB_CHINESE_ENCODE_CODING:
        name_pass_pair_list = tuple_list_chinese_encode_by_char(name_pass_pair_list,
                                                                coding_list=GB_CHINESE_ENCODE_CODING,
                                                                url_encode=GB_CHINESE_CHAR_URLENCODE,
                                                                de_strip=True,
                                                                only_chinese=GB_ONLY_CHINESE_URL_ENCODE)
        output(f"[*] 中文编码衍生完成 name_pass_pair_list:{len(name_pass_pair_list)}")
        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.chinese_encode.pair.txt"),
                    frozen_tuple_list(name_pass_pair_list, link_symbol=":"))

    return name_pass_pair_list


# 分割写法 基于 用户名:密码对 规则生成 元组列表
def social_rule_handle_in_steps_one_pairs(target_url, default_name_list=None, default_pass_list=None):
    mode = "mode2"
    step = 0

    # 读取用户账号文件
    name_pass_pair_list = read_file_to_list(GB_USER_PASS_PAIR_FILE,
                                            encoding=file_encoding(GB_USER_PASS_PAIR_FILE),
                                            de_strip=True,
                                            de_weight=True)
    output(f"[*] 读取账号密码文件完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 动态规则解析和基本变量替换过程 默认取消
    if GB_USE_PAIR_BASE_REPL:
        # 动态规则解析
        name_pass_pair_list, _, _ = base_rule_render_list(name_pass_pair_list)
        output(f"[*] 元组动态规则解析完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.base_render.pair.txt"), name_pass_pair_list)

        # 获取基本变量字典
        base_var_replace_dict = set_base_var_dict(GB_BASE_VAR_DIR, GB_DICT_SUFFIX, GB_BASE_VAR_REPLACE_DICT)
        output(f"[*] 基本变量字典获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        base_var_replace_dict = set_base_var_dict(GB_BASE_DYNA_DIR, GB_DICT_SUFFIX, base_var_replace_dict)
        output(f"[*] 动态基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        # base_var_replace_dict = set_base_var_dict(GB_BASE_NAME_DIR, GB_DICT_SUFFIX, base_var_replace_dict)
        # output(f"[*] 姓名基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")
        # base_var_replace_dict = set_base_var_dict(GB_BASE_PASS_DIR, GB_DICT_SUFFIX, base_var_replace_dict)
        # output(f"[*] 密码基本变量获取成功 base_var_replace_dict:{len(str(base_var_replace_dict))}")

        # 对基本变量字典中的列表值进行中文处理
        if GB_CHINESE_TO_PINYIN:
            output(f"[*] 中文列表处理转换开始 base_var_replace_dict:{len(str(base_var_replace_dict))}", level=LOG_INFO)
            base_var_replace_dict = dict_chinese_to_dict_alphabet(string_dict=base_var_replace_dict,
                                                                  options_dict=GB_CHINESE_OPTIONS_TUPLE,
                                                                  store_chinese=GB_STORE_CHINESE)
            output(f"[*] 中文列表处理转换完成 base_var_replace_dict:{len(str(base_var_replace_dict))}", level=LOG_INFO)

        # 基本变量替换
        name_pass_pair_list, _, _ = replace_list_has_key_str(name_pass_pair_list, base_var_replace_dict)
        output(f"[*] 元组基本变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.replace_base.pair.txt"), name_pass_pair_list)

        # 获取因变量
        dependent_var_replace_dict = set_dependent_var_dict(target_url=target_url,
                                                            base_dependent_dict=GB_DEPENDENT_VAR_REPLACE_DICT,
                                                            ignore_ip_format=GB_IGNORE_IP_FORMAT,
                                                            symbol_replace_dict=GB_SYMBOL_REPLACE_DICT,
                                                            not_allowed_symbol=GB_NOT_ALLOW_SYMBOL)

        # 因变量替换
        name_pass_pair_list, _, _ = replace_list_has_key_str(name_pass_pair_list, dependent_var_replace_dict)
        output(f"[*] 元组因变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

        # 写入当前结果
        step += 1
        write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.replace_dependent.pair.txt"), name_pass_pair_list)

    # 拆分出账号 密码对 元祖
    name_pass_pair_list = unfrozen_tuple_list(name_pass_pair_list, GB_PAIR_LINK_SYMBOL)

    # 如果输入了默认值列表,就组合更新的账号 列表
    if default_name_list or default_pass_list:
        output(f"[*] 已输入默认账号列表 {default_name_list} 需要更新账号密码列表")
        if default_name_list:
            pass_list = [name_pass_pair[1] for name_pass_pair in name_pass_pair_list]
            name_pass_pair_list = cartesian_product_merging(default_name_list, pass_list)
        if default_pass_list:
            name_list = [name_pass_pair[0] for name_pass_pair in name_pass_pair_list]
            name_pass_pair_list = cartesian_product_merging(name_list, default_pass_list)
        output(f"[*] 重组账号密码列表完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 对基于用户名变量的密码做综合处理
    name_pass_pair_list = replace_mark_user_on_pass(name_pass_pair_list,
                                                    mark_string=GB_USER_NAME_MARK,
                                                    options_dict=GB_SOCIAL_OPTIONS_DICT)
    output(f"[*] 用户名变量替换完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 进行格式化
    name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
    output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)

    # 写入当前结果
    step += 1
    frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=":")
    write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.replace_mark.pair.txt"), frozen_tuple_list_)

    # 对元组列表进行 中文编码处理
    if GB_CHINESE_ENCODE_CODING:
        name_pass_pair_list = tuple_list_chinese_encode_by_char(name_pass_pair_list,
                                                                coding_list=GB_CHINESE_ENCODE_CODING,
                                                                url_encode=GB_CHINESE_CHAR_URLENCODE,
                                                                de_strip=True,
                                                                only_chinese=GB_ONLY_CHINESE_URL_ENCODE)
        output(f"[*] 中文编码衍生完成 name_pass_pair_list:{len(name_pass_pair_list)}")
        # 进行格式化
        name_pass_pair_list = format_tuple_list(tuple_list=name_pass_pair_list, options_dict=GB_FILTER_TUPLE_OPTIONS)
        output(f"[*] 元组过滤格式化完成 name_pass_pair_list:{len(name_pass_pair_list)}", level=LOG_INFO)
        # 写入当前结果
        step += 1
        frozen_tuple_list_ = frozen_tuple_list(name_pass_pair_list, link_symbol=":")
        write_lines(os.path.join(GB_TEMP_DICT_DIR, f"{mode}.{step}.chinese_encode.pair.txt"), frozen_tuple_list_)
    return name_pass_pair_list


def parse_input():
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)
    # description 程序描述信息
    argument_parser.description = "Based HTTP Packet Login Auto Blasting, And Social Account Password Generation Tool"

    argument_parser.add_argument("-t", "--target_url", default=GB_TARGET_URL,
                                 help=f"Specify the blasting Target url, Default is {GB_TARGET_URL}", )

    argument_parser.add_argument("-U", "--user_name_file", default=GB_USER_NAME_FILE,
                                 help=f"Specifies the username rule file, Default is {GB_USER_NAME_FILE}")
    argument_parser.add_argument("-P", "--user_pass_file", default=GB_USER_PASS_FILE,
                                 help=f"Specifies the password rule file, Default is {GB_USER_PASS_FILE}")

    argument_parser.add_argument("-A", "--user_pass_pair_file", default=GB_USER_PASS_PAIR_FILE,
                                 help=f"Specifies the password rule file, Default is {GB_USER_PASS_PAIR_FILE}")
    argument_parser.add_argument("-a", "--use_pair_file", default=GB_USE_PAIR_FILE, action="store_true",
                                 help=f"Specifies Display Debug Info, Default is {GB_USE_PAIR_FILE}", )

    argument_parser.add_argument("-d", "--debug_flag", default=GB_DEBUG_FLAG, action="store_true",
                                 help=f"Specifies Display Debug Info, Default is {GB_DEBUG_FLAG}", )

    # epilog 程序额外信息
    argument_parser.epilog = f"""更多参数可通过[setting.py]进行配置"""
    return argument_parser


if __name__ == '__main__':
    # 输入参数解析
    parser = parse_input()

    # 输出所有参数
    args = parser.parse_args()
    output(f"[*] 所有输入参数信息: {args}")

    # 通过一个循环将命令行传递的参数直接赋值给相应的全局变量，从而避免了冗余的代码
    # 使用字典解压将参数直接赋值给相应的全局变量
    for param_name, param_value in vars(args).items():
        globals()[f"GB_{str(param_name).upper()}"] = param_value
        # print(f"GB_{key.upper()} = {value}")
        # print(globals()[f"GB_{key.upper()}"])

    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    set_logger(GB_INFO_LOG_FILE, GB_ERR_LOG_FILE, GB_DBG_LOG_FILE, GB_DEBUG_FLAG)

    # GB_TARGET_URL = "http://www.baidu.com"  # 336
    if not GB_USE_PAIR_FILE:
        user_pass_dict = social_rule_handle_in_steps_two_list(GB_TARGET_URL)
    else:
        user_pass_dict = social_rule_handle_in_steps_one_pairs(GB_TARGET_URL)

    output(f"[*] 最终生成账号密码对数量: {len(user_pass_dict)}", level=LOG_INFO)
