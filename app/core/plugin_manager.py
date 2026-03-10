import importlib
import pkgutil
from app.utils.logger import get_logger

logger = get_logger("plugin_manager")


class PluginManager:

    def __init__(self, router):
        self.router = router
        self.plugins = []

    def load_plugins(self, package="app.plugins"):

        logger.info("Loading plugins...")

        pkg = importlib.import_module(package)

        for _, module_name, is_pkg in pkgutil.iter_modules(pkg.__path__):

            if not is_pkg:
                continue

            logger.info(f"Found plugin package: {module_name}")

            try:

                module = importlib.import_module(
                    f"{package}.{module_name}.plugin"
                )

                if hasattr(module, "Plugin"):

                    plugin = module.Plugin()

                    plugin.register(self.router)

                    self.plugins.append(plugin)

                    logger.info(f"Plugin loaded: {plugin.name}")

                else:
                    logger.warning(
                        f"{module_name} has no Plugin class"
                    )

            except Exception as e:

                logger.error(
                    f"Plugin load failed: {module_name} {e}"
                )

    def list_plugins(self):

        return [p.name for p in self.plugins]