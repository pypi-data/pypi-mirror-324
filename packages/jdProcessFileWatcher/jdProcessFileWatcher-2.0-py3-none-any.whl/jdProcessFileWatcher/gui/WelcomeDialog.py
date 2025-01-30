from PyQt6 import QtGui
from ..ui_compiled.WelcomeDialog import Ui_WelcomeDialog
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QCloseEvent
from typing import TYPE_CHECKING
import os


if TYPE_CHECKING:
    from ..Environment import Environment
    from .MainWindow import MainWindow


class WelcomeDialog(QDialog, Ui_WelcomeDialog):
    def __init__(self, env: "Environment", main_window: "MainWindow") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._env = env

        self.button_box.accepted.connect(self.close)

    def open_dialog(self) -> None:
        self.startup_check_box.setChecked(self._env.settings.get("welcomeDialogStartup"))
        self.open()

    def closeEvent(self, event: QCloseEvent) -> None:
        self._env.settings.set("welcomeDialogStartup", self.startup_check_box.isChecked())
        self._env.settings.save(os.path.join(self._env.data_dir, "settings.json"))
        event.accept()
