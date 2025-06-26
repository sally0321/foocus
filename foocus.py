import sqlite3
import ctypes
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from controllers.main_window_controller import MainWindowController
from utils.userdb_utils import initialize_userdb
from utils.sessiondb_utils import initialize_session_metrics_db
from utils.utils import *

# set unique app id for taskbar icon display
myappid = 'foocus.' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)

icon = QIcon(resource_path("resources/logos/foocus_logo.ico"))
app.setWindowIcon(icon)

with open(resource_path("style.qss"), "r") as f:
    # app.setStyleSheet(f.read())
    style = f.read()

style = adjust_qss_urls(style)
app.setStyleSheet(style)

initialize_userdb()
initialize_session_metrics_db()

main_window_controller = MainWindowController()
main_window_controller.run()

sys.exit(app.exec())