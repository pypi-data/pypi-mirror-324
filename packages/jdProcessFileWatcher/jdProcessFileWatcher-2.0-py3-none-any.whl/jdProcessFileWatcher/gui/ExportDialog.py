from PyQt6.QtWidgets import QDialog, QFileDialog, QStyle
from ..ui_compiled.ExportDialog import Ui_ExportDialog
from ..core.Filter import PathFilter, FilterList
from .FilterWidgets import BasicFilterWidgets
from ..core.Exporter import get_all_exporter
from PyQt6.QtCore import QCoreApplication
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
import os


if TYPE_CHECKING:
    from ..Environment import Environment
    from .MainWindow import MainWindow


class ExportDialog(QDialog, Ui_ExportDialog):
    def __init__(self, env: "Environment", main_window: "MainWindow") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._exporter_list = get_all_exporter()
        for exporter in self._exporter_list:
            self.exporter_box.addItem(exporter.get_name(), exporter.get_id())

        self._data = main_window.get_file_changed_data()

        self._basic_filer_widgets = BasicFilterWidgets()
        self.filter_layout.addWidget(self._basic_filer_widgets)

        for current_data in self._data:
            self._basic_filer_widgets.add_data(current_data)

        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        self.cancel_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)))

        self.ok_button.clicked.connect(self._ok_button_clicked)
        self.cancel_button.clicked.connect(self.close)

    def _ok_button_clicked(self) -> None:
        for exporter in self._exporter_list:
            if exporter.get_id() == self.exporter_box.currentData():
                break
        else:
            return

        file_filter = exporter.get_file_filter() + ";;" + QCoreApplication.translate("ExportDialog", "All files") + " (*)"

        path = QFileDialog.getSaveFileName(self, directory=os.path.expanduser("~"), filter=file_filter)[0]

        if path == "":
            return

        filter_list = FilterList()

        if self.path_filter_edit.text() != "":
            filter_list.append(PathFilter(self.path_filter_edit.text().strip()))

        self._basic_filer_widgets.fill_filter_list(filter_list)

        exporter.export_data(path, filter_list.filter_list(self._data))

        self.close()
