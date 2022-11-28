#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- Time    : 2022/11/28 09:22:39
# -*- Author  : ayunwSky
# -*- File    : settings.py
# *******************************************


import os
from pathlib import Path
# pip3 install python-dotenv
from dotenv import find_dotenv, load_dotenv

# # 方法一: 定义log文件的目录
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# LOG_PATH = os.path.join(BASE_DIR, 'logs')

# 方法二: 定义log文件的目录

# 以下表示当前目录的上一级目录
BASE_DIR = Path(__file__).resolve().parent.parent
# 以下表示当前目录
# BASE_DIR = Path(__file__).resolve().parent

LOG_PATH = BASE_DIR.parent / 'logs'

# 加载当前路径下的 .env 环境变量文件
ENVFILE_PATH = Path('.') / '.env'
load_dotenv(dotenv_path=ENVFILE_PATH, verbose=True)

# 如果不存在定义的日志目录就创建
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# log文件的全路径
BOSS_LOGFILE = LOG_PATH / 'boss.log'
ACCESS_LOGFILE = LOG_PATH / 'access.log'
DEFAULT_LOGFILE = LOG_PATH / 'default.log'
TIMED_ACCESS_LOGFILE = LOG_PATH / 'access_timed.log'

# 2、定义日志格式
standard_format = '[%(asctime)s] - [%(levelname)s] - [%(threadName)s:%(thread)d] - [task_id:%(name)s] ' \
                  '- [%(filename)s:%(lineno)d]: %(message)s'

simple_format = '[%(asctime)s] - [%(levelname)s] - [%(filename)s:%(lineno)d]: %(message)s'

test_format = '[%(asctime)s] - [%(levelname)s]: %(message)s'

# 3、日志配置字典
"""
handlers: 日志接收者,不同的handlers会将日志输出到不同的位置。一般是输出到console和文件
loggers: 日志的生产者,负责产生不同级别的日志。产生的日志会传递给handlers,然后控制输出日志的位置


loggers 中设置了日志 level 等级,handlers也设置了日志 level 等级。
解释：
    loggers 设置了 DEBUG 级别,则DEBUG以上的级别的日志都能被输出;
    接下来日志丢给 handlers ,如果 handlers 的日志级别也是 DEBUG,那么就输出DEBUG级别以上的日志;
    如果 handlers设置的是 INFO 级别的日志，那么 只有 INFO 级别的日志才能被输出.
"""

LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'test': {
            'format': test_format
        },
    },
    'filters': {},
    # handlers: 日志接收者,不同的handlers会将日志输出到不同的位置
    'handlers': {
        # 默认输出到文件
        'default': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'class': 'logging.FileHandler',  # 输出到文件
            'formatter': 'standard',
            'filename': DEFAULT_LOGFILE,
            'encoding': 'utf-8',
        },
        # 输出到终端(标准输出)
        'console': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'class': 'logging.StreamHandler',  # 输出到屏幕，即终端
            'formatter': 'simple'
        },
        # 根据日志文件大小来自动切割日志
        'access': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': ACCESS_LOGFILE,
            'maxBytes': 1024 * 1024 * 200,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        # 根据时间来切割日志
        'access_time': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': TIMED_ACCESS_LOGFILE,
            'when': 'midnight',
            'interval': 1,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        # 给领导或者老板看的日志文件
        'boss': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'class': 'logging.FileHandler',
            'formatter': 'test',
            'filename': BOSS_LOGFILE,
            'encoding': 'utf-8',
        },
    },
    # loggers: 日志的生产者,负责产生不同级别的日志。产生的日志会传递给handlers,然后控制输出日志的位置
    'loggers': {
        # 没有名字表示的是默认的 loggers
        '': {
            'handlers': ['default', 'console'],     # 这个 logger 产生的日志会丢给 default 和 console 这两个接收者
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,     # 和日志继承相关，一般改成 False 即可。
        },
        'access_log': {
            'handlers': ['access', ],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'console_log': {
            'handlers': ['console', ],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'access_console_log': {
            'handlers': ['access', 'console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'boss_log': {
            'handlers': ['boss', ],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
