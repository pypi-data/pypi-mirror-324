from ..ui_compiled.SettingsDialog import Ui_SettingsDialog
from ..Functions import select_combo_box_data, is_flatpak
from PyQt6.QtWidgets import QDialog, QStyle, QFileDialog
from ..Constants import USE_STRACE_SETTINGS_VALUE
from ..core.Languages import get_language_names
from PyQt6.QtCore import Qt, QCoreApplication
from ..core.Settings import Settings
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
import datetime
import sys
import os


if TYPE_CHECKING:
    from ..Environment import Environment
    from .MainWindow import MainWindow


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, env: "Environment", main_window: "MainWindow") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._env = env

        found_translations = False
        language_names = get_language_names()
        self.language_box.addItem(language_names["en"], "en")
        for i in os.listdir(os.path.join(env.program_dir, "translations")):
            if i.endswith(".qm"):
                lang = i.removeprefix("jdProcessFileWatcher_").removesuffix(".qm")
                self.language_box.addItem(language_names.get(lang, lang), lang)
                found_translations = True
        if not found_translations:
             print("No compiled translations found. Please run tools/BuildTranslations to build the Translations.py.", file=sys.stderr)
        self.language_box.model().sort(0, Qt.SortOrder.AscendingOrder)
        self.language_box.insertItem(0, QCoreApplication.translate("SettingsDialog", "System language"), "default")

        self.builtin_strace_radio_button.setHidden(not is_flatpak())
        self.custom_strace_browse_button.setHidden(is_flatpak())

        self.reset_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)))
        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        self.cancel_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)))

        self.time_format_edit.textChanged.connect(self._update_time_preview_label)
        self.custom_strace_radio_button.toggled.connect(self._update_custom_strace_path_enabled)
        self.custom_strace_browse_button.clicked.connect(self._custom_strace_browse_button_clicked)

        self.reset_button.clicked.connect(lambda: self._update_widgets(Settings()))
        self.ok_button.clicked.connect(self._ok_button_clicked)
        self.cancel_button.clicked.connect(self.close)

    def _update_time_preview_label(self) -> None:
        try:
            self.time_preview_label.setText(QCoreApplication.translate("SettingsDialog", "(Preview: {{preview}})"). replace("{{preview}}",datetime.datetime.now().strftime(self.time_format_edit.text())))
        except ValueError:
            self.time_preview_label.setText(QCoreApplication.translate("SettingsDialog", "(Invalid)"))

    def _update_custom_strace_path_enabled(self) -> None:
        enabled = self.custom_strace_radio_button.isChecked()
        self.custom_strace_edit.setEnabled(enabled)
        self.custom_strace_browse_button.setEnabled(enabled)

    def _custom_strace_browse_button_clicked(self) -> None:
        if self.custom_strace_edit.text() == "":
            start_dir = os.path.expanduser("~")
        else:
            start_dir = os.path.dirname(self.custom_strace_edit.text())

        path = QFileDialog.getOpenFileName(self, directory=start_dir)[0]

        if path == "":
            return

        self.custom_strace_edit.setText(path)

    def _update_widgets(self, settings: Settings) -> None:
        select_combo_box_data(self.language_box, settings.get("language"))
        self.time_format_edit.setText(settings.get("timeFormat"))

        match settings.get("useStrace"):
            case USE_STRACE_SETTINGS_VALUE.BUILT_IN:
                self.builtin_strace_radio_button.setChecked(True)
            case USE_STRACE_SETTINGS_VALUE.SYSTEM:
                self.system_strace_radio_button.setChecked(True)
            case USE_STRACE_SETTINGS_VALUE.CUSTOM:
                self.custom_strace_radio_button.setChecked(True)

        self.custom_strace_edit.setText(settings.get("customStracePath"))
        self._update_custom_strace_path_enabled()

    def _set_settings(self, settings: Settings) -> None:
        settings.set("language", self.language_box.currentData())
        settings.set("timeFormat", self.time_format_edit.text())

        if self.builtin_strace_radio_button.isChecked():
            settings.set("useStrace", USE_STRACE_SETTINGS_VALUE.BUILT_IN)
        elif self.system_strace_radio_button.isChecked():
            settings.set("useStrace", USE_STRACE_SETTINGS_VALUE.SYSTEM)
        elif self.custom_strace_radio_button.isChecked():
            settings.set("useStrace", USE_STRACE_SETTINGS_VALUE.CUSTOM)

        settings.set("customStracePath", self.custom_strace_edit.text())

    def _ok_button_clicked(self) -> None:
        self._set_settings(self._env.settings)
        self._env.settings.save(os.path.join(self._env.data_dir, "settings.json"))
        self.close()

    def open_dialog(self) -> None:
        self._update_widgets(self._env.settings)
        self.open()
