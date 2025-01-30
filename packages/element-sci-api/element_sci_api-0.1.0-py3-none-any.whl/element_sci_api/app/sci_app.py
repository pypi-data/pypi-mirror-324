from .file_manager import FileManager


class SciApp:
    # 写单例模式
    _instance = None
    _init_called = False

    def __new__(cls, *args, **kwargs):
        assert not cls._instance, "SciApp already initialized"
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, configs_path: str) -> None:
        if not self._init_called:
            self.configs_path = configs_path
            self.configs_file_manager = FileManager(configs_path)
            self._init_called = True

    @classmethod
    def getInstance(cls):
        assert cls._instance is not None, "SciApp not initialized"
        return cls._instance
