from ..ui_compiled.RunCommandDialog import Ui_RunCommandDialog
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.QtCore import QCoreApplication
from ..Types import StartProcessInfo
from ..Functions import is_flatpak
from typing import TYPE_CHECKING
import os


if TYPE_CHECKING:
    from .MainWindow import MainWindow


class RunCommandDialog(QDialog, Ui_RunCommandDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._main_window= main_window

        self.browse_working_directory.setHidden(is_flatpak())

        self.browse_working_directory.clicked.connect(self._browse_working_directory_clicked)
        self.button_box.accepted.connect(self._ok_button_clicked)

    def _browse_working_directory_clicked(self) -> None:
        if self.working_directory_edit.text().strip() == "":
            start_dir = os.path.expanduser("~")
        else:
            start_dir = self.working_directory_edit.text().strip()

        path = QFileDialog.getExistingDirectory(directory=start_dir)

        if path == "":
            return

        self.edit_working_directory.setText(path)

    def _ok_button_clicked(self) -> None:
        if self.command_edit.text().strip() == "":
            QMessageBox.critical(self, QCoreApplication.translate("RunCommandDialog", "No Command"),  QCoreApplication.translate("RunCommandDialog", "You need to enter a Command"))
            return

        info = StartProcessInfo(["sh", "-c", self.command_edit.text()])

        if self.working_directory_edit.text().strip() == "":
            info.working_directory = self.working_directory_edit.text()

        self._main_window.start_process(info)
        self.close()

    def open_dialog(self) -> None:
        self.open()
