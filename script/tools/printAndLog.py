# -*- coding: utf-8 -*-

import os
import logging


def log_and_print(message, log_file_path, log_file_name):
    if not log_file_path.endswith('/'):
        log_file_path += '/'
    log_file_name = log_file_name.replace('.log', '')

    log_file_path_and_name = log_file_path + log_file_name
    log_file_path_and_name = f"{log_file_path_and_name}.log"
    # 确保日志目录存在
    log_directory = os.path.dirname(log_file_path_and_name)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # 配置日志记录器
    logging.basicConfig(
        filename=log_file_path_and_name,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'  # 追加模式
    )

    # 创建日志记录器
    logger = logging.getLogger()

    """<--- 打印消息到控制台并记录到日志文件 --->"""
    print(message)
    logger.info(message)


# 使用示例
if __name__ == "__main__":
    log_and_print("这是一个日志消息", "../logs/","日志输出一体化测试")
