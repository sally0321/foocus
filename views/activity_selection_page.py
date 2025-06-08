from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

from models.data import ActivityPageConfig

class ActivitySelectionPage(QWidget):
    def __init__(self, page_title, activity_page_configs: list[ActivityPageConfig]):
        super().__init__()

        self.layout = QVBoxLayout(self)
        
        self.page_title = QLabel(page_title, alignment=Qt.AlignCenter)
        self.page_title.setProperty("role", "activity_selection_page_title")
        self.layout.addWidget(self.page_title)
        self.layout.addStretch(2)

        self.activity_selection_btns = []

        for activity_page_config in activity_page_configs:
            btn = QPushButton(activity_page_config.title)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setProperty("role", "activity_selection_btn")

            self.activity_selection_btns.append(btn)
            self.layout.addWidget(btn, alignment=Qt.AlignHCenter)
            self.layout.addStretch(1)

        self.pick_for_me_btn = QPushButton("Pick for me")
        self.pick_for_me_btn.setProperty("role", "pick_for_me_btn")
        self.pick_for_me_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.layout.addWidget(self.pick_for_me_btn, alignment=Qt.AlignHCenter)
        self.layout.addStretch(2)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
