"""
system_agent.py

系统管理 Agent 示例
- 清理临时文件
- 获取 CPU/内存信息
"""

import os
import tempfile
from app.tools.tool_decorator import tool

@tool("clean_temp")
def clean_temp():
    """
    清理临时文件夹
    返回:
        {"deleted": int}
    """
    count = 0
    try:
        temp_dir = tempfile.gettempdir()
        for f in os.listdir(temp_dir):
            path = os.path.join(temp_dir, f)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    count += 1
            except Exception as e:
                print(f"[WARN] 删除文件失败: {path} -> {e}")
        return {"deleted": count}
    except Exception as e:
        return {"error": str(e)}