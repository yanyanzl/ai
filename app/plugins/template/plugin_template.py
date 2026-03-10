import os
from app.utils.logger import get_logger

logger = get_logger("NEW_PLUGIN_NAME_plugin")

class Plugin:
    name = "NEW_PLUGIN_NAME"

    def register(self, router):
        """
        将工具注册到系统的 tool_router
        """
        router.register_tool(self.name, self.run)

    def run(self, args: dict):
        """
        工具执行入口，args 中包含用户传入参数
        """
        # 参数解析与默认值
        folder = args.get("folder", "C:/Users/Public/Desktop")
        include_hidden = args.get("include_hidden", False)

        # 业务逻辑示例
        try:
            files = []
            for f in os.listdir(folder):
                if not include_hidden and f.startswith('.'):
                    continue
                path = os.path.join(folder, f)
                files.append({
                    "name": f,
                    "is_dir": os.path.isdir(path)
                })
            logger.info(f"{self.name}: scanned {len(files)} items in {folder}")
            return {"total": len(files), "files": files}
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return {"error": str(e)}