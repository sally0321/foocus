from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QCursor

from utils.utils import resource_path

class SignInPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        
        self.banner_logo = QSvgWidget(resource_path("resources/logos/foocus_banner_logo.svg"))
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_confirmation_input = QLineEdit()
        self.error_message_label = QLabel("")
        self.sign_in_btn = QPushButton("Sign in")
        self.log_in_message_label = QLabel("Already registered?")
        self.back_to_log_in_btn = QPushButton("Back to log in")
        
        self.banner_logo.setFixedSize(500, 200)

        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("sign_in_username_input")

        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("sign_in_password_input")

        self.password_confirmation_input.setPlaceholderText("Confirm password")
        self.password_confirmation_input.setEchoMode(QLineEdit.Password)
        self.password_confirmation_input.setObjectName("sign_in_password_confirmation_input")

        self.error_message_label.setObjectName("sign_in_error_message_label")

        self.sign_in_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.sign_in_btn.setObjectName("sign_in_btn")

        self.log_in_message_label.setObjectName("log_in_message_label")

        self.back_to_log_in_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_to_log_in_btn.setObjectName("back_to_log_in_btn")

        self.layout.addStretch(1)
        self.layout.addWidget(self.banner_logo, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.username_input, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.password_input, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.password_confirmation_input, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.error_message_label, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.sign_in_btn, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.log_in_message_label, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.back_to_log_in_btn, alignment=Qt.AlignHCenter)
        self.layout.addStretch(1)


