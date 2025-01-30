from PyQt6.QtWidgets import QComboBox, QWidget, QLabel, QHBoxLayout
from ..core.Filter import ActionFilter, ProcessFilter, FilterList
from PyQt6.QtCore import QCoreApplication, pyqtSignal
from ..Types import FileChangedData
from ..FileAction import FileAction


class ActionComboBox(QComboBox):
    def __init__(self) -> None:
        super().__init__()

        self._action_check: dict[FileAction, bool] = {}

    def reset(self) -> None:
        self.clear()
        self.addItem(QCoreApplication.translate("FilterWidgets", "All"))
        self.setCurrentIndex(0)
        self._action_check = {}

    def add_data(self, data: FileChangedData) -> None:
        if data.action in self._action_check:
            return

        self.addItem(FileAction.get_display_name(data.action), data.action)
        self._action_check[data.action] = True

    def get_filter(self) -> ActionFilter| None:
        if self.currentIndex() == 0:
            return None

        return ActionFilter(self.currentData())


class ProcessComboBox(QComboBox):
    def __init__(self) -> None:
        super().__init__()

        self._pid_dict: dict[int, tuple[str, int]] = {}

    def reset(self) -> None:
        self.clear()
        self.addItem(QCoreApplication.translate("FilterWidgets", "All"))
        self._pid_dict = {}
        self.setCurrentIndex(0)

    def add_data(self, data: FileChangedData) -> None:
        if data.pid not in self._pid_dict:
            self.addItem(f"{data.pid} ({data.process_name})", data.pid)
            self._pid_dict[data.pid] = (data.process_name, self.count() - 1)
            return

        if self._pid_dict[data.pid][0] != data.process_name:
            self.setItemText(self._pid_dict[data.pid][1], f"{data.pid} ({data.process_name})")

    def get_filter(self) -> ProcessFilter | None:
        if self.currentIndex() == 0:
            return None

        return ProcessFilter(self.currentData())


class BasicFilterWidgets(QWidget):
    filter_changed = pyqtSignal(FilterList)

    def __init__(self) -> None:
        super().__init__()

        self._action_box = ActionComboBox()
        self._process_box = ProcessComboBox()

        self._action_box.reset()
        self._process_box.reset()

        self._action_box.currentIndexChanged.connect(self._emit_filter_changed)
        self._process_box.currentIndexChanged.connect(self._emit_filter_changed)

        main_layout = QHBoxLayout()
        main_layout.addWidget(QLabel(QCoreApplication.translate("FilterWidgets", "Action:")))
        main_layout.addWidget(self._action_box)
        main_layout.addWidget(QLabel(QCoreApplication.translate("FilterWidgets", "Process:")))
        main_layout.addWidget(self._process_box)

        self.setLayout(main_layout)

    def _emit_filter_changed(self) -> None:
        filter_list = FilterList()
        self.fill_filter_list(filter_list)
        self.filter_changed.emit(filter_list)

    def fill_filter_list(self, filter_list: FilterList) -> None:
        if (action_filer := self._action_box.get_filter()) is not None:
            filter_list.append(action_filer)

        if (process_filer := self._process_box.get_filter()) is not None:
            filter_list.append(process_filer)

    def add_data(self, data: FileChangedData) -> None:
        self._action_box.add_data(data)
        self._process_box.add_data(data)

    def reset(self) -> None:
        self._action_box.reset()
        self._process_box.reset()
