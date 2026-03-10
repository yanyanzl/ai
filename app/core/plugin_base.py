

class PluginBase:

    name = "base_plugin"
    description = ""
    version = "1.0"
    
    def register(self, router):
        """
        注册工具到 router
        """
        raise NotImplementedError