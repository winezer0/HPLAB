import base64
import hashlib
import inspect
import urllib.parse


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


def _function_names_():
    # 获取当前文件中定义的所有函数列表
    current_module = inspect.getmodule(inspect.currentframe())
    functions = inspect.getmembers(current_module, inspect.isfunction)
    function_names = [f[0] for f in functions if f[0] != "_function_names_"]
    return function_names


if __name__ == "__main__":
    print(_function_names_())
