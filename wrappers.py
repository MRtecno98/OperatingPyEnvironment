class PluginClass() :
    def __init__(self, clazz, meta) :
        self.clazz = clazz
        self.plugin_name = meta["pl_name"]
        self.plugin_description = meta["pl_desc"]
        self.plugin_author = meta["author"]
        self.plugin_version = meta["version"]
