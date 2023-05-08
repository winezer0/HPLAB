import base64
import hashlib
import inspect
import urllib.parse
import js2py

from libs.lib_file_operate.file_path import file_is_exist
from libs.lib_file_operate.file_read import read_file_to_str
from libs.lib_log_print.logger_printer import output, LOG_ERROR
from setting_total import TAG_EXEC_CUSTOM_JS_FILE


def base64_encode(string=""):
    # base64编码
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def base64_safe_encode(string=""):
    # URL安全的Base64编码
    base64url = base64.urlsafe_b64encode(string.encode("utf-8"))
    base64url = base64url.rstrip(b'=')
    return base64url.decode("utf-8")


def md5_encode(string=""):
    # md5值计算
    return hashlib.md5(string.encode(encoding='utf-8')).hexdigest()


def url_encode(string=""):
    # url编码
    return urllib.parse.quote(string)


def none_encode(string=""):
    # 原样返回
    return string


def str_upper(string=""):
    # 全部大写
    return str(string).upper()


def str_lower(string=""):
    # 全部小写
    return str(string).lower()


def str_capitalize(string=""):
    # 首字母大写
    return str(string).capitalize()


def func_js2py(string=""):
    # 动态调用js代码进行执行
    js_file_path = TAG_EXEC_CUSTOM_JS_FILE
    if file_is_exist(js_file_path):
        js_func_code = read_file_to_str(js_file_path, encoding=None, de_strip=False, de_unprintable=False)
        try:
            js2py_func = js2py.eval_js(js_func_code)
            return js2py_func(string)
        except Exception as error:
            output(f"[!]  JS FILE [{js_file_path}] EVAL ERROR!!! {str(error)}", level=LOG_ERROR)
    else:
        output(f"[!] JS FILE [{js_file_path}] NOT FOUND !!!", level=LOG_ERROR)
        exit()


def _function_names_():
    # 获取当前文件中定义的所有函数列表
    current_module = inspect.getmodule(inspect.currentframe())
    functions = inspect.getmembers(current_module, inspect.isfunction)
    function_names = [f[0] for f in functions if f[0] != "_function_names_"]
    return function_names


if __name__ == "__main__":
    print(_function_names_())
