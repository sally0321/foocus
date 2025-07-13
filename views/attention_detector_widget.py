from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class AttentionDetectorWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Display the classification of eye state (focused, blinking, sleeping)
        self.eye_status_label = QLabel("", alignment=Qt.AlignCenter)
        self.eye_status_label.setObjectName("eye_status_label")
        
        # Display the camera feed video with annotated eye landmarks and eye gaze direction
        self.camera_feed_label = QLabel("Click start to activate the attention detector 📷", alignment=Qt.AlignCenter)
        self.camera_feed_label.setFixedSize(600, 400)
        self.camera_feed_label.setObjectName("camera_feed_label")

        self.layout.addStretch()
        self.layout.addWidget(self.eye_status_label, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.camera_feed_label, alignment=Qt.AlignHCenter)
        self.layout.addStretch()
