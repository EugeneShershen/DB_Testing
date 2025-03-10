class BaseDB:
    def __init__(self, config: dict):
        self.config = config
        self.logger = config.get("logger")
        self.engine = config.get("engine")
        self.session = config.get("session")
