class OpenDiggerCliConfig:
    def __init__(self):
        self.debug = False
        self.github_pat = "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"

        self.__load_config()

    def __load_config(self):
        pass

    def set_debug(self, debug: bool):
        self.debug = debug
