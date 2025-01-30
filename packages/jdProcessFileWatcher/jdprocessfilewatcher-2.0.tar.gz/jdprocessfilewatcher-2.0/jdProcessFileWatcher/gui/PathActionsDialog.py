from ..ui_compiled.PathActionsDialog import Ui_PathActionsDialog
from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import QCoreApplication
from .ActionsTable import ActionsTable
from PyQt6.QtWidgets import QDialog


if TYPE_CHECKING:
    from .MainWindow import MainWindow, FileTreeItem
    from ..Environment import Environment


class PathActionsDialog(QDialog, Ui_PathActionsDialog):
    def __init__(self, env: "Environment", main_window: "MainWindow") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._env = env
        self._current_item: Optional["FileTreeItem"] = None

        self._actions_table = ActionsTable(env, False)
        self.main_layout.insertWidget(0, self._actions_table)

        self.include_content_check_box.toggled.connect(self._update_table)

    def _update_table(self) -> None:
        self._actions_table.clear()

        if self.include_content_check_box.isChecked():
            for data in self._current_item.get_recursive_data():
                data.create_table_row(self._env.settings.get("timeFormat"))
                self._actions_table.add_data(data)
        else:
            for data in self._current_item.get_own_data():
                data.create_table_row(self._env.settings.get("timeFormat"))
                self._actions_table.add_data(data)

    def open_dialog(self, item: "FileTreeItem") -> None:
        self._current_item = item
        self.include_content_check_box.setChecked(False)
        self.include_content_check_box.setHidden(not item.is_directory)
        self.setWindowTitle(QCoreApplication.translate("PathActionsDialog", "Actions of {{path}}").replace("{{path}}", item.path))
        self._update_table()
        self.open()
