"""
file_agent.py

AI 数字管家 - 文件管理 Agent

功能：
1 扫描桌面文件
2 查找大文件
3 自动整理桌面
4 统计文件类型

特点：
- 自动识别 Windows / OneDrive Desktop
- 全部异常捕获
- 防止误删
- 日志输出
"""

from pathlib import Path
import shutil
import traceback


class FileAgent:

    def __init__(self):
        """
        初始化 Agent
        """
        self.desktop = self._get_desktop_path()

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

    # ------------------------------------------------
    # 扫描桌面
    # ------------------------------------------------
    def scan_desktop(self):
        """
        返回桌面文件列表
        """

        try:

            if not self.desktop:
                return {"error": "desktop path not found"}

            files = []

            for f in self.desktop.iterdir():

                files.append({
                    "name": f.name,
                    "is_dir": f.is_dir()
                })

            return {
                "total": len(files),
                "files": files
            }

        except Exception as e:

            print("扫描桌面失败")
            traceback.print_exc()

            return {"error": str(e)}

    # ------------------------------------------------
    # 查找大文件
    # ------------------------------------------------
    def find_large_files(self, size_mb=100):
        """
        查找桌面大文件

        默认：100MB
        """

        try:

            if not self.desktop:
                return {"error": "desktop path not found"}

            size_bytes = size_mb * 1024 * 1024

            results = []

            for f in self.desktop.iterdir():

                try:

                    if f.is_file():

                        size = f.stat().st_size

                        if size > size_bytes:

                            results.append({
                                "name": f.name,
                                "size_mb": round(size / 1024 / 1024, 2)
                            })

                except Exception:
                    # 单个文件错误不影响整体
                    continue

            return {
                "count": len(results),
                "files": results
            }

        except Exception as e:

            traceback.print_exc()
            return {"error": str(e)}

    # ------------------------------------------------
    # 整理桌面
    # ------------------------------------------------
    def organize_desktop(self):
        """
        自动整理桌面文件
        """

        try:

            if not self.desktop:
                return {"error": "desktop path not found"}

            moved = []

            # 分类规则
            categories = {
                "Images": [".png", ".jpg", ".jpeg", ".gif"],
                "Documents": [".pdf", ".doc", ".docx", ".txt"],
                "Videos": [".mp4", ".mkv", ".mov"],
                "Archives": [".zip", ".rar", ".7z"],
                "Code": [".py", ".js", ".json", ".html"]
            }

            for f in self.desktop.iterdir():

                try:

                    if f.is_dir():
                        continue

                    ext = f.suffix.lower()

                    for folder, exts in categories.items():

                        if ext in exts:

                            target_dir = self.desktop / folder

                            # 创建分类目录
                            target_dir.mkdir(exist_ok=True)

                            target_file = target_dir / f.name

                            shutil.move(str(f), str(target_file))

                            moved.append(f.name)

                            break

                except Exception:
                    continue

            return {
                "moved_files": len(moved),
                "files": moved
            }

        except Exception as e:

            traceback.print_exc()
            return {"error": str(e)}

    # ------------------------------------------------
    # 文件类型统计
    # ------------------------------------------------
    def file_statistics(self):
        """
        统计桌面文件类型
        """

        try:

            if not self.desktop:
                return {"error": "desktop path not found"}

            stats = {}

            for f in self.desktop.iterdir():

                try:

                    if f.is_file():

                        ext = f.suffix.lower()

                        if ext not in stats:
                            stats[ext] = 0

                        stats[ext] += 1

                except Exception:
                    continue

            return stats

        except Exception as e:

            traceback.print_exc()
            return {"error": str(e)}