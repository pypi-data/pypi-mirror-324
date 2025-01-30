from PyQt6.QtWidgets import QApplication
from .core.Settings import Settings
from PyQt6.QtGui import QIcon
import platform
import pathlib
import os


class Environment:
    def __init__(self, app: QApplication) -> None:
        self.app = app

        self.program_dir = os.path.dirname(__file__)
        self.data_dir = self._get_data_path()

        with open(os.path.join(self.program_dir, "Version.txt"), "r", encoding="utf-8") as f:
            self.version = f.read().strip()

        self.icon = QIcon(os.path.join(self.program_dir, "Icon.png"))

        self.settings = Settings()
        self.settings.load(os.path.join(self.data_dir, "settings.json"))

    def _get_data_path(self) -> str:
        match platform.system():
            case "Windows":
                return os.path.join(os.getenv("APPDATA"), "JakobDev", "jdProcessFileWatcher")
            case "Darwin":
                return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "JakobDev", "jdProcessFileWatcher")
            case "Haiku":
                return os.path.join(str(pathlib.Path.home()), "config", "settings", "JakobDev", "jdProcessFileWatcher")
            case _:
                if os.getenv("XDG_DATA_HOME") is not None:
                    return os.path.join(os.getenv("XDG_DATA_HOME"), "JakobDev", "jdProcessFileWatcher")
                else:
                    return os.path.join(str(pathlib.Path.home()), ".local", "share", "JakobDev", "jdProcessFileWatcher")
