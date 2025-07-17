import sqlite3
import ctypes
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from controllers.main_window_controller import MainWindowController
from utils.userdb_utils import initialize_userdb
from utils.sessiondb_utils import initialize_session_metrics_db
from utils.utils import *

# Set unique app id for taskbar icon display
myappid = 'foocus.' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)

# Set the window icon
icon = QIcon(resource_path("resources/logos/foocus_logo.ico"))
app.setWindowIcon(icon)

# Adjust URLs in the stylesheet to point to the correct resources
with open(resource_path("style.qss"), "r") as f:
    style = f.read()
style = adjust_qss_urls(style)

app.setStyleSheet(style)

# Initialize and connect to SQLite database
initialize_userdb()
initialize_session_metrics_db()

main_window_controller = MainWindowController()
main_window_controller.run()

sys.exit(app.exec())