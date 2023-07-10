import inspect

######################################################
# 默认参数相关
GB_BASE_DIR = ""
GB_RUN_TIME = ""
GB_VERSION = ""
GB_DEBUG_FLAG = ""

# 日志路径相关
GB_LOG_INFO_FILE = ""
GB_LOG_DEBUG_FILE = ""
GB_LOG_ERROR_FILE = ""

# 结果文件路径
GB_RESULT_DIR = ""
######################################################
# 自定义输入参数相关
GB_EXCLUDE_FLAG = ""
GB_EXCLUDE_FILE = ""
GB_CONST_LINK = ""
GB_TARGET = ""
GB_NAME_FILE = ""
GB_PASS_FILE = ""
GB_PAIR_FILE = ""
GB_PAIR_LINK = ""
GB_NAME_PASS_FILE = ""
GB_PAIR_FILE_FLAG = ""
GB_USERNAME_PARAMS = ""
GB_PASSWORD_PARAMS = ""
GB_MARK_USERNAME = ""
GB_MARK_PASSWORD = ""
GB_CHECK_TAGS = ""
GB_BRUTE_ONE_KEY = ""
######################################################
GB_REQ_HEADERS = ""
GB_TIME_OUT = ""
GB_PROXIES = ""
GB_SSL_VERIFY = ""
GB_ALLOW_REDIRECTS = ""
GB_RETRY_TIMES = ""
GB_THREADS_COUNT = ""
GB_THREAD_SLEEP = ""
GB_TASK_CHUNK_SIZE = ""
GB_PROTOCOL = ""
GB_EXCLUDE_STATUS = ""
GB_EXCLUDE_REGEXP = ""
GB_MAX_ERROR_NUM = ""


######################################################


# 实现自动更新全局变量名和对应值
def update_global_vars(startswith="GB_", require_blank=True, debug=False):
    # 修改所有全局变量名的值为变量名字符串
    # 当前本函数必须放置到本目录内才行

    def get_var_string(variable):
        # 自动根据输入的变量,获取变量名的字符串
        # 获取全局变量字典
        global_vars = globals()

        # 遍历全局变量字典
        for name, value in global_vars.items():
            if value is variable:
                # print(f"[*] global_vars <--> {variable} <--> {name} <--> {value}")
                return name

        # 获取局部变量字典
        local_vars = locals()
        # 遍历局部变量字典
        for name, value in local_vars.items():
            if value is variable:
                # print(f"[*] local_vars <--> {variable} <--> {name} <--> {value}")
                return name

        return None  # 如果未找到对应的变量名，则返回 None

    def get_global_var_names():
        # 获取本文件所有全局变量名称, 排除函数名等
        global_var_names = list(globals().keys())
        # 获取当前文件中定义的所有函数列表
        current_module = inspect.getmodule(inspect.currentframe())
        functions = inspect.getmembers(current_module, inspect.isfunction)
        function_names = [f[0] for f in functions]
        # 在本文件所有全局变量排除函数列表
        global_var_names = [name for name in global_var_names
                            if name not in function_names  # 排除内置函数名
                            and name.count("__") < 2  # 排除内置__name__等变量
                            and name != "inspect"  # 排除内置inspect包的变量
                            ]

        # 仅处理以 startswith 开头的变量
        if startswith:
            global_var_names = [name for name in global_var_names if name.startswith(startswith)]

        return global_var_names

    for variable_name in get_global_var_names():
        # 仅处理空变量
        if require_blank and globals()[variable_name]:
            if debug:
                print(f"跳过 Name:{variable_name} <--> Value: {globals()[variable_name]}")
            continue

        globals()[variable_name] = "NONE"
        globals()[variable_name] = get_var_string(globals()[variable_name])
        if debug:
            print(f"更新 Name:{variable_name} <--> Value: {globals()[variable_name]}")


# 自动更新变量的值为变量名字符串 # 必须放在末尾
update_global_vars(startswith="GB_", require_blank=True, debug=False)
