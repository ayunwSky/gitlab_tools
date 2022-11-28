#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- Time    : 2022/11/28 10:24:56
# -*- Author  : ayunwSky
# -*- File    : src.py
# -*- Desc    :
# *******************************************


from src.config import settings

from logging import config, getLogger

"""
import logging.config  # 等同于 from logging import config

如果用的是 import logging.config, 则使用的时候用 logging.config.dictConfig
如果用的是 from logging import config, 则使用的时候用 config.dictConfig
"""


# 加载配置
config.dictConfig(settings.LOGGING_DIC)
# 获取日志的生产者,也就是 loggers 下面的名字
logger1 = getLogger("access_console_log")
logger2 = getLogger("console_log")
# 使用 __name__ ，而不指定loggers 下面的名字，则会使用 loggers 下的 '' 的这个handlers
# 最终将日志输出到 default 和 console
logger3 = getLogger(__name__)

# 产生日志
logger1.info("这是 logger1 产生的一条测试的 info 级别日志!")

logger2.info("这是 logger2 产生的一条测试的 info 级别日志!")

logger3.info("这是 logger3 产生的一条测试的 info 级别日志!")
