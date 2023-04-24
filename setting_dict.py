#!/usr/bin/env python
# encoding: utf-8
import copy
import os
import pathlib
import time

from libs.lib_chinese_pinyin.chinese_const import *
from libs.lib_filter_srting.filter_const import *
from libs.lib_social_dict.social_const import *

############################################################
# 获取setting.py脚本所在路径作为的基本路径
GB_BASE_DIR = pathlib.Path(__file__).parent.resolve()
##################################################################
# 获取setting.py脚本所在路径作为的基本路径
GB_BASE_DIR = pathlib.Path(__file__).parent.resolve()
############################################################
# 基础变量文件夹 里面的每个文件都代表一个替换变量
GB_BASE_VAR_DIR = GB_BASE_DIR.joinpath("dict_base")
# 基础变量字典文件的后缀名列表 通过file.endswith匹配
GB_DICT_SUFFIX = [".txt"]
# 存储 自定义 基本变量
GB_BASE_VAR_REPLACE_DICT = {"%BLANK%": ['']}
###################
# 存储 自定义 因变量
GB_DEPENDENT_VAR_REPLACE_DICT = {"%%DEPENDENT%%": []}
# DOMAIN PATH 因变量中的 符号替换规则, 替换后追加到域名因子列表
GB_SYMBOL_REPLACE_DICT = {":": ["_"], ".": ["_"]}
# 删除带有 特定符号 的因变量（比如:）的元素
GB_NOT_ALLOW_SYMBOL = [":"]
# 忽略IP格式的域名
GB_IGNORE_IP_FORMAT = True
# 手动指定获取域名因变量的域名 # 仅用于单独调用口令生成脚本
GB_TARGET_URL = None
###################
# 指定用户名变量字符串 # 在密码字典中用这个变量表示用户名
GB_USER_NAME_MARK = "%USERNAME%"
############################################################
# 账号密码目录
GB_RULE_DICT_DIR = GB_BASE_DIR.joinpath("dict_rule")
# 账号密码字典
GB_USER_NAME_FILE = os.path.join(GB_RULE_DICT_DIR, f"mode1_name.txt")
GB_USER_PASS_FILE = os.path.join(GB_RULE_DICT_DIR, f"mode1_pass.txt")
###################
# 直接输入账号密码对文件
GB_USER_PASS_PAIR_FILE = os.path.join(GB_RULE_DICT_DIR, f"mode2_name_pass_pair.txt")
# 账号密码对文件 连接符号
GB_PAIR_LINK_SYMBOL = ':'
# 使用账号:密码对文件进行爆破，默认使用账号字典、密码字典
GB_USE_PAIR_FILE = False
# 使用账号:密码对文件进行爆破时,是否进行基础变量替换
GB_USE_PAIR_BASE_REPL = False
############################################################
# 指定记录字典文件的目录
GB_TEMP_DICT_DIR = os.path.join(GB_RULE_DICT_DIR, f"temp.dict.{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}")
############################################################
# 用户名中的中文转拼音处理
GB_CHINESE_TO_PINYIN = True  # 开启中文转拼音的操作
GB_STORE_CHINESE = True  # 保留原始的中文字符串 便于中文用户名的爆破
GB_IGNORE_SYMBOLS = ["%%", "%", "}$"]
###################
# 中文转拼音处理时，通过长度对最后的（账号:密码）进行过滤的依据
GB_USER_NAME_MIN_LEN = 0  # 用户名最小长度（含）
GB_USER_NAME_MAX_LEN = 12  # 用户名最大长度（含）

GB_USER_PASS_MIN_LEN = 0  # 密码最小长度（含）
GB_USER_PASS_MAX_LEN = 12  # 密码最大长度（含）
#######################
# 中文转拼音处理时，对字符串列表处理时的配置字典
# GB_CHINESE_OPTIONS_LIST = copy.copy(PY_BASE_OPTIONS)  # MAX_OPTIONS->最大化配置,不建议使用
# GB_CHINESE_OPTIONS_LIST[PY_FT_MAX_LEN] = GB_USER_NAME_MAX_LEN  # 最终生成的字符串不能超过这个长度
# GB_CHINESE_OPTIONS_LIST[PY_IGNORE_SYMBOL] = GB_IGNORE_SYMBOLS  # 长度过滤时忽略带有这些字符的元素
#######################
# 对账号中依赖的中文处理方案
GB_CHINESE_OPTIONS_NAME = {
    PY_TEMP_SYMBOL: "_",
    PY_LINK_SYMBOLS: [""],
    PY_CN_NAME_MAX_LEN: 4,

    PY_SY_LOWER: True,
    PY_SY_UPPER: False,
    PY_SY_TITLE: False,
    PY_SY_CAPER: False,

    PY_CN_USE_JIEBA: True,

    PY_POSITIVE: True,
    PY_REVERSE: False,
    PY_UNIVERS: True,

    PY_XM2CH: False,
    PY_CH2XM: False,

    PY_FT_NO_BLANK: True,
    PY_FT_NO_DUPL: True,
    PY_FT_MAX_LEN: GB_USER_NAME_MAX_LEN,
    PY_IGNORE_SYMBOL: GB_IGNORE_SYMBOLS,

    PY_NORMAL_UNI: True,
    PY_FIRST_UNI: True,
    PY_INITIALS_UNI: True,

    PY_LOWER_UNI: True,
    PY_UPPER_UNI: False,
    PY_TITLE_UNI: False,
    PY_CAPER_UNI: False,

    PY_NORMAL_XIN: True,
    PY_FIRST_XIN: True,
    PY_INITIALS_XIN: True,

    PY_LOWER_XIN: True,
    PY_UPPER_XIN: False,
    PY_TITLE_XIN: False,
    PY_CAPER_XIN: False,

    PY_NORMAL_MIN: True,
    PY_FIRST_MIN: True,
    PY_INITIALS_MIN: True,

    PY_LOWER_MIN: True,
    PY_UPPER_MIN: False,
    PY_TITLE_MIN: False,
    PY_CAPER_MIN: False,
}
#######################
# 对密码中依赖的中文处理方案
GB_CHINESE_OPTIONS_PASS = {
    PY_TEMP_SYMBOL: "_",
    PY_LINK_SYMBOLS: [""],
    PY_CN_NAME_MAX_LEN: 4,

    PY_SY_LOWER: True,
    PY_SY_UPPER: True,
    PY_SY_TITLE: True,
    PY_SY_CAPER: True,

    PY_CN_USE_JIEBA: True,

    PY_POSITIVE: True,
    PY_REVERSE: False,
    PY_UNIVERS: True,

    PY_XM2CH: False,
    PY_CH2XM: False,

    PY_FT_NO_BLANK: True,
    PY_FT_NO_DUPL: True,
    PY_FT_MAX_LEN: GB_USER_NAME_MAX_LEN,
    PY_IGNORE_SYMBOL: GB_IGNORE_SYMBOLS,

    PY_NORMAL_UNI: True,
    PY_FIRST_UNI: True,
    PY_INITIALS_UNI: True,

    PY_LOWER_UNI: True,
    PY_UPPER_UNI: True,
    PY_TITLE_UNI: True,
    PY_CAPER_UNI: True,

    PY_NORMAL_XIN: True,
    PY_FIRST_XIN: True,
    PY_INITIALS_XIN: True,

    PY_LOWER_XIN: True,
    PY_UPPER_XIN: True,
    PY_TITLE_XIN: True,
    PY_CAPER_XIN: True,

    PY_NORMAL_MIN: True,
    PY_FIRST_MIN: True,
    PY_INITIALS_MIN: True,

    PY_LOWER_MIN: True,
    PY_UPPER_MIN: True,
    PY_TITLE_MIN: True,
    PY_CAPER_MIN: True,
}
#######################
# 中文转拼音处理时，对元组列表处理时的配置字典
# GB_CHINESE_OPTIONS_TUPLE = copy.copy(PY_BASE_OPTIONS)  # MAX_OPTIONS->最大化配置,不建议使用
# GB_CHINESE_OPTIONS_TUPLE[PY_FT_MAX_LEN] = GB_USER_NAME_MAX_LEN * 2  # 最终生成的字符串不能超过这个长度
# GB_CHINESE_OPTIONS_TUPLE[PY_IGNORE_SYMBOL] = GB_IGNORE_SYMBOLS  # 长度过滤时忽略带有这些字符的元素
GB_CHINESE_OPTIONS_TUPLE = copy.copy(GB_CHINESE_OPTIONS_NAME)
GB_CHINESE_OPTIONS_TUPLE[PY_FT_MAX_LEN] = GB_USER_NAME_MAX_LEN * 2
############################################################
# 对生成的账号|密码列表进行排除的选项配置
GB_IGNORE_EMPTY = True  # 进行格式过滤时保留空值[""]
# 排除列表 排除姓名的配置
# GB_FILTER_OPTIONS_NAME = copy.copy(FILTER_STRING_OPTIONS)
GB_FILTER_OPTIONS_NAME = {
    FT_IGNORE_SYMBOLS: GB_IGNORE_SYMBOLS,
    FT_IGNORE_EMPTY: GB_IGNORE_EMPTY,

    FT_NO_DUPLICATE: True,
    FT_BAN_SYMBOLS_STR: [],

    FT_MIN_LEN_STR: GB_USER_NAME_MIN_LEN,
    FT_MAX_LEN_STR: GB_USER_NAME_MAX_LEN,

    # 排除规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXCLUDE_RULES_STR: [
        (0, 0, 0, 1, 0),  # 排除纯符号
        (-1, 1, -1, -1, 1),  # 排除中英文混合 有大写+中文
        (-1, -1, 1, -1, 1),  # 排除中英文混合 有小写+中文
    ],
    # 提取规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXTRACT_RULES_STR: [],

}
#######################
# 排除列表 排除密码的配置
# GB_FILTER_OPTIONS_PASS = copy.copy(FILTER_STRING_OPTIONS)
GB_FILTER_OPTIONS_PASS = {
    FT_IGNORE_SYMBOLS: GB_IGNORE_SYMBOLS,
    FT_IGNORE_EMPTY: GB_IGNORE_EMPTY,

    FT_NO_DUPLICATE: True,
    FT_BAN_SYMBOLS_STR: [],

    FT_MIN_LEN_STR: GB_USER_PASS_MIN_LEN,
    FT_MAX_LEN_STR: GB_USER_PASS_MAX_LEN,

    # 排除规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXCLUDE_RULES_STR: [
        (0, 0, 0, 1, 0),  # 排除仅符号
        (0, 1, 0, 0, 0),  # 排除仅大写
        (0, 1, 0, 1, 0),  # 排除仅大写+符号
        (-1, 1, -1, -1, 1),  # 排除中英文混合 必须有大写+中文
        (-1, -1, 1, -1, 1),  # 排除中英文混合 必须有小写+中文
    ],

    # 提取规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXTRACT_RULES_STR: [],

}
#######################
# 对生成的账号|密码元组进行排除的选项配置
# 排除元组 通过长度
# GB_FILTER_TUPLE_OPTIONS = copy.copy(FILTER_TUPLE_OPTIONS)
GB_FILTER_TUPLE_OPTIONS = {
    FT_IGNORE_SYMBOLS: GB_IGNORE_SYMBOLS,
    FT_IGNORE_EMPTY: GB_IGNORE_EMPTY,

    FT_NO_DUPLICATE: True,

    FT_BAN_SYMBOLS_NAME: [],
    FT_BAN_SYMBOLS_PASS: [],

    FT_MAX_LEN_NAME: GB_USER_NAME_MAX_LEN,
    FT_MIN_LEN_NAME: GB_USER_NAME_MIN_LEN,
    FT_MAX_LEN_PASS: GB_USER_PASS_MAX_LEN,
    FT_MIN_LEN_PASS: GB_USER_PASS_MIN_LEN,

    # 排除规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXCLUDE_RULES_NAME: [
        (0, 0, 0, 1, 0),  # 排除纯符号
    ],
    FT_EXCLUDE_RULES_PASS: [
        (0, 0, 0, 1, 0),  # 排除仅符号
        (0, 1, 0, 0, 0),  # 排除仅大写
        (0, 1, 0, 1, 0),  # 排除仅大写+符号
        (-1, 1, -1, -1, 1),  # 排除中英文混合 必须有大写+中文
        (-1, -1, 1, -1, 1),   # 排除中英文混合 必须有小写+中文
    ],

    # 提取规则 # has_digit, has_upper, has_lower, has_symbol, has_chinese
    FT_EXTRACT_RULES_NAME: [],
    FT_EXTRACT_RULES_PASS: [],
}
############################################################
# 对密码中的用户名替换时候的一些选项
# GB_SOCIAL_OPTIONS_DICT = copy.copy(SOCIAL_OPTIONS_DICT)
GB_SOCIAL_OPTIONS_DICT = {
    SO_NAME_CAPER: False,  # 用户名首字母大写
    SO_NAME_LOWER: True,  # 用户名全部小写
    SO_NAME_UPPER: False,  # 用户名全部大写
    SO_NAME_KEEP: False,  # 当开启用户名格式处理时,依旧保留原始用户名

    SO_PASS_CAPER: False,  # 密码 首字母大写（如果密码中有用户名 就密码内的 用户名首字母大写,否则就密码整体首字母大写）
    SO_PASS_LOWER: False,  # 密码用户名 全部小写（如果密码中有用户名 就密码内的 用户名全部小写,否则就密码整体全部小写）
    SO_PASS_UPPER: False,  # 密码用户名 全部大写 （如果密码中有用户名 就密码内的 用户名全部大写,否则就密码整体全部大写）4
    SO_PASS_KEEP: False,    # 当开启密码格式处理时,依旧保留原始密码

    SO_ONLY_MARK_PASS: False  # 仅对 密码中包含用户名变量的密码 进行以上操作
}
############################################################
# 最后爆破时，对中文账号密码进行进行中文编码
GB_CHINESE_ENCODE_CODING = ["utf-8"]  # 可选 ["utf-8","gb2312","unicode_escape"]
GB_CHINESE_CHAR_URLENCODE = True  # 对中文编码时操作、同时进行URL编码
GB_ONLY_CHINESE_URL_ENCODE = True  # 仅对包含中文的字符串进行中文及URL编码操作
############################################################
