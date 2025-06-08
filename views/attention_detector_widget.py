from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class AttentionDetectorWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.base = QVBoxLayout(self)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        self.camera_feed_label = QLabel("Click start to activate the attention detector")
        # self.control_btns = QWidget()
        # self.control_btns_layout = QHBoxLayout(self.control_btns)
        # self.start_pause_btn = QPushButton("Start")
        # self.stop_btn = QPushButton("Stop")

        self.camera_feed_label.setFixedSize(600, 400)
        self.camera_feed_label.setAlignment(Qt.AlignCenter)

        # self.start_pause_btn.setCursor(QCursor(Qt.PointingHandCursor))
        # self.stop_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # self.control_btns_layout.addWidget(self.start_pause_btn, alignment=Qt.AlignHCenter)
        # self.control_btns_layout.addWidget(self.stop_btn, alignment=Qt.AlignHCenter)

        self.layout.addStretch()
        self.layout.addWidget(self.camera_feed_label, alignment=Qt.AlignHCenter)
        # self.layout.addWidget(self.control_btns, alignment=Qt.AlignHCenter)
        self.layout.addStretch()

        self.widget.setObjectName("camera_feed")

        self.base.setContentsMargins(0, 0, 0, 0)

        self.base.addWidget(self.widget)