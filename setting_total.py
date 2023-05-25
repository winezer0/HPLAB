#!/usr/bin/env python
# encoding: utf-8
# 全局配置文件
# 输入原始报文路径

from libs.lib_file_operate.file_path import auto_make_dir
from setting_dict import *

##################################################################
# 版本号配置
GB_VERSION = "Ver 0.2.1 2023-05-25 02:30"
##################################################################
# 程序开始运行时间  %Y-%m-%d-%H-%M-%S
GB_RUN_TIME = time.strftime("%Y-%m-%d", time.localtime())
##################################################################
# 是否显示DEBUG级别信息,默认False
GB_DEBUG_FLAG = True
##################################################################
# 仅生成字典,不进行爆破
GB_ONLY_GENERATE_DICT = False
##################################################################
# 增加标签处理功能,便于对标记的数据自动进行（加密|编码）操作
# 目前支持功能请查看 libs/lib_tags_exec/tags_const.py 的 TAG_FUNC_DICT
# 标签执行时调用的自定义js文件路径
TAG_EXEC_CUSTOM_JS_FILE = r"libs/lib_tags_exec/demo/custom.js"
# 标签执行时调用的自定义py文件路径
TAG_EXEC_CUSTOM_PY_FILE = r"libs/lib_tags_exec/demo/custom.py"
##################################################################
# 设置日志输出文件路径 #目录不存在会自动创建
GB_LOG_FILE_DIR = GB_BASE_DIR.joinpath("runtime")

GB_LOG_FILE_PATH = GB_LOG_FILE_DIR.joinpath("runtime_module.log")
# GB_LOG_FILE_PATH = GB_LOG_FILE_DIR.joinpath("runtime_{GB_RUN_TIME}_module.log")

GB_INFO_LOG_FILE = str(GB_LOG_FILE_PATH).replace('module', 'info')
GB_DBG_LOG_FILE = str(GB_LOG_FILE_PATH).replace('module', 'debug')
GB_ERR_LOG_FILE = str(GB_LOG_FILE_PATH).replace('module', 'error')
##################################################################
# # 设置输出结果文件目录
# RESULT_FILE_PATH = f"{RESULT_DIR_PATH}/result_{GB_RUN_TIME}.csv"
GB_RESULT_FILE_PATH = "auto"  # auto 根据主机名和时间戳自动生成爆破结果
##################################################################
# 默认调用的流量
GB_HTTP_FILE = "http_packet.txt"
##################################################################
# 对外请求代理
GB_PROXIES = {
    # "http": "http://127.0.0.1:8080",
    # "https": "http://127.0.0.1:8080",
    # "http": "http://user:pass@10.10.1.10:3128/",
    # "https": "https://192.168.88.1:8080",
    # "http": "socks5://192.168.88.1:1080",
}

# 对外请求代超时时间 # URL重定向会严重影响程序的运行时间
GB_TIMEOUT = 10
GB_SSL_VERIFY = False
GB_ALLOW_REDIRECTS = True

# 最大重试次数
GB_RETRY_TIMES = 3

# 默认线程数
GB_THREADS_COUNT = 30
# 每个线程之间的延迟 单位S秒
GB_THREAD_SLEEP = 0.2
# 任务分块大小 所有任务会被分为多个列表
GB_TASK_CHUNK_SIZE = GB_THREADS_COUNT
############################################################
# 作为HTTP报文中 账号、密码 可能的参数名
GB_USERNAME_PARAMS = ["username", "name", "uname", "loginname", "loginuser",
                      "LogName", "Account", "userId", "userCode", "User"]
GB_PASSWORD_PARAMS = ["password", "passwd", "pwd", "loginpass"]

# 将 账号密码参数对应的参数值 替换为标记字符串,便于后续替换使用
GB_MARK_USERNAME = '$user$'  # $$$username$$$
GB_MARK_PASSWORD = '$pass$'  # $$$password$$$
############################################################
# 进行标签格式检查
GB_CHECK_TAGS = True
############################################################
# 是否是HTTPS协议
GB_PROTOCOL = "AUTO"  # HTTPS|HTTP|AUTO

# 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
GB_EXCLUDE_STATUS = [404, 401, 403, 405, 406, 410, 500, 501, 502, 503]

# 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
GB_EXCLUDE_REGEXP = r"页面不存在|未找到|not[ -]found|403|404|410"
############################################################
# 最大错误次数
GB_MAX_ERROR_NUM = 20
############################################################
# 仅爆破一个账号密码,成功后退出 很少使用
GB_ONLY_BRUTE_ONE_PASS = True
############################################################
# 一些创建目录的操作
auto_make_dir(GB_RESULT_DIR)
auto_make_dir(GB_TEMP_DICT_DIR)
# auto_make_dir(GB_BASE_VAR_DIR)
# auto_make_dir(GB_BASE_DYNA_DIR)
# auto_make_dir(GB_BASE_NAME_DIR)
# auto_make_dir(GB_BASE_PASS_DIR)
# auto_make_dir(GB_RULE_DICT_DIR)
############################################################
