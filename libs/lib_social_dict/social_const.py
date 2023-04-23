#!/usr/bin/env python
# encoding: utf-8

#######################################
SO_NAME_KEEP = "SO_NAME_KEEP"  # 保留原始用户名
SO_NAME_CAPER = "SO_NAME_CAPER"  # 账号首字母大写
SO_NAME_LOWER = "SO_NAME_LOWER"
SO_NAME_UPPER = "SO_NAME_UPPER"

SO_PASS_KEEP = "SO_PASS_KEEP"  # 保留原始密码名
SO_PASS_CAPER = "SO_PASS_CAPER"  # 密码首字母大写
SO_PASS_LOWER = "SO_PASS_LOWER"
SO_PASS_UPPER = "SO_PASS_UPPER"

SO_ONLY_MARK_PASS = "SO_ONLY_MARK_PASS"
#######################################
SOCIAL_OPTIONS_DICT = {
    SO_NAME_CAPER: False,  # 用户名首字母大写
    SO_NAME_LOWER: True,  # 用户名全部小写
    SO_NAME_UPPER: False,  # 用户名全部大写
    SO_NAME_KEEP: False,  # 对用户名进行格式化时, 保留原始用户名

    SO_PASS_CAPER: False,  # 密码 首字母大写（如果密码中有用户名 就密码内的 用户名首字母大写,否则就密码整体首字母大写）
    SO_PASS_LOWER: False,  # 密码 全部小写（如果密码中有用户名 就密码内的 用户名全部小写,否则就密码整体全部小写）
    SO_PASS_UPPER: False,  # 密码 全部大写 （如果密码中有用户名 就密码内的 用户名全部大写,否则就密码整体全部大写）
    SO_PASS_KEEP: True,  # 对密码进行格式化时, 保留原始密码

    SO_ONLY_MARK_PASS: True  # 仅对 密码中包含用户名变量标记的密码 进行密码格式处理操作
}
#######################################
