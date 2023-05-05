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
from libs.lib_file_operate.file_path import get_dir_path_file_info_dict, file_name_remove_ext_list, \
    get_dir_path_dir_info_dict


# 查找重复元素
def find_duplicates(string_list):
    # 使用一个集合来保存已经出现过的元素
    seen = set()
    # 使用一个列表来保存重复的元素
    duplicates = []
    for item in string_list:
        # 如果元素已经在集合中出现过，说明是重复元素
        if item in seen:
            # 将重复元素添加到列表中
            duplicates.append(item)
        else:
            # 将元素添加到集合中
            seen.add(item)
    return duplicates


# 列表去重并保持原始顺序
def unique_list(string_list):
    unique_lst = []
    seen = set()
    for item in string_list:
        if item not in seen:
            seen.add(item)
            unique_lst.append(item)
    return unique_lst


# 进行小写处理
def lower_list(string_list):
    for index, string in enumerate(string_list):
        string_list[index] = str(string).lower()
    return string_list


# 对目录下的文件进行小写和去重处理
def format_dict_dirs(dirs):
    for base_var_dir, ext_list in dirs.items():
        file_info_dict = get_dir_path_file_info_dict(base_var_dir, ext_list=ext_list)
        print(f"[*] DIR:{base_var_dir} -> SUFFIX: {ext_list}")
        print(f"[*] FILES : {list(file_info_dict.values())}")

        for file_name, file_path in file_info_dict.items():
            pure_name = file_name_remove_ext_list(file_name, ext_list)
            # 读文件到列表
            file_content = read_file_to_list(file_path,
                                             encoding=file_encoding(file_path),
                                             de_strip=True,
                                             de_weight=True,
                                             de_unprintable=True)

            if file_content:
                new_content_list = lower_list(file_content)
                new_content_list = unique_list(new_content_list)
                if len(file_content) != len(new_content_list):
                    print(f"[*] 有效变量名: {f'%{pure_name}%'}")
                    print(f"[*] 变量名内容: {file_content}")
                    write_lines(file_path, new_content_list, encoding="utf-8", new_line=True, mode="w+")
                    print(f"[+] 成功格式化: {file_path}")
                else:
                    print(f"[*] 跳过格式化: {file_path}")


# 检查基本变量是否重复
def check_duplicates_var(dirs):
    name_dirs = copy.copy(dirs)
    del name_dirs[GB_BASE_PASS_DIR]

    pass_dirs = copy.copy(dirs)
    del pass_dirs[GB_BASE_NAME_DIR]

    dirs_list = [name_dirs, pass_dirs]

    for temp_dirs in dirs_list:
        # 分析是否存在重复文件名
        all_file_list = []
        all_file_dict = {}
        for base_var_dir, ext_list in temp_dirs.items():
            file_info_dict = get_dir_path_file_info_dict(base_var_dir, ext_list=ext_list)
            # print(f"[*] file_info_dict: {base_var_dir}:{file_info_dict.keys()}")
            all_file_list.extend(list(file_info_dict.keys()))
            all_file_dict[base_var_dir] = list(file_info_dict.keys())
        duplicates_file_list = find_duplicates(all_file_list)
        if duplicates_file_list:
            print(f"[-] 发现重复文件|建议修改名称: {duplicates_file_list}")
            # 反向查找文件所在目录
            for duplicates_file in duplicates_file_list:
                for k, v in all_file_dict.items():
                    if duplicates_file in v:
                        print(f"[-] 重复文件 {duplicates_file} 位于 {k}")
        else:
            print(f"[*] 未发现重复文件...{list(temp_dirs.keys())}")

        # 分析是否存在重复目录
        all_dir_list = []
        all_dir_dict = {}
        for base_var_dir, ext_list in temp_dirs.items():
            dir_info_dict = get_dir_path_dir_info_dict(base_var_dir)
            # print(f"[*] dir_info_dict: {base_var_dir}:{dir_info_dict.keys()}")
            all_dir_list.extend(list(dir_info_dict.keys()))
            all_dir_dict[base_var_dir] = list(dir_info_dict.keys())
        duplicates_dir_list = find_duplicates(all_dir_list)
        if duplicates_dir_list:
            print(f"[-] 发现重复目录|建议修改名称: {duplicates_dir_list}")
            # 反向查找文件所在目录
            for duplicates_dir in duplicates_dir_list:
                for k, v in all_dir_dict.items():
                    if duplicates_dir in v:
                        print(f"[-] 重复目录 {duplicates_dir} 位于 {k}")
        else:
            print(f"[*] 未发现重复目录...{list(temp_dirs.keys())}")

        # 分析是否存在目录和文件名重复的情况
        for dir_var in all_dir_list:
            for file_var in all_file_list:
                if str(dir_var) in str(file_var):
                    print(f"[-] 发现重复目录文件|建议修改名称: {dir_var} <--> {file_var}")
        else:
            print(f"[*] 未发现重复目录文件...{list(temp_dirs.keys())}")


if __name__ == '__main__':
    all_dirs = {
        GB_BASE_VAR_DIR: GB_DICT_SUFFIX,
        GB_BASE_DYNA_DIR: GB_DICT_SUFFIX,
        GB_BASE_NAME_DIR: GB_DICT_SUFFIX,
        GB_BASE_PASS_DIR: GB_DICT_SUFFIX
    }

    # 格式化所有文件
    format_dict_dirs(all_dirs)

    # 判断是否存在重复的属性名称,不能够存在重复【文件名|目录名】的
    # 如果存在目录和文件名相同也需要警告
    check_duplicates_var(all_dirs)
