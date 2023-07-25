#!/usr/bin/env python
# encoding: utf-8

from libs.lib_tags_exec.tags_func import func_js2py

# 测试自定义jS脚本是否可以正常调用
if __name__ == '__main__':
    string = "password"
    js_file_path = "libs/lib_tags_exec/demo/custom.js"
    result = func_js2py(string,js_file_path )
    print(f"result:{result}")
