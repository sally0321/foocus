from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QCursor

class LogInPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.banner_logo = QSvgWidget("resources/logos/foocus_banner_logo.svg")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.error_message_label = QLabel("")
        self.log_in_btn = QPushButton("Log in")
        self.sign_in_message_label = QLabel("Not registered?")
        self.create_acc_btn = QPushButton("Create an account")

        self.banner_logo.setFixedSize(500, 200)

        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("log_in_username_input")

        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("log_in_password_input")

        self.error_message_label.setObjectName("log_in_error_message_label")

        self.log_in_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.log_in_btn.setObjectName("log_in_btn")

        self.sign_in_message_label.setObjectName("sign_in_message_label")

        self.create_acc_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.create_acc_btn.setObjectName("create_acc_btn")

        self.layout.addStretch(1)
        self.layout.addWidget(self.banner_logo, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.username_input, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.password_input, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.error_message_label, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.log_in_btn, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.sign_in_message_label, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.create_acc_btn, alignment=Qt.AlignHCenter)
        self.layout.addStretch(1)

