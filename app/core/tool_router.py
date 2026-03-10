# """
# tool_router.py

# 统一工具调用接口
# - 自动从 TOOL_REGISTRY 获取工具
# - 提供容错机制
# """

# from app.tools.tool_decorator import TOOL_REGISTRY

# class ToolRouter:
#     """通用工具路由器"""

#     def execute(self, tool_name: str, args: dict = None):
#         """
#         调用指定工具
#         :param tool_name: 工具名
#         :param args: 可选参数 dict
#         :return: dict, 成功返回工具结果，否则返回 error 信息
#         """
#         if tool_name not in TOOL_REGISTRY:
#             return {"error": f"Tool '{tool_name}' 未找到"}

#         try:
#             func = TOOL_REGISTRY[tool_name]
#             if args:
#                 return func(**args)
#             return func()
#         except Exception as e:
#             # 捕获所有异常，保证不会导致系统崩溃
#             return {"error": str(e)}
"""
tool_router.py

Solo AI Platform 核心组件
负责：
1. 注册所有工具 (@tool)
2. 提供统一执行入口
3. 管理工具列表
4. 提供错误处理
5. 支持 DevAgent 动态生成工具

设计原则：
- 单例 Router
- 自动注册
- 完整容错
"""

import traceback
from typing import Callable, Dict, Any
from app.utils.logger import get_logger

logger = get_logger("tool_router")

class ToolRouter:
    """
    ToolRouter:
    统一管理所有工具
    """

    def __init__(self):
        # 工具注册表
        self.tools: Dict[str, Callable] = {}

    # --------------------------
    # 注册工具
    # --------------------------
    def register(self, name: str, func: Callable):
        """
        注册工具

        :param name: 工具名称
        :param func: 工具函数
        """

        if not name:
            logger.warning(f"工具名称不能为空")
            raise ValueError("工具名称不能为空")

        if name in self.tools:
            # print(f"[WARNING] Tool '{name}' 已存在，将覆盖")
            logger.warning(f"[WARNING] Tool '{name}' 已存在，将覆盖")

        self.tools[name] = func
        logger.info(f"Tool registered: {name}")

    # --------------------------
    # 执行工具
    # --------------------------
    def execute(self, name: str, args: Dict[str, Any] = None):
        """
        执行工具

        :param name: 工具名称
        :param args: 参数
        """

        if args is None:
            args = {}

        if name not in self.tools:
            logger.error(f"Tool not found: {name}")

            return {
                "error": f"工具 '{name}' 不存在",
                "available_tools": self.list_tools()
            }

        tool_func = self.tools[name]

        try:

            # 执行工具
            result = tool_func(**args)

            # 标准返回格式
            if isinstance(result, dict):
                return result

            return {"result": result}

        except Exception as e:

            logger.exception("Tool execution failed")
            traceback.print_exc()

            return {
                "error": str(e),
                "tool": name
            }

    # --------------------------
    # 获取工具列表
    # --------------------------
    def list_tools(self):
        return list(self.tools.keys())


# --------------------------
# 单例 Router
# --------------------------

tool_router = ToolRouter()