

class PluginBase:

    name = "base_plugin"
    description = ""

    def register(self, router):
        """
        注册工具到 router
        """
        raise NotImplementedError