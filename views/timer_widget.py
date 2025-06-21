from mimetypes import init
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSpinBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QCursor

class TimerWidget(QWidget):
    
    def __init__(self, initial_time):
        super().__init__()

        self.base = QVBoxLayout(self)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # self.time_display = QLabel(f"{(initial_time // 60):02}:{(initial_time % 60):02}")
        self.time_display = QLabel("00:00")
        
        self.time_selector = QWidget()
        self.time_selector_layout = QHBoxLayout(self.time_selector)
        self.minutes_input = QSpinBox()
        self.seconds_input = QSpinBox()

        self.control_btns = QWidget()
        self.control_btns_layout = QHBoxLayout(self.control_btns)
        self.play_pause_btn = QPushButton(icon=QIcon("resources/icons/play_icon.png"))
        self.restart_btn = QPushButton(icon=QIcon("resources/icons/restart_icon.png"))
        self.stop_btn = QPushButton(icon=QIcon("resources/icons/stop_icon.png"))

        self.minutes_input.setRange(0, 59)
        self.minutes_input.setSuffix(" min")
        self.minutes_input.setValue(initial_time // 60)
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setSuffix(" sec")
        self.seconds_input.setValue(initial_time % 60)

        self.play_pause_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.restart_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.time_selector_layout.addStretch()
        self.time_selector_layout.addWidget(self.minutes_input)
        self.time_selector_layout.addWidget(self.seconds_input)
        self.time_selector_layout.addStretch()

        self.control_btns_layout.addWidget(self.restart_btn)
        self.control_btns_layout.addSpacing(50)
        self.control_btns_layout.addWidget(self.play_pause_btn)
        self.control_btns_layout.addSpacing(50)
        self.control_btns_layout.addWidget(self.stop_btn)

        self.widget.setObjectName("timer")
        
        self.time_selector.setObjectName("time_selector")

        self.layout.addWidget(self.time_display, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.time_selector, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.control_btns, alignment=Qt.AlignCenter)

        self.base.setContentsMargins(0, 0, 0, 0)
        
        self.base.addWidget(self.widget)
