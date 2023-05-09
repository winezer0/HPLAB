#!/usr/bin/env python
# encoding: utf-8

from libs.lib_tags_exec.tags_func import func_mypy
from setting_total import TAG_EXEC_CUSTOM_PY_FILE

# 测试自定义PY脚本是否可以正常调用
if __name__ == '__main__':
    string = "password"
    py_file_path = TAG_EXEC_CUSTOM_PY_FILE
    result = func_mypy(string, py_file_path)
    print(f"result:{result}")
