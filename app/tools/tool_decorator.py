# """
# tool_decorator.py

# 工具注册系统（Tool Registry）
# - 所有工具通过 @tool 装饰器自动注册
# - Router 调用工具时无需修改
# """

# from typing import Callable

# # 全局工具注册表
# TOOL_REGISTRY = {}

# def tool(name: str):
#     """
#     装饰器：注册工具到全局工具表
#     参数:
#         name: str 工具名称（唯一）
#     使用：
#         @tool("scan_desktop")
#         def scan_desktop():
#             ...
#     """

#     def decorator(func: Callable):
#         if name in TOOL_REGISTRY:
#             # 防止重复注册
#             print(f"[WARN] Tool {name} 已存在，将覆盖")
#         TOOL_REGISTRY[name] = func
#         return func

#     return decorator
"""
tool_decorator.py

工具注册装饰器
"""

from app.core.tool_router import tool_router
from app.utils.logger import get_logger

logger = get_logger("tool_decorator")

def tool(name: str):
    """
    工具注册装饰器

    用法：
    @tool("scan_desktop")
    def scan_desktop():
        pass
    """

    def decorator(func):

        try:

            tool_router.register(name, func)

            logger.info(f"Tool decorator registered: {name}")

        except Exception as e:

            logger.error(f"Tool register failed: {name}")

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator