# -*- coding: utf-8 -*-

import copy

# 离线翻译字典
from libs.lib_chinese_pinyin.chinese_const import PY_SY_LOWER, PY_SY_UPPER, PY_SY_TITLE, PY_SY_CAPER, PY_OPTIMIZED
from libs.lib_chinese_pinyin.chinese_string_handle import gen_chinese_to_pinyin_mark_dict


# 优化离线翻译字典处理  目前为空
def optimize_translate_dict(translate_dict,
                            options_dict,
                            deep_copy=False):
    # 判断字典是否包含optimized记录
    if PY_OPTIMIZED in translate_dict.keys():
        return translate_dict

    if deep_copy:
        translate_dict = copy.copy(translate_dict)

    # 支持全部大小写、首字母大小写等
    for key, value in translate_dict.items():
        new_value = copy.copy(value)
        for v in value:
            if options_dict[PY_SY_LOWER]:
                new_value.append(str(v).lower())
            if options_dict[PY_SY_UPPER]:
                new_value.append(str(v).upper())
            if options_dict[PY_SY_TITLE]:
                # v.title() 将字符串中每个单词的首字母都变成大写字母
                new_value.append(str(v).title())
            if options_dict[PY_SY_CAPER]:
                # v.capitalize() 只将字符串的第一个字符变成大写字母，
                new_value.append(str(v).capitalize())
        # 更新列表值
        if new_value:
            translate_dict[key] = list(set(new_value))

    # 优化完成记录
    translate_dict[PY_OPTIMIZED] = PY_OPTIMIZED
    return translate_dict


# 生成 专业术语 替换字典的 替换字典
def gen_translate_replace_dict(translate_dict):
    # 生成 键的替换字典
    chinese_word_list = list(translate_dict.keys())
    chinese_to_pinyin_key_dict = gen_chinese_to_pinyin_mark_dict(chinese_word_list)
    # print(chinese_to_pinyin_key_dict)   # {'管理员': '%%guan_li_yuan%%', '用户名': '%%yong_hu_ming%%', ...}

    # 生成 值的替换字典
    pinyin_key_to_value_list_dict = {}
    for chinese_key, chinese_key_pinyin in chinese_to_pinyin_key_dict.items():
        pinyin_key_to_value_list_dict[chinese_key_pinyin] = translate_dict[chinese_key]
    # print(pinyin_key_to_value_list_dict) # {'%%guan_li_yuan%%': ['admin', 'administrator', 'manager', ...']

    return chinese_to_pinyin_key_dict, pinyin_key_to_value_list_dict
