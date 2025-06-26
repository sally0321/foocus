from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QCursor

from utils.utils import resource_path

class SidebarWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.base = QVBoxLayout(self)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        self.home_page_btn = QPushButton(icon=QIcon(resource_path("resources/icons/home_icon.png")), text="Home")
        self.focus_zone_page_btn = QPushButton(icon=QIcon(resource_path("resources/icons/focus_zone_icon.png")), text="Focus Zone")
        self.mind_energizer_page_btn = QPushButton(icon=QIcon(resource_path("resources/icons/mind_energizer_icon.png")), text="Mind Energizer")
        self.insights_page_btn = QPushButton(icon=QIcon(resource_path("resources/icons/insights_icon.png")), text="Insights")
        self.leaderboard_page_btn = QPushButton(icon=QIcon(resource_path("resources/icons/leaderboard_icon.png")), text="Leaderboard")

        self.user_btn = QPushButton(icon=QIcon(resource_path("resources/icons/user_icon.png")), text="You")
        self.user_btn.setDisabled(True)

        self.home_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.focus_zone_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.mind_energizer_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.insights_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.leaderboard_page_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.layout.addWidget(self.home_page_btn)
        self.layout.addWidget(self.focus_zone_page_btn)
        self.layout.addWidget(self.mind_energizer_page_btn)
        self.layout.addWidget(self.insights_page_btn)
        self.layout.addWidget(self.leaderboard_page_btn)
        self.layout.addStretch()
        self.layout.addWidget(self.user_btn)

        self.widget.setObjectName("sidebar")

        self.base.addWidget(self.widget)
        self.base.setContentsMargins(0, 0, 0, 0)

        self.setMinimumWidth(250)
        self.setContentsMargins(0, 0, 0, 0)
        