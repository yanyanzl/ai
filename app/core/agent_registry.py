"""
agent_registry.py

自动加载 agents
- 自动扫描 app/agents 下所有模块
- 导入模块时，工具自动注册
"""

import importlib
import pkgutil
import app.agents

def load_agents():
    """
    扫描并加载所有 agent 文件
    """
    package = app.agents
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        try:
            importlib.import_module(f"app.agents.{module_name}")
            print(f"[INFO] Agent '{module_name}' 加载成功")
        except Exception as e:
            print(f"[ERROR] 加载 Agent '{module_name}' 失败: {e}")