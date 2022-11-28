#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- Time    : 2022/11/28 12:56:41
# -*- Author  : ayunwSky
# -*- File    : t.py
# -*- Desc    : 测试在windows上导入 src/config 目录下的 settings文件
# *******************************************


import sys

sys.path.append(r'e:\codes\gitlab_tools\src\config')
print(sys.path)
print()

import settings
print(settings.LOGGING_DIC)

