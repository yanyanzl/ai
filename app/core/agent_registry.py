"""
agent_registry.py

自动加载 agents
- 自动扫描 app/agents 下所有模块
- 导入模块时，工具自动注册
"""

import importlib
import pkgutil
import app.agents
from app.utils.logger import get_logger

logger = get_logger("agent_registry")

def load_agents():
    """
    扫描并加载所有 agent 文件
    """
    package = app.agents
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):

        module_path = f"app.agents.{module_name}"

        try:

            importlib.import_module(module_path)

            logger.info(f"Agent loaded: {module_name}")

        except Exception as e:
            logger.error(f"Agent load failed: {module_name}")