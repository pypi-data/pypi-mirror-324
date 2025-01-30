from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo
from PyQt6.QtDBus import QDBusConnection
from PyQt6.QtWidgets import QApplication
from .Environment import Environment
import sys
import os


def main() -> None:
    if not os.path.isdir(os.path.join(os.path.dirname(__file__), "ui_compiled")):
        print("Could not find compiled ui files. Please run tools/CompileUI.py first.", file=sys.stderr)
        sys.exit(1)

    from .gui.MainWindow import MainWindow

    app = QApplication(sys.argv)

    env = Environment(app)

    app.setDesktopFileName("page.codeberg.JakobDev.jdProcessFileWatcher")
    app.setApplicationName("jdProcessFileWatcher")
    app.setApplicationVersion(env.version)
    app.setWindowIcon(env.icon)

    if env.settings.get("language") == "default":
        current_locale = QLocale()
    else:
        current_locale = QLocale(env.settings.get("language"))

    qt_translator = QTranslator()
    if qt_translator.load(current_locale, "qt", "_", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)):
        app.installTranslator(qt_translator)

    app_translator = QTranslator()
    if app_translator.load(current_locale, "jdProcessFileWatcher", "_", os.path.join(env.program_dir, "translations")):
        app.installTranslator(app_translator)

    main_window = MainWindow(env)
    main_window.show()

    if env.settings.get("welcomeDialogStartup"):
        main_window.welcome_dialog.open_dialog()

    conn = QDBusConnection.sessionBus()
    if conn.isConnected():
        if conn.registerService("page.codeberg.JakobDev.jdProcessFileWatcher"):
            from .dbus.jdProcessFileWatcherInterface import jdProcessFileWatcherInterface

            jdProcessFileWatcherInterface(conn, app, env, main_window)

            conn.registerObject("/page/codeberg/JakobDev/jdProcessFileWatcher", app)
        else:
            print(conn.lastError().message(), file=sys.stderr)

    sys.exit(app.exec())
