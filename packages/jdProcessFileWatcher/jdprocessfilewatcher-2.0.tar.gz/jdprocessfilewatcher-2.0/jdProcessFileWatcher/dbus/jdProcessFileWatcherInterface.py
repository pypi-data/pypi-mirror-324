from PyQt6.QtDBus import QDBusAbstractAdaptor, QDBusMessage, QDBusError, QDBusConnection
from PyQt6.QtCore import pyqtClassInfo, pyqtSlot, pyqtProperty
from ..Functions import is_process_running
from PyQt6.QtWidgets import QApplication
from ..Types import StartProcessInfo
from typing import TYPE_CHECKING
import desktop_entry_lib
import os


if TYPE_CHECKING:
    from ..Environment import Environment
    from ..gui.MainWindow import MainWindow


with open(os.path.join(os.path.dirname(__file__), "jdProcessFileWatcherInterface.xml"), "r", encoding="utf-8") as f:
    interface = f.read()


@pyqtClassInfo("D-Bus Interface", "page.codeberg.JakobDev.jdProcessFileWatcher")
@pyqtClassInfo("D-Bus Introspection", interface)
class jdProcessFileWatcherInterface(QDBusAbstractAdaptor):
    def __init__(self, connection: QDBusConnection,parent: QApplication, env: "Environment", main_window: "MainWindow") -> None:
        super().__init__(parent)

        self._env = env
        self._main_window = main_window
        self._connection = connection

    @pyqtSlot(str, str, QDBusMessage)
    def RunCommand(self, command: str, working_directory: str, msg: QDBusMessage) -> None:
        if command.strip() == "":
            self._connection.send(msg.createErrorReply(QDBusError.ErrorType.InvalidArgs, "command can't be empty"))
            return

        info = StartProcessInfo(["sh", "-c", command])

        if working_directory.strip() != "":
            info.working_directory = working_directory.strip()

        self._main_window.start_process(info)

    @pyqtSlot(str, str, QDBusMessage)
    def RunProgram(self, app_id: str, msg: QDBusMessage) -> None:
        if app_id.strip() == "":
            self._connection.send(msg.createErrorReply(QDBusError.ErrorType.InvalidArgs, "app_id can't be empty"))
            return

        collection = desktop_entry_lib.DesktopEntryCollection()
        collection.load_menu()

        try:
            entry = collection[app_id]
        except KeyError:
            self._connection.send(msg.createErrorReply(QDBusError.ErrorType.InvalidArgs, f"{app_id} was not found"))
            return

        info = StartProcessInfo(entry.get_command())
        info.working_directory = entry.get_working_directory()

        self._main_window.start_process(info)

    @pyqtSlot(int, QDBusMessage)
    def AttachProcess(self, pid: int, msg: QDBusMessage) -> None:
        if not is_process_running(pid):
            self._connection.send(msg.createErrorReply(QDBusError.ErrorType.InvalidArgs, f"There is no process with the PID {pid}"))
            return

        self._main_window.attach_process(pid)

    @pyqtProperty(str)
    def Version(self) -> str:
        return self._env.version

