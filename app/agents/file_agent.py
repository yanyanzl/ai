"""
file_agent.py

文件操作 Agent 示例
- 扫描桌面文件
- 容错机制：路径不存在或权限问题
"""

from pathlib import Path
from app.tools.tool_decorator import tool

# ------------------------------------------------
# 获取桌面路径
# ------------------------------------------------
def _get_desktop_path():
    """
    自动检测桌面路径

    Windows 常见两种：
    C:/Users/xxx/Desktop
    C:/Users/xxx/OneDrive/Desktop
    """

    try:

        # 默认桌面
        desktop = Path.home() / "Desktop"

        if desktop.exists():
            return desktop

        # OneDrive桌面
        desktop = Path.home() / "OneDrive" / "Desktop"

        if desktop.exists():
            return desktop

        raise Exception("Desktop path not found")

    except Exception as e:

        print("获取桌面路径失败:", e)
        return None

@tool("scan_desktop")
def scan_desktop():
    """
    扫描用户桌面文件
    返回:
        {
            "total": int,
            "files": [{"name": str, "is_dir": bool}]
        }
    """
    try:
        desktop = _get_desktop_path()

        if not desktop.exists():
            return {"error": f"桌面路径不存在: {desktop}"}

        files = []
        for f in desktop.iterdir():
            try:
                files.append({
                    "name": f.name,
                    "is_dir": f.is_dir()
                })
            except Exception as e:
                # 跳过无法访问的文件
                print(f"[WARN] 访问文件失败: {f} -> {e}")
        return {
            "total": len(files),
            "files": files
        }
    except Exception as e:
        return {"error": str(e)}