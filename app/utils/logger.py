"""
logger.py

统一日志系统

功能：
- 统一日志格式
- 支持 debug / info / error
- 支持文件日志
"""

import logging
import sys


def get_logger(name: str):
    """
    获取统一 logger

    参数:
        name: 模块名称
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    # 控制台日志
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)

    logger.addHandler(console)

    return logger