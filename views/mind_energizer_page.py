from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QCursor, QIcon, QPixmap

class MindEnergizerPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create widgets to hold the buttons for selecting the category of mind energizer
        self.mindfulness_activity_widget = QWidget()
        self.mindfulness_activity_widget_layout = QVBoxLayout(self.mindfulness_activity_widget)

        self.physical_activity_widget = QWidget()
        self.physical_activity_widget_layout = QVBoxLayout(self.physical_activity_widget)

        self.rest_widget = QWidget()
        self.rest_widget_layout = QVBoxLayout(self.rest_widget)

        # Create buttons for each mind energizer category
        self.mindfulness_activity_btn = QPushButton("Mindfulness Activity")
        self.physical_activity_btn = QPushButton("Physical Exercise")
        self.rest_btn = QPushButton("Take a Break")

        self.mindfulness_activity_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.physical_activity_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.rest_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.mindfulness_activity_btn.setObjectName("mindfulness_activity_btn")
        self.physical_activity_btn.setObjectName("physical_exercise_btn")
        self.rest_btn.setObjectName("rest_btn")

        self.mindfulness_activity_widget_layout.addWidget(self.mindfulness_activity_btn, alignment=Qt.AlignCenter)
        self.physical_activity_widget_layout.addWidget(self.physical_activity_btn, alignment=Qt.AlignCenter)
        self.rest_widget_layout.addWidget(self.rest_btn, alignment=Qt.AlignCenter)

        self.layout.addStretch(2)
        self.layout.addWidget(self.mindfulness_activity_widget)
        self.layout.addStretch(1)
        self.layout.addWidget(self.physical_activity_widget)
        self.layout.addStretch(1)
        self.layout.addWidget(self.rest_widget)
        self.layout.addStretch(2)

        