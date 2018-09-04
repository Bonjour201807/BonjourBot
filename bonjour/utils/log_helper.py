"""
@Author: yangdu
@Time: 2018/8/4 下午10:58
@Software: PyCharm
"""
import logging
import os
from logging.handlers import RotatingFileHandler


LOG_BASE_PATH = './logs/'
if not os.path.exists(LOG_BASE_PATH):
    os.makedirs(LOG_BASE_PATH)


class LogHelper:
    cur_level = logging.DEBUG
    is_initialized = False

    @staticmethod
    def get(name):
        logging.getLogger().setLevel(LogHelper.cur_level)
        return logging.getLogger(name)

    @staticmethod
    def initialize(log_file_name, log_file_max_size=40000000, log_file_max_count=10):
        if LogHelper.is_initialized:
            return

        format_str = '[%(asctime)s][%(name)s][%(levelname)s]: %(message)s'

        formatter = logging.Formatter(format_str, datefmt='%Y-%m-%d %H:%M:%S')
        handler = RotatingFileHandler(LOG_BASE_PATH + os.path.sep + log_file_name,
                                      maxBytes=log_file_max_size,
                                      backupCount=log_file_max_count)
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)

        LogHelper.is_initialized = True

    @staticmethod
    def set_level(level):
        level = level.lower()
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "error": logging.ERROR,
        }
        if level not in level_map:
            print('Failed to set log level')
            return

        LogHelper.cur_level = level_map[level]
        logging.getLogger().setLevel(LogHelper.cur_level)


if __name__ == '__main__':
    # 配置路径
    LogHelper.initialize('test_app.log')
    # 设置级别（可选，默认DEBUG）
    LogHelper.set_level('ERROR')
    # 获取句柄
    logger = LogHelper.get('app')

    logger.info(' * hello im info')
    logger.error(' * hello im error')
    logger.debug(' * hello im debug')