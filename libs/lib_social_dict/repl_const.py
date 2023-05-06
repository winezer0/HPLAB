#!/usr/bin/env python
# encoding: utf-8

#######################################
SO_NAME_KEEP = "SO_NAME_KEEP"  # 保留原始用户名

# SO_NAME_CAPER = "SO_NAME_CAPER"  # 账号首字母大写
# SO_NAME_LOWER = "SO_NAME_LOWER"
# SO_NAME_UPPER = "SO_NAME_UPPER"
SO_NAME_CASE = "SO_NAME_CASE"

SO_PASS_KEEP = "SO_PASS_KEEP"  # 保留原始密码名
# SO_PASS_CAPER = "SO_PASS_CAPER"  # 密码首字母大写
# SO_PASS_LOWER = "SO_PASS_LOWER"
# SO_PASS_UPPER = "SO_PASS_UPPER"
SO_PASS_CASE = "SO_PASS_CASE"

SO_ONLY_MARK_PASS = "SO_ONLY_MARK_PASS"
#######################################
# 额外的密码处理参数
SO_PASS_REPL = "SO_PASS_REPL"  # 进行密码字符替换,如 password -> passw0rd
SO_PASS_SEGMENT = "SO_PASS_SEGMENT"  # 进行密码按字母段索引进行大小处理,如 pass@word -> PASS@word
SO_PASS_INDEXED = "SO_PASS_INDEXED"  # 进行密码按字母索引进行大小处理,如 password -> pAssword
#######################################
SOCIAL_USER_OPTIONS_DICT = {
    # SO_NAME_CAPER: False,  # 用户名首字母大写
    # SO_NAME_LOWER: True,  # 用户名全部小写
    # SO_NAME_UPPER: False,  # 用户名全部大写
    SO_NAME_CASE:["lower"],
    SO_NAME_KEEP: False,  # 对用户名进行格式化时, 保留原始用户名

    # SO_PASS_CAPER: False,  # 密码 首字母大写（如果密码中有用户名 就密码内的 用户名首字母大写,否则就密码整体首字母大写）
    # SO_PASS_LOWER: False,  # 密码 全部小写（如果密码中有用户名 就密码内的 用户名全部小写,否则就密码整体全部小写）
    # SO_PASS_UPPER: False,  # 密码 全部大写 （如果密码中有用户名 就密码内的 用户名全部大写,否则就密码整体全部大写）
    SO_PASS_CASE: [],
    SO_PASS_KEEP: True,  # 对密码进行格式化时, 保留原始密码

    SO_ONLY_MARK_PASS: True,  # 仅对 包含用户名变量标记的密码 进行密码格式处理操作
}
#######################################
SOCIAL_PASS_OPTIONS_DICT = {
    SO_PASS_KEEP: True,  # 对密码进行格式化时, 保留原始密码

    SO_PASS_REPL: [  # 密码字符替换
        # {"o": "0"},
        # {"o": "@"},
    ],

    SO_PASS_SEGMENT: [  # 密码字母按段索引大小写
        # {0: "upper"},
        # {1: "upper"},
        # {0: "upper", 1: "upper"},
        # {0: "upper", 2: "upper"},
        # {0: "upper", "*": "lower"},
    ],

    SO_PASS_INDEXED: [  # 密码字母按字母索引大小写
        # {1:"upper","*":"lower"},
        # {0: "upper", "*": "lower"},
        # {-1: "lower", "*": "u"},
    ],

}
#######################################