#!/usr/bin/env python
# encoding: utf-8
# 全局配置文件
# 输入原始报文路径
import pathlib
import time

from libs.lib_args.input_const import *
from libs.lib_file_operate.file_path import auto_make_dir


def init_common(config):
    """
    初始化本程序的通用参数
    :param config:
    :return:
    """
    ############################################################
    # 获取setting.py脚本所在路径作为的基本路径
    config[GB_BASE_DIR] = pathlib.Path(__file__).parent.resolve()
    ##################################################################
    # 版本号配置
    config[GB_VERSION] = "Ver 0.4.2 2023-07-18 12:00"
    ##################################################################
    # 程序开始运行时间  %Y-%m-%d-%H-%M-%S
    config[GB_RUN_TIME] = time.strftime("%Y-%m-%d", time.localtime())
    ##################################################################
    # 是否显示DEBUG级别信息,默认False
    config[GB_DEBUG_FLAG] = False
    ##################################################################
    # 设置日志输出文件路径 #目录不存在会自动创建
    config[GB_LOG_INFO_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_info.log").as_posix()
    config[GB_LOG_DEBUG_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_debug.log").as_posix()
    config[GB_LOG_ERROR_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_error.log").as_posix()


def init_dict(config):
    # 默认调用的流量
    config[GB_TARGET] = "http_packet.txt"
    ##################################################################
    # 排除历史爆破记录的功能
    config[GB_EXCLUDE_FLAG] = True
    # 排除历史爆破文件名称
    config[GB_EXCLUDE_FILE] = "history_file.txt"
    # 记录历史账号密码时的const_sign 的 连接符号 # 无需修改
    config[GB_CONST_LINK] = '<-->'
    ############################################################
    # 账号密码字典文件的格式
    config[GB_NAME_FILE] = config[GB_BASE_DIR].joinpath("dict", "mode1_name.txt")
    config[GB_PASS_FILE] = config[GB_BASE_DIR].joinpath("dict", "mode1_pass.txt")
    # 账号密码对文件命名格式
    config[GB_PAIR_FILE] = config[GB_BASE_DIR].joinpath("dict", "mode2_pairs.txt")
    # 账号密码对文件 连接符号
    config[GB_PAIR_LINK] = ':'
    # 使用账号、密码文件进行爆破
    config[GB_NAME_PASS_FILE] = True
    # 使用账号:密码对文件进行爆破
    config[GB_PAIR_FILE_FLAG] = False
    ##################################################################
    # 设置输出结果文件目录
    config[GB_RESULT_DIR] = config[GB_BASE_DIR].joinpath("result")
    # 一些创建目录的操作
    auto_make_dir(config[GB_RESULT_DIR])
    ##################################################################
    # 作为HTTP报文中 账号、密码 可能的参数名
    config[GB_USERNAME_PARAMS] = ["username", "name", "uname", "loginname", "loginuser",
                                  "LogName", "Account", "userId", "userCode", "User"]
    config[GB_PASSWORD_PARAMS] = ["password", "passwd", "pwd", "loginpass"]

    # 将 账号密码参数对应的参数值 替换为标记字符串,便于后续替换使用
    config[GB_MARK_USERNAME] = '$user$'  # $$$username$$$
    config[GB_MARK_PASSWORD] = '$pass$'  # $$$password$$$
    ############################################################
    # 进行标签格式检查
    config[GB_CHECK_TAGS] = True
    ##################################################################
    # 仅爆破一个账号密码,成功后退出 很少使用
    config[GB_BRUTE_ONE_KEY] = True


def init_http(config):
    # 默认请求头配置
    config[GB_REQ_HEADERS] = {}

    # 对外请求代理
    config[GB_PROXIES] = {
        # "http": "http://127.0.0.1:8080",
        # "https": "http://127.0.0.1:8080",
        # "http": "http://user:pass@10.10.1.10:3128/",
        # "https": "https://192.168.88.1:8080",
        # "http": "socks5://192.168.88.1:1080",
    }

    # 对外请求代超时时间 # URL重定向会严重影响程序的运行时间
    config[GB_TIME_OUT] = 10
    config[GB_SSL_VERIFY] = False
    config[GB_ALLOW_REDIRECTS] = True

    # 最大重试次数
    config[GB_RETRY_TIMES] = 3

    # 最大错误次数
    config[GB_MAX_ERROR_NUM] = 20

    # 默认线程数
    config[GB_THREADS_COUNT] = 30

    # 每个线程之间的延迟 单位S秒
    config[GB_THREAD_SLEEP] = 0.2

    # 任务分块大小 所有任务会被分为多个列表
    config[GB_TASK_CHUNK_SIZE] = config[GB_THREADS_COUNT]

    # 是否是HTTPS协议
    config[GB_PROTOCOL] = None  # HTTPS|HTTP|None 自动识别

    # 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
    config[GB_EXCLUDE_STATUS] = [404, 401, 403, 405, 406, 410, 500, 501, 502, 503]

    # 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
    config[GB_EXCLUDE_REGEXP] = r"页面不存在|未找到|not[ -]found|403|404|410"
