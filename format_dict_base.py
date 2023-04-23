#!/usr/bin/env python
# encoding: utf-8
from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_write import write_lines
from setting_total import *

"""
1、循环读取dict_base下的所有文件
2、基本元素进行格式化 【全部小写、去重、】
"""
from libs.lib_file_operate.file_path import get_dir_path_file_name


def format_string_list(string_list):
    for index,string in enumerate(string_list):
        string_list[index]=str(string).lower()
    return string_list


def format_dir(base_var_dir, ext_list):
    base_var_file_list = get_dir_path_file_name(base_var_dir, ext_list=ext_list)
    print(base_var_file_list)

    for base_var_file_name in base_var_file_list:
        base_file_pure_name = os.path.basename(base_var_file_name)
        base_var_name = f'%{base_file_pure_name}%'

        # 读文件到列表
        base_var_file_path = os.path.join(base_var_dir, base_var_file_name)
        base_var_file_content = read_file_to_list(base_var_file_path,
                                                  encoding=file_encoding(base_var_file_path),
                                                  de_strip=True,
                                                  de_weight=True,
                                                  de_unprintable=True)
        new_content_list = format_string_list(base_var_file_content)
        write_lines(base_var_file_path, new_content_list, encoding="utf-8", new_line=True, mode="w+")
        print(f"[+] 格式化成功...{base_var_file_path}")


if __name__ == '__main__':
    format_dir(GB_BASE_VAR_DIR, GB_DICT_SUFFIX)
