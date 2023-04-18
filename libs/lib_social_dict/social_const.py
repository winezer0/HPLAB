#!/usr/bin/env python
# encoding: utf-8

#######################################
SO_NAME_CAPER = "SO_NAME_CAPER",  # 账号首字母大写
SO_NAME_LOWER = "SO_NAME_LOWER",
SO_NAME_UPPER = "SO_NAME_UPPER",

SO_PASS_CAPER = "SO_PASS_CAPER",  # 密码首字母大写
SO_PASS_LOWER = "SO_PASS_LOWER",
SO_PASS_UPPER = "SO_PASS_UPPER",
SO_ONLY_REPL_MARK_PASS = "SO_ONLY_REPL_MARK_PASS",
#######################################
SOCIAL_OPTIONS_DICT = {
    SO_NAME_CAPER: False,  # 用户名首字母大写
    SO_NAME_LOWER: False,  # 用户名全部小写
    SO_NAME_UPPER: False,  # 用户名全部大写
    SO_PASS_CAPER: False,  # 密码 首字母大写（如果密码中有用户名 就密码内的 用户名首字母大写,否则就密码整体首字母大写）
    SO_PASS_LOWER: False,  # 密码用户名 全部小写（如果密码中有用户名 就密码内的 用户名全部小写,否则就密码整体全部小写）
    SO_PASS_UPPER: False,  # 密码用户名 全部大写 （如果密码中有用户名 就密码内的 用户名全部大写,否则就密码整体全部大写）
    SO_ONLY_REPL_MARK_PASS: True  # 仅对 密码中包含用户名变量的密码 进行以上操作
}
#######################################
