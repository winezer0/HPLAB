#!/usr/bin/env python
# encoding: utf-8

from libs.lib_tags_exec.tags_func import func_mypy

# 测试自定义PY脚本是否可以正常调用
if __name__ == '__main__':
    string = "password"
    py_file_path = "libs/lib_tags_exec/demo/custom.py"
    result = func_mypy(string, py_file_path)
    print(f"result:{result}")
