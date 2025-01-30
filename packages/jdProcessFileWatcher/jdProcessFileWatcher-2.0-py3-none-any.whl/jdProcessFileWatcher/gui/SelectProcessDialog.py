from ..ui_compiled.SelectProcessDialog import Ui_SelectProcessDialog
from PyQt6.QtWidgets import QDialog, QStyle, QListWidgetItem
from ..Functions import list_processes
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon


if TYPE_CHECKING:
    from ..Environment import Environment
    from .MainWindow import MainWindow


class SelectProcessDialog(QDialog, Ui_SelectProcessDialog):
    def __init__(self,  env: "Environment", main_window: "MainWindow") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._main_window = main_window

        self.reload_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)))
        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        self.cancel_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)))

        self.process_list.currentItemChanged.connect(self._update_ok_button_enabled)
        self.search_edit.textChanged.connect(self._update_items_visible)
        self.reload_button.clicked.connect(self._fill_process_list)
        self.ok_button.clicked.connect(self._ok_button_clicked)
        self.cancel_button.clicked.connect(self.close)

        self._fill_process_list()

    def _update_ok_button_enabled(self) -> None:
        item = self.process_list.currentItem()

        if item is None:
            self.ok_button.setEnabled(False)
            return

        self.ok_button.setEnabled(not item.isHidden())

    def _fill_process_list(self) -> None:
        self.process_list.clear()

        for current_process in list_processes():
            item = QListWidgetItem(f"{current_process[0]}\t{current_process[1]}")
            item.setData(42, current_process[0])
            self.process_list.addItem(item)

        self.search_edit.setText("")

        self._update_ok_button_enabled()

    def _update_items_visible(self) -> None:
        search_text = self.search_edit.text().lower()

        for row in range(self.process_list.count()):
            item = self.process_list.item(row)
            item.setHidden(not search_text in item.text().lower())

        self._update_ok_button_enabled()

    def _ok_button_clicked(self) -> None:
        item = self.process_list.currentItem()

        if item is None:
            return

        self._main_window.attach_process(item.data(42))

        self.close()
