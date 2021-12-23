# -*- coding=utf8 -*-
"""
# @Author       : jizhongxian@baidu.com
# @Created Time : 2021-12-13 12:06:27
# @Description  : 开发期间用于调试的一些函数
"""

import os
from sys import stderr

IS_DEBUG = True if os.getenv("DEBUG_MODE", None) else False

if IS_DEBUG:
    stderr.write("\033[1;36mDEBUG MODE IS ON\033[0m\n")
    stderr.flush()

if __name__ == "__main__":
    print(IS_DEBUG)
