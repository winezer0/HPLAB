#!/usr/bin/env python
# encoding: utf-8
import argparse
from pyfiglet import Figlet
from libs.lib_args.input_const import *
from libs.lib_args.input_basic import StoreReverse, extract_heads
from libs.lib_log_print.logger_printer import output, LOG_ERROR


def args_parser(config_dict):
    # RawDescriptionHelpFormatter 支持输出换行符
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)

    # description 程序描述信息
    argument_parser.description = Figlet().renderText("HPLAB")

    # 动态实现重复参数设置代码  # 可提取到函数外正常使用
    # 规则示例: { "param": "", "dest": "","name": "", "default": "", "nargs": "","action": "",  "choices": "", "type": "","help": ""}
    args_options = [
        # 指定请求报文
        {"param": GB_TARGET, "help": f"指定请求报文"},
        # 指定请求协议
        {"param": GB_PROTOCOL, "help": "指定请求协议"},

        # 控制使用账号、密码字典
        {"param": GB_NAME_PASS_FILE, "action": StoreReverse, "help": "开关 使用[账号+密码]字典"},
        # 控制使用账号密码对字典
        {"param": GB_PAIR_FILE_FLAG, "action": StoreReverse, "help": "开关 使用[账号密码对]字典"},
        # 指定请求代理服务
        {"param": GB_PROXIES, "help": "指定请求代理服务 http|https|socks5"},
        # 指定请求线程数量
        {"param": GB_THREADS_COUNT, "type": int, "help": "指定请求线程数量"},

        # 指定请求超时时间
        {"param": GB_TIME_OUT, "type": int, "help": "指定请求超时时间"},
        # 指定自动错误重试次数
        {"param": GB_RETRY_TIMES, "type": int, "help": "指定自动错误重试次数"},

        # 指定账号文件
        {"param": GB_NAME_FILE, "help": f"指定账号文件"},
        # 指定密码文件
        {"param": GB_PASS_FILE, "help": f"指定密码文件"},
        # 指定口令对文件
        {"param": GB_PAIR_FILE, "help": f"指定口令对文件"},
        # 指定口令对分隔符
        {"param": GB_PAIR_LINK, "help": f"指定口令对分隔符"},

        # 开启调试功能
        {"param": GB_DEBUG_FLAG, "action": StoreReverse, "help": "开关 调试信息显示"},

    ]

    param_dict = {"help": "h"}  # 存储所有长-短 参数对应关系,用于自动处理重复的短参数名
    options_to_argument(args_options, argument_parser, config_dict, param_dict)

    # 其他输出信息
    shell_name = argument_parser.prog
    argument_parser.epilog = f"""Version: {config_dict[GB_VERSION]}"""

    args = argument_parser.parse_args()
    return args


def args_dict_handle(args):
    # 记录已经更新过的数据
    update_dict = {}
    # 格式化输入的Proxy参数 如果输入了代理参数就会变为字符串
    if args.proxies and isinstance(args.proxies, str):
        if "socks" in args.proxies or "http" in args.proxies:
            args.proxies = {
                'http': args.proxies.replace('https://', 'http://'),
                'https': args.proxies.replace('https://', 'http://')
            }
            update_dict["proxies"] = args.proxies
        else:
            output(f"[!] 输入的代理地址[{args.proxies}]不正确,正确格式:Proto://IP:PORT", level=LOG_ERROR)
    return update_dict


def config_dict_handle(config_dict):
    # 记录已经更新过的数据
    update_dict = {}
    return update_dict


def options_to_argument(args_options, argument_parser, config_dict, param_dict):
    """
    将参数字典转换为参数选项  与全局变量有关,最好放在同一个文件
    :param args_options:
    :param argument_parser:
    :param config_dict:
    :param param_dict: 全局变量<-->短参数对应关系字典
    :return:
    """
    support_list = ["param", "dest", "name", "default", "nargs", "action", "choices", "type", "help"]
    for option in args_options:
        # 跳过空字典
        if not option:
            continue

        try:
            # 使用 issubset() 方法判断字典的所有键是否都是列表 support_list 的子集
            if not set(option.keys()).issubset(support_list):
                not_allowed_keys = set(option.keys()) - set(support_list)
                output(f"[!] 参数选项:[{option}]存在非预期参数[{not_allowed_keys}]!!!", level=LOG_ERROR)
            else:
                gb_param = option["param"]
                tmp_dest = vars_to_param(gb_param) if "dest" not in option.keys() else option["dest"]
                tmp_name = extract_heads(tmp_dest, param_dict) if "name" not in option.keys() else option["name"]
                tmp_default = config_dict[gb_param] if "default" not in option.keys() else option["default"]
                tmp_nargs = None if "nargs" not in option.keys() else option["nargs"]
                tmp_action = None if "action" not in option.keys() else option["action"]
                tmp_help = f"Specify the {vars_to_param(gb_param)}" if "help" not in option.keys() else option["help"]
                tmp_type = None if "type" not in option.keys() else option["type"]
                tmp_choices = None if "choices" not in option.keys() else option["choices"]

                # 存储长短参数对应关系
                param_dict[gb_param] = tmp_name

                if tmp_action:
                    argument_parser.add_argument(f"-{tmp_name.strip('-')}",
                                                 f"--{tmp_dest.strip('-')}",
                                                 default=tmp_default,
                                                 action=tmp_action,
                                                 # type=tmp_type,  # type 互斥 action
                                                 # nargs=tmp_nargs,  # type 互斥 action
                                                 # choices=tmp_choices,
                                                 help=f"{tmp_help}. 默认值 [{tmp_default}]. 默认动作 [{tmp_action}].",
                                                 )
                else:
                    # 当设置nargs参数时, 不能设置action, 需要分别设置
                    argument_parser.add_argument(f"-{tmp_name.strip('-')}",
                                                 f"--{tmp_dest.strip('-')}",
                                                 default=tmp_default,
                                                 nargs=tmp_nargs,
                                                 type=tmp_type,
                                                 choices=tmp_choices,
                                                 help=f"{tmp_help}. 默认值 [{tmp_default}].",
                                                 )
        except Exception as error:
            output(f"[!] 参数选项 {option} 解析发生错误, ERROR:{error}", level=LOG_ERROR)
            exit()


def vars_to_param(var_name):
    # 与全局变量有关,最好放在同一个文件
    # 实现全局变量到参数名的自动转换,和 config_dict_add_args中的修改过程相反
    # 基于变量的值实现，要求 变量="变量", 如:GB_PROXIES="GB_PROXIES"
    # param_name = str(var_name).replace("GB_", "").lower()
    # 基于变量名的更通用的实现, 要求变量是全局变量.
    param_name = str(globals()[var_name]).replace("GB_", "").lower()
    return param_name
