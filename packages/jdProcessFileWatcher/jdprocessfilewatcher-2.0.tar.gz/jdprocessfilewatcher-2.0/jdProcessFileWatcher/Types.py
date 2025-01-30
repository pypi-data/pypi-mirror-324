from PyQt6.QtGui import QStandardItem
from .FileAction import FileAction
from .Functions import format_time
import dataclasses
import datetime


@dataclasses.dataclass
class FileChangedData:
    action: FileAction
    path: str
    time: datetime.time
    pid: int
    process_name: str
    table_row: list[QStandardItem] = dataclasses.field(init=False)

    def create_table_row(self, time_format: str) -> None:
        self.table_row = [
            QStandardItem(FileAction.get_display_name(self.action)),
            QStandardItem(format_time(self.time, time_format)),
            QStandardItem(self.path),
            QStandardItem(str(self.pid)),
            QStandardItem(self.process_name)
        ]


@dataclasses.dataclass
class StartProcessInfo:
    cmdline: list[str]
    working_directory: str | None = None
