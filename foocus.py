import sqlite3
import ctypes
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from controllers.main_window_controller import MainWindowController
from utils.userdb_utils import initialize_userdb
from utils.sessiondb_utils import initialize_session_metrics_db

# set unique app id for taskbar icon display
myappid = 'foocus.' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)

icon = QIcon("resources/logos/foocus_logo.ico")
app.setWindowIcon(icon)

with open("style.qss", "r") as f:
    app.setStyleSheet(f.read())

initialize_userdb()
initialize_session_metrics_db()

main_window_controller = MainWindowController()
main_window_controller.run()

sys.exit(app.exec())