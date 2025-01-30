from PyQt6.QtWidgets import QDialog, QListWidgetItem, QDialogButtonBox
from ..ui_compiled.RunProgramDialog import Ui_RunProgramDialog
from PyQt6.QtCore import QCoreApplication
from ..Functions import is_one_in_list
from typing import cast, TYPE_CHECKING
from ..Types import StartProcessInfo
from PyQt6.QtGui import QIcon
import desktop_entry_lib


if TYPE_CHECKING:
    from .MainWindow import MainWindow


class RunProgramDialog(QDialog, Ui_RunProgramDialog):
    def __init__(self, main_window: "MainWindow", app_icon: QIcon) -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._main_window = main_window
        self._app_icon = app_icon
        self._is_setup = False

        self._categories: list[tuple[str, str, list[str]]] = [
            ("Office", QCoreApplication.translate("RunProgramDialog", "Office"), ["Office"], "applications-office"),
            ("Utility", QCoreApplication.translate("RunProgramDialog", "Utilities"), ["Utility"], "applications-utilities"),
            ("Settings", QCoreApplication.translate("RunProgramDialog", "Settings"), ["Settings"], "preferences-system"),
            ("Development", QCoreApplication.translate("RunProgramDialog", "Development"), ["Development"], "applications-development"),
            ("Graphics", QCoreApplication.translate("RunProgramDialog", "Graphics"), ["Graphics"], "applications-graphics"),
            ("Network", QCoreApplication.translate("RunProgramDialog", "Internet"), ["Network"], "applications-internet"),
            ("Multimedia", QCoreApplication.translate("RunProgramDialog", "Multimedia"), ["AudioVideo", "Audio", "Video"], "applications-multimedia"),
            ("Games", QCoreApplication.translate("RunProgramDialog", "Games"), ["Game", "Games"], "applications-games"),
            ("System", QCoreApplication.translate("RunProgramDialog", "System"), ["System"], "applications-system"),
        ]

        self._category_items: dict[str, list[desktop_entry_lib.DesktopEntry]] = {}

        self.category_list.currentItemChanged.connect(self._update_entry_list)
        self.entry_list.currentRowChanged.connect(self._update_ok_button_enabled)
        self.button_box.accepted.connect(self._ok_button_clicked)
        self.button_box.rejected.connect(self.close)

    def _setup(self) -> None:
        for category in self._categories:
            self._category_items[category[0]] = []
            item = QListWidgetItem(category[1])
            item.setIcon(QIcon.fromTheme(category[3]))
            item.setData(42, category[0])
            self.category_list.addItem(item)

        self._category_items["Other"] = []
        other_item = QListWidgetItem(QCoreApplication.translate("RunProgramDialog", "Other"))
        other_item.setIcon(QIcon.fromTheme("applications-other"))
        other_item.setData(42, "Other")
        self.category_list.addItem(other_item)

        collection = desktop_entry_lib.DesktopEntryCollection()
        collection.load_menu()

        for entry in collection.desktop_entries.values():
            if not entry.should_show_in_menu():
                continue

            if entry.Icon is not None:
                icon = QIcon.fromTheme(entry.Icon)
                if not icon.isNull():
                    item.setIcon(icon)
                else:
                    item.setIcon(self._app_icon)
            else:
                item.setIcon(self._app_icon)

            for category in self._categories:
                if is_one_in_list(category[2], entry.Categories):
                    self._category_items[category[0]].append(entry)
                    break
            else:
                self._category_items["Other"].append(entry)

        self._is_setup = True

    def _update_ok_button_enabled(self) -> None:
        enabled = self.entry_list.currentRow() != -1
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setEnabled(enabled)

    def _update_entry_list(self) -> None:
        self.entry_list.clear()

        for entry in self._category_items[self.category_list.currentItem().data(42)]:
            item = QListWidgetItem(entry.Name.get_translated_text())
            item.setToolTip(entry.Comment.get_translated_text())
            item.setData(42, entry)

            if (icon_path := entry.get_icon_path()) is not None:
                icon = QIcon(icon_path)
                if not icon.isNull():
                    item.setIcon(icon)
                else:
                    item.setIcon(self._app_icon)
            else:
                item.setIcon(self._app_icon)

            self.entry_list.addItem(item)

        self._update_ok_button_enabled()

    def _ok_button_clicked(self) -> None:
        entry = cast(desktop_entry_lib.DesktopEntry, self.entry_list.currentItem().data(42))

        info = StartProcessInfo(entry.get_command([], []))
        info.working_directory = entry.get_working_directory()

        self._main_window.start_process(info)

        self.close()

    def open_dialog(self) -> None:
        if not self._is_setup:
            self._setup()

        self.open()
