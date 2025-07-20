# coding: utf-8

# 项目根目录
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'db')


LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # 日志格式
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s [%(name)s] %(levelname)s  %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'test': {
            'format': '%(asctime)s %(message)s',
        },
        'test1': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'filters': {},
    # 日志处理器
    'handlers': {
        'console_debug_handler': {
            'level': 'DEBUG',  # 日志处理的级别限制
            'class': 'logging.StreamHandler',  # 输出到终端
            'formatter': 'simple'  # 日志格式
        },
        'file_info_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': os.path.join(BASE_DIR, 'log', 'user.log'),  # 日志存放的路径
            'maxBytes': 800,  # 日志大小 10M
            'backupCount': 3,  # 日志文件保存数量限制
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'file_deal_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',  # 保存到文件
            'filename': 'deal.log',  # 日志存放的路径
            'encoding': 'utf-8',  # 日志文件的编码
            'formatter': 'standard',
        },
        'file_operate_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',  # 保存到文件
            'filename': 'operate.log',  # 日志存放的路径
            'encoding': 'utf-8',  # 日志文件的编码
            'formatter': 'standard',
        },
    },
    # 日志记录器
    'loggers': {
        '': {
            'handlers': ['console_debug_handler','file_info_handler'],
            'level': 'DEBUG',
            'propagate': False,

        },
    }
}


import logging.config
logging.config.dictConfig(LOGGING_DIC)

# # 配置文件相关
# import configparser

# config = configparser.ConfigParser()
# CONFIG_PATH = os.path.join(BASE_DIR, 'settings.ini')
# config.read(CONFIG_PATH, encoding='utf-8-sig')
# LOGIN_TYPE = config['USER']['LOGIN_TYPE']
# LOGIN_USER = config['USER']['LOGIN_USER']

# 读取配置文件
import configparser
config = configparser.ConfigParser()
CONFIG_PATH = os.path.join(
    BASE_DIR,'settings.ini'
)
config.read(CONFIG_PATH,encoding='utf-8-sig')
LOGIN_TYPE = config.get('USER','LOGIN_TYPE')
LOGIN_USER = config.get('USER','LOGIN_USER')
FALSE_STUDENTS_NUM = config.getint('USER','false_students_num')