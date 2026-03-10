from app.core.plugin_base import PluginBase
from pathlib import Path


class Plugin(PluginBase):

    name = "desktop_plugin"
    description = "Desktop management tools"

    def register(self, router):

        router.register("scan_desktop", self.scan_desktop)

    def scan_desktop(self):
        """
        扫描用户桌面文件
        返回:
            {
                "total": int,
                "files": [{"name": str, "is_dir": bool}]
            }
        """
        try:
            desktop = self._get_desktop_path()

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
    
    # ------------------------------------------------
    # 获取桌面路径
    # ------------------------------------------------
    def _get_desktop_path(self):
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