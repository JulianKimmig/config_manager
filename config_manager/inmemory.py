from .core import ConfigManager


class InMemoryConfig(ConfigManager):
    def __init__(self, *args, **kwargs) -> None:
        self._backup = {}
        super().__init__(*args, **kwargs)

    def save(self):
        self._backup = self.data

    def load(self):
        self._data = self._backup
