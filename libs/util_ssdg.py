#!/usr/bin/env python
# encoding: utf-8
import re

from libs.lib_dyna_rule.dyna_rule_tools import list_to_re_str
from libs.lib_file_operate.file_path import file_is_exist
from libs.lib_log_print.logger_printer import output, LOG_ERROR
from setting_dict import GB_USER_NAME_MARK


def gen_file_names(formar_str, repalce, rule_exact=False, marks="{LEVEL}"):
    file_names = []
    if rule_exact:
        a_file = formar_str.replace(marks, f"{repalce}")
        if file_is_exist(a_file):
            file_names.append(a_file)
        else:
            output(f"[*] 目标文件不存在 {a_file}", level=LOG_ERROR)
    else:
        for level in range(repalce + 1):
            a_file = formar_str.replace(marks, f"{repalce}")
            if file_is_exist(a_file):
                file_names.append(a_file)
    return file_names


# 命中结果转原始规则（做反向变量替换）
def result_rule_classify(hit_str_list,
                         reverse_replace_dict_list,
                         hit_user_file,
                         hit_pass_file,
                         hit_pair_file,
                         hit_const_link
                         ):
    hit_classify = {hit_user_file: [],
                    hit_pass_file: [],
                    hit_pair_file: []
                    }
    for url_str in hit_str_list:
        # 循环替换因变量值为%%键%%
        # ['%%DOMAIN%%': ['www', 'www.baidu.com', 'baidu', 'baidu_com', 'baidu.com', 'www_baidu_com'],
        # '%%PATH%%': []}]  # 需要排除其中的空列表
        for reverse_replace_dict in reverse_replace_dict_list:
            for key, value in reverse_replace_dict.items():
                value = [ele for ele in value if str(ele).strip()]  # 处理[ ]字符
                if value and value != [""]:
                    patter = list_to_re_str(value)
                    url_str = re.sub(patter, key, url_str, count=0)
        name_ = url_str.split(hit_const_link)[0]
        pass_ = url_str.split(hit_const_link)[1]

        # 如果URL中确实存在后缀
        if name_ and name_.strip():
            hit_classify[hit_user_file].append(name_)

        if pass_ and pass_.strip():
            hit_classify[hit_pass_file].append(pass_)

        if url_str and url_str.strip():
            if name_ != pass_:
                hit_classify[hit_pair_file].append(url_str.replace(hit_const_link, ":"))
            else:
                hit_classify[hit_pair_file].append(f"{name_}:{GB_USER_NAME_MARK}")
    return hit_classify


# if __name__ == '__main__':
#     pass
#     hit_result_list = ['admin<-->password',
#                        'baidu<-->password',
#                        'baidu<-->baidu',
#                        ]
#     req_url = "http://baidu.com"
#     # 获取因变量字典用于数据统计
#     current_dependent_dict = set_dependent_var_dict(target_url=req_url,
#                                                     base_dependent_dict=GB_DEPENDENT_VAR_REPLACE_DICT,
#                                                     ignore_ip_format=GB_IGNORE_IP_FORMAT,
#                                                     symbol_replace_dict=GB_SYMBOL_REPLACE_DICT,
#                                                     not_allowed_symbol=GB_NOT_ALLOW_SYMBOL)
#
#     # 分析命中的URL 并返回命中的path部分 path部分是字典 分类包括 后缀、路径、目录、文件
#     hit_classify_dict = result_rule_classify(hit_str_list=hit_result_list,
#                                              reverse_replace_dict_list=[current_dependent_dict],
#                                              hit_user_file=GB_HIT_NAME_FILE,
#                                              hit_pass_file=GB_HIT_PASS_FILE,
#                                              hit_pair_file=GB_HIT_PAIR_FILE,
#                                              hit_const_link=GB_CONST_LINK
#                                              )
#     # 将命中的路径分别写到不同的频率文件中
#     for file_name, path_list in hit_classify_dict.items():
#         auto_make_dir(os.path.dirname(file_name))
#         write_path_list_to_frequency_file(file_path=file_name,
#                                           path_list=path_list,
#                                           encoding='utf-8',
#                                           frequency_symbol="<-->",
#                                           annotation_symbol="#",
#                                           hit_over_write=GB_HIT_OVER_CALC)
#     output(f"[*] 记录命中结果: {len(list(hit_classify_dict.values()))}")
