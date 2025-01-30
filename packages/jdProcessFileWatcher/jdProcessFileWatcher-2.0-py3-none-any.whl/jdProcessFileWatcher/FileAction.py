from PyQt6.QtCore import QCoreApplication
import enum

class FileAction(int, enum.Enum):
    OPEN = 0
    CLOSE = enum.auto()
    READ_FILE = enum.auto()
    WRITE_FILE = enum.auto()
    READ_STATUS = enum.auto()
    READ_DIRECTORY = enum.auto()
    CHANGE_PERMISSION = enum.auto()
    READ_FILESYSTEM_INFO = enum.auto()
    CHANGE_WORKING_DIRECTORY = enum.auto()
    READ_PERMISSION = enum.auto()
    READ_LINK = enum.auto()
    UNKNOWN = enum.auto()

    @staticmethod
    def get_internal_name(action: int) -> str:
        match action:
            case FileAction.OPEN:
                return "Open"
            case FileAction.CLOSE:
                return "Close"
            case FileAction.READ_FILE:
                return "Read file"
            case FileAction.WRITE_FILE:
                return "Write file"
            case FileAction.READ_STATUS:
                return "Read file status"
            case FileAction.READ_DIRECTORY:
                return "Read directory"
            case FileAction.CHANGE_PERMISSION:
                return "Change permission"
            case FileAction.READ_FILESYSTEM_INFO:
                return "Read filesystem info"
            case FileAction.CHANGE_WORKING_DIRECTORY:
                return "Change working directory"
            case FileAction.READ_PERMISSION:
                return "Read permission"
            case FileAction.READ_LINK:
                return "Read link"
            case FileAction.UNKNOWN:
                return "Unknown"
            case _:
                return "Error"

    @staticmethod
    def get_display_name(action: int) -> str:
        match action:
            case FileAction.OPEN:
                return QCoreApplication.translate("FileAction", "Open")
            case FileAction.CLOSE:
                return QCoreApplication.translate("FileAction", "Close")
            case FileAction.READ_FILE:
                return QCoreApplication.translate("FileAction", "Read file")
            case FileAction.WRITE_FILE:
                return QCoreApplication.translate("FileAction", "Write file")
            case FileAction.READ_STATUS:
                return QCoreApplication.translate("FileAction", "Read file status")
            case FileAction.READ_DIRECTORY:
                return QCoreApplication.translate("FileAction", "Read directory")
            case FileAction.CHANGE_PERMISSION:
                return QCoreApplication.translate("FileAction", "Change permission")
            case FileAction.READ_FILESYSTEM_INFO:
                return QCoreApplication.translate("FileAction", "Read filesystem info")
            case FileAction.CHANGE_WORKING_DIRECTORY:
                return QCoreApplication.translate("FileAction", "Change working directory")
            case FileAction.READ_PERMISSION:
                return QCoreApplication.translate("FileAction", "Read permission")
            case FileAction.READ_LINK:
                return QCoreApplication.translate("FileAction", "Read link")
            case FileAction.UNKNOWN:
                return QCoreApplication.translate("FileAction", "Unknown")
            case _:
                return QCoreApplication.translate("FileAction", "Error")
