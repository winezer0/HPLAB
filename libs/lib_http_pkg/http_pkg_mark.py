#!/usr/bin/env python
# encoding: utf-8
import sys

from libs.lib_http_pkg.parse_http_pkg import parse_diff_content_type_body_simple, update_http_param_value, \
    parsed_query_params
from libs.lib_http_pkg.parse_tools import list_ele_in_str, freeze_headers, unfreeze_headers
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_ERROR
from libs.lib_tags_exec.tags_exec import match_exec_repl_loop

sys.dont_write_bytecode = True  # 设置不生成pyc文件


# 在参数字典的键中，查找是否有 存在于列表中的键
def search_key_in_list(params_dict={}, key_list=[]):
    for key, value in params_dict.items():
        if list_ele_in_str(list_=key_list, str_=str(key).lower(), default=False):
            return key
    return None


# 查找参数名 并进行标记
def search_and_mark_http_param(req_params,
                               req_path,
                               req_body,
                               req_content_type,
                               search_key_list,
                               mark_repl_string):
    output(f"[*] 查找参数列表: [{search_key_list}] <--> {mark_repl_string}")
    search_key = search_key_in_list(req_params, search_key_list)
    if search_key:
        # 获取请求参数的值 如果值不存在就退出
        if isinstance(req_params[search_key], list):
            search_key_value = req_params[search_key][0]
        else:
            search_key_value = req_params[search_key]
        # 获取参数值
        if not search_key_value:
            output(f"[-] 未发现参数值: 不存在参数[{search_key}]对应的参数值, 如报文中为空值请填充任意值", level=LOG_ERROR)
            return False, req_path, req_body
        output(f"[+] 查找参数成功: {search_key} <--> {search_key_value}", level=LOG_INFO)
    else:
        output(f"[-] 未发现参数名: 所有请求参数[{req_params}]中未发现[{search_key}]", level=LOG_ERROR)
        return False, req_path, req_body

    # 更新请求参数在 请求行 和请求体中的位置
    output(f"[*] 标记HTTP请求包中的[{search_key}]的字段值")
    req_path, req_body = update_http_param_value(req_path=req_path,
                                                 req_body=req_body,
                                                 req_content_type=req_content_type,
                                                 param_key=search_key,
                                                 param_value=search_key_value,
                                                 new_param_value=mark_repl_string)
    return True, req_path, req_body


# 查找参数名 并进行标记
def search_and_get_param_value(req_params,
                               search_key_list):
    output(f"[*] 查找参数列表: [{search_key_list}]")
    search_key = search_key_in_list(req_params, search_key_list)

    # 返回参数值
    if search_key:
        # 获取请求参数的值 如果值不存在就退出
        if isinstance(req_params[search_key], list):
            search_key_value = req_params[search_key][0]
        else:
            search_key_value = req_params[search_key]
        # 获取参数值
        if not search_key_value:
            output(f"[-] 未发现参数值: 不存在参数[{search_key}]对应的参数值, 如报文中为空值请填充任意值", level=LOG_ERROR)
            return None
        else:
            output(f"[+] 查找参数成功: {search_key} <--> {search_key_value}", level=LOG_INFO)
            return search_key_value
    else:
        output(f"[-] 未发现参数名: 所有请求参数[{req_params}]中未发现[{search_key}]", level=LOG_ERROR)
        return None


def parse_http_params(req_path, req_method, req_body, req_content_type):
    params = {}
    params_query = parsed_query_params(req_path)
    # params_query = {} if params_query is None else params_query
    params_query = params_query or {}
    params.update(params_query)
    # 是否需要读取Body数据
    if str(req_method).upper() not in ["GET"] and req_content_type is not None:
        params_body = parse_diff_content_type_body_simple(req_body, req_content_type)
        # params_body = {} if params_body is None else params_body
        params_body = params_body or {}
        params.update(params_body)
    # 对于xml解析出来的参数需要额外处理
    # params:{'root': {'password': 'admin888', 'Login': 'Login', 'user_token': '8f8fac7e0f426fef1d990a648c309a23', 'username': 'admin'}}
    if "xml" in req_content_type:
        for values in list(params.values()):
            if isinstance(values, dict):
                params.update(values)
    output(f"[*] 解析请求参数: {params}", level=LOG_INFO)
    return params


# 替换payload标记
def replace_payload_sign(req_url, req_body, req_headers, mark_repl_str_dict, func_dict):
    # mark_repl_str_dict('$$$username$$$', 'DUIF23fKtnc'), ('$$$password$$$', '2Pqzhn79AAq')

    # 冻结headers
    if req_headers:
        req_headers = freeze_headers(req_headers)

    for mark_string, replace_string in mark_repl_str_dict.items():
        # 判断注入标记是否在URL中
        if mark_string in req_url:
            req_url = req_url.replace(mark_string, replace_string)
        # 判断注入标记是否在Body中
        if req_body and mark_string in req_body:
            req_body = req_body.replace(mark_string, replace_string)
        # 判断注入标记是否在headers中
        if mark_string in req_headers:
            req_headers = req_headers.replace(mark_string, replace_string)

    # 解析 req_url req_body req_headers中的标签
    req_url = match_exec_repl_loop(req_url, func_dict=func_dict)
    req_body = match_exec_repl_loop(req_body, func_dict=func_dict)
    req_headers = match_exec_repl_loop(req_headers, func_dict=func_dict)

    # 修复Body中的换行符
    if req_body and "\r\n" not in req_body and "\n" in req_body:
        req_body = req_body.replace("\n", "\r\n")

    # 恢复headers
    if req_headers:
        req_headers = unfreeze_headers(req_headers)

    return req_url, req_body, req_headers
