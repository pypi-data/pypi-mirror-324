from PyQt6.QtWidgets import QTableWidget, QHeaderView, QComboBox
from .Constants import DEFAULT_TIME_FORMAT
from typing import Any
import subprocess
import datetime
import os


def clear_table_widget(table: QTableWidget):
    "Removes all Rows from a QTableWidget"
    while table.rowCount() > 0:
        table.removeRow(0)


def stretch_table_widget_colum_size(table: QTableWidget):
    """Stretch all Colums of a QTableWidget"""
    for i in range(table.horizontalHeader().count()):
        table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)


def select_combo_box_data(box: QComboBox, data: Any, default_index: int = 0) -> None:
    "Set the index to the item with the given data"
    index = box.findData(data)
    if index == -1:
        box.setCurrentIndex(default_index)
    else:
        box.setCurrentIndex(index)


def is_one_in_list(list_a: list, list_b: list) -> bool:
    for i in list_a:
        if i in list_b:
            return True
    return False


def format_time(time: datetime.time, time_format: str) -> str:
    try:
        return time.strftime(time_format)
    except ValueError:
        return time.strftime(DEFAULT_TIME_FORMAT)


def is_flatpak() -> bool:
    return os.path.exists("/.flatpak-info")


def is_process_running(pid: int) -> bool:
    "Check if a Process with the PID is running"
    if is_flatpak():
        return subprocess.run(["flatpak-spawn", "--host", "ps", str(pid)], capture_output=True).returncode == 0
    else:
         return subprocess.run(["ps", str(pid)], capture_output=True).returncode == 0


def list_processes() -> list[tuple[int, str]]:
    command = ["ps", "axco", "pid,command"]

    if is_flatpak():
        command = ["flatpak-spawn", "--host"] + command

    process_list: list[tuple[int, str]] = []

    lines = subprocess.run(command, capture_output=True).stdout.decode("utf-8").splitlines()

    for line in lines:
        pid, name = line.strip().split(" ", 1)

        try:
            process_list.append((int(pid), name))
        except ValueError:
            continue

    # The last process is ps itself, so we need to delete that
    del process_list[-1]

    return process_list
