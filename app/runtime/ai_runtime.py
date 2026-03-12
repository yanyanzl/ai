"""
Module: ai_runtime

Purpose:
    Solo AI Platform runtime.

Responsibilities:
    - 初始化系统
    - 加载工具
    - 加载插件
    - 初始化 LLMBrain
    - 运行主循环
"""

from app.core.tool_router import tool_router
from app.core.plugin_manager import PluginManager
from app.core.memory_manager import MemoryManager
from app.brain.llm_brain import LLMBrain
from app.utils.logger import get_logger

logger = get_logger("ai_runtime")


class AIRuntime:

    def __init__(self):

        logger.info("Initializing AI Runtime...")

        # -------------------------
        # Router
        # -------------------------
        self.router = tool_router

        # -------------------------
        # Plugin manager
        # -------------------------
        self.plugin_manager = PluginManager(self.router)

        # -------------------------
        # Memory
        # -------------------------
        self.memory = MemoryManager()

        # -------------------------
        # Brain
        # -------------------------
        # Brain already loads router / plugins / memory
        self.brain = LLMBrain()

    # ------------------------------------------------
    # 启动系统
    # ------------------------------------------------
    def start(self):

        logger.info("Starting Solo AI Platform...")

        # 加载插件
        self.plugin_manager.load_plugins()

        logger.info("System ready.")

    # ------------------------------------------------
    # 处理用户消息
    # ------------------------------------------------
    def handle_message(self, message: str):

        logger.info(f"[USER] {message}")

        try:

            result = self.brain.handle(message)

            if isinstance(result, dict):

                if "summary" in result:
                    return result["summary"]

                if "message" in result:
                    return result["message"]

            return str(result)

        except Exception as e:

            logger.exception("Runtime error")

            return f"系统错误: {str(e)}"