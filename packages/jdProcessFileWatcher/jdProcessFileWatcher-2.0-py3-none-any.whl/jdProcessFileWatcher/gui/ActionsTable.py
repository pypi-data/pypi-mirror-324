from PyQt6.QtWidgets import QWidget, QAbstractItemView, QMenu, QApplication
from ..Functions import stretch_table_widget_colum_size
from ..ui_compiled.ActionsTable import Ui_ActionsTable
from PyQt6.QtCore import Qt, QCoreApplication, QPoint
from PyQt6.QtGui import QStandardItemModel, QAction
from ..core.Filter import PathFilter, FilterList
from .FilterWidgets import BasicFilterWidgets
from typing import Any, TYPE_CHECKING
from ..Types import FileChangedData


if TYPE_CHECKING:
    from ..Environment import Environment


class _CustomItemModel(QStandardItemModel):
    def data(self, index: int, role: int) -> Any:
        if role == Qt.ItemDataRole.ToolTipRole:
            return str(super().data(index, Qt.ItemDataRole.DisplayRole))
        else:
            return super().data(index, role)


class ActionsTable(QWidget, Ui_ActionsTable):
    def __init__(self, env: "Environment", autoscroll: bool) -> None:
        super().__init__()

        self.setupUi(self)

        self._env = env
        self._autoscroll = autoscroll
        self._data_list: list[FileChangedData] = []

        self._current_filter = FilterList()

        self._model = _CustomItemModel(0, 5)
        self.main_table.setModel(self._model)
        stretch_table_widget_colum_size(self.main_table)
        self.main_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.main_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self._model.setHorizontalHeaderLabels((
            QCoreApplication.translate("ActionsTable", "Action"),
            QCoreApplication.translate("ActionsTable", "Time"),
            QCoreApplication.translate("ActionsTable", "Path"),
            QCoreApplication.translate("ActionsTable", "PID"),
            QCoreApplication.translate("ActionsTable", "Process name"),
        ))

        self._basic_filter_widgets = BasicFilterWidgets()
        self.main_layout.addWidget(self._basic_filter_widgets)

        self.main_table.customContextMenuRequested.connect(self._open_context_menu)
        self.path_filter_edit.textChanged.connect(self._update_filter_list)
        self._basic_filter_widgets.filter_changed.connect(self._update_filter_list)

    def _open_context_menu(self, pos: QPoint) -> None:
        index_list = self.main_table.selectedIndexes()

        if len(index_list) == 0:
            return

        menu = QMenu(self)

        copy_action_action = QAction(QCoreApplication.translate("ActionsTable", "Copy Action"), self)
        copy_action_action.triggered.connect(lambda: QApplication.clipboard().setText(str(index_list[0].data(Qt.ItemDataRole.DisplayRole))))
        menu.addAction(copy_action_action)

        copy_time_action = QAction(QCoreApplication.translate("ActionsTable", "Copy Time"), self)
        copy_time_action.triggered.connect(lambda: QApplication.clipboard().setText(str(index_list[1].data(Qt.ItemDataRole.DisplayRole))))
        menu.addAction(copy_time_action)

        copy_path_action = QAction(QCoreApplication.translate("ActionsTable", "Copy Path"), self)
        copy_path_action.triggered.connect(lambda: QApplication.clipboard().setText(str(index_list[2].data(Qt.ItemDataRole.DisplayRole))))
        menu.addAction(copy_path_action)

        copy_pid_action = QAction(QCoreApplication.translate("ActionsTable", "Copy PID"), self)
        copy_pid_action.triggered.connect(lambda: QApplication.clipboard().setText(str(index_list[3].data(Qt.ItemDataRole.DisplayRole))))
        menu.addAction(copy_pid_action)

        copy_process_name_action = QAction(QCoreApplication.translate("ActionsTable", "Copy Process name"), self)
        copy_process_name_action.triggered.connect(lambda: QApplication.clipboard().setText(str(index_list[4].data(Qt.ItemDataRole.DisplayRole))))
        menu.addAction(copy_process_name_action)

        menu.popup(self.main_table.mapToGlobal(pos))

    def _update_filter_list(self) -> None:
        self._current_filter = FilterList()
        self._basic_filter_widgets.fill_filter_list(self._current_filter)

        if self.path_filter_edit.text() != "":
            self._current_filter.append(PathFilter(self.path_filter_edit.text().strip()))

        self._model.removeRows(0, self._model.rowCount())
        for data in self._current_filter.filter_list(self._data_list):
            data.create_table_row(self._env.settings.get("timeFormat"))
            self._model.appendRow(data.table_row)

    def add_data(self, data: FileChangedData) -> None:
        self._data_list.append(data)

        self._basic_filter_widgets.add_data(data)

        if self._current_filter.check_data(data):
            self._model.appendRow(data.table_row)

        if self._autoscroll:
            self.main_table.scrollToBottom()

    def get_all_data(self) -> list[FileChangedData]:
        return self._data_list

    def clear(self) -> None:
        self._data_list.clear()
        self._model.removeRows(0, self._model.rowCount())
        self._basic_filter_widgets.reset()
        self.path_filter_edit.setText("")
        self._current_filter = FilterList()
