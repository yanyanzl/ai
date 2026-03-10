import importlib
import pkgutil
import json
import os
from typing import Optional

from app.utils.logger import get_logger

logger = get_logger("plugin_manager")


class PluginManager:
    """
    插件管理器 v3
    功能：
    - 自动加载插件
    - 支持热加载/卸载
    - 插件权限管理
    - 获取插件信息
    """

    def __init__(self, router):
        self.router = router
        # 插件字典: name -> {"instance": Plugin(), "manifest": {...}}
        self.plugins = {}

    # ------------------------------------------------
    # 自动加载插件（可指定包路径）
    # ------------------------------------------------
    def load_plugins(self, package="app.plugins"):
        logger.info("Loading plugins...")

        try:
            pkg = importlib.import_module(package)
        except Exception as e:
            logger.error(f"Cannot import plugin package {package}: {e}")
            return

        for _, module_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
            if not is_pkg:
                continue

            try:
                plugin_path = f"{package}.{module_name}"
                manifest = self.load_manifest(plugin_path)

                if manifest.get("enabled", True) is False:
                    logger.info(f"Plugin disabled: {module_name}")
                    continue

                module = importlib.import_module(f"{plugin_path}.plugin")

                if not hasattr(module, "Plugin"):
                    logger.warning(f"{module_name} missing Plugin class")
                    continue

                plugin = module.Plugin()
                plugin.register(self.router)

                # 保存插件实例和 manifest
                self.plugins[plugin.name] = {
                    "instance": plugin,
                    "manifest": manifest
                }

                logger.info(
                    f"Plugin loaded: {plugin.name} v{manifest.get('version','1.0')} "
                    f"permissions={manifest.get('permissions', [])}"
                )

            except Exception as e:
                logger.error(f"Plugin load failed: {module_name} {e}")

    # ------------------------------------------------
    # 热加载单个插件
    # ------------------------------------------------
    def enable_plugin(self, name: str, package="app.plugins") -> bool:
        if name in self.plugins:
            logger.info(f"Plugin {name} already loaded")
            return True

        try:
            plugin_path = f"{package}.{name}"
            manifest = self.load_manifest(plugin_path)
            if manifest.get("enabled", True) is False:
                logger.info(f"Plugin {name} is disabled in manifest")
                return False

            module = importlib.import_module(f"{plugin_path}.plugin")
            if not hasattr(module, "Plugin"):
                logger.warning(f"{name} missing Plugin class")
                return False

            plugin = module.Plugin()
            plugin.register(self.router)

            self.plugins[plugin.name] = {
                "instance": plugin,
                "manifest": manifest
            }

            logger.info(
                f"Plugin enabled: {plugin.name} v{manifest.get('version','1.0')} "
                f"permissions={manifest.get('permissions', [])}"
            )
            return True
        except Exception as e:
            logger.error(f"Enable plugin failed: {name} {e}")
            return False

    # ------------------------------------------------
    # 卸载插件
    # ------------------------------------------------
    def disable_plugin(self, name: str) -> bool:
        if name not in self.plugins:
            logger.warning(f"Plugin {name} not loaded")
            return False

        try:
            plugin = self.plugins[name]["instance"]
            if hasattr(plugin, "unregister"):
                plugin.unregister(self.router)

            del self.plugins[name]
            logger.info(f"Plugin disabled: {name}")
            return True
        except Exception as e:
            logger.error(f"Disable plugin failed: {name} {e}")
            return False

    # ------------------------------------------------
    # 读取 manifest
    # ------------------------------------------------
    def load_manifest(self, plugin_path: str) -> dict:
        try:
            module = importlib.import_module(plugin_path)
            base_path = os.path.dirname(module.__file__)
            manifest_path = os.path.join(base_path, "plugin.json")

            if not os.path.exists(manifest_path):
                return {}

            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 校验 manifest 必须包含 name, version, permissions
                data.setdefault("name", os.path.basename(plugin_path))
                data.setdefault("version", "1.0")
                data.setdefault("permissions", [])
                data.setdefault("enabled", True)
                return data
        except Exception as e:
            logger.error(f"Load manifest failed for {plugin_path}: {e}")
            return {}

    # ------------------------------------------------
    # 列出所有插件名称
    # ------------------------------------------------
    def list_plugins(self):
        return list(self.plugins.keys())

    # ------------------------------------------------
    # 获取插件 manifest / info
    # ------------------------------------------------
    def plugin_info(self, name: str) -> Optional[dict]:
        if name not in self.plugins:
            return None
        return self.plugins[name]["manifest"]

    # ------------------------------------------------
    # 获取插件权限
    # ------------------------------------------------
    def plugin_permissions(self, name: str):
        info = self.plugin_info(name)
        if info:
            return info.get("permissions", [])
        return []
