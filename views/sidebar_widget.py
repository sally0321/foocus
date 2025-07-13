from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
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
        self.home_page_btn.setObjectName("sidebar_btn")
        self.focus_zone_page_btn.setObjectName("sidebar_btn")
        self.mind_energizer_page_btn.setObjectName("sidebar_btn")
        self.insights_page_btn.setObjectName("sidebar_btn")
        self.leaderboard_page_btn.setObjectName("sidebar_btn")

        self.profile_widget = QWidget()
        self.profile_widget_layout = QHBoxLayout(self.profile_widget)
        self.user_btn = QPushButton(icon=QIcon(resource_path("resources/icons/user_icon.png")), text="You")
        self.user_btn.setDisabled(True)
        self.user_btn.setObjectName("sidebar_btn")
        self.logout_btn = QPushButton(icon=QIcon(resource_path("resources/icons/logout_icon.png")))
        self.logout_btn.setFixedSize(40, 40)
        self.logout_btn.setObjectName("sidebar_logout_btn")
        self.profile_widget_layout.addWidget(self.user_btn)
        self.profile_widget_layout.addStretch()
        self.profile_widget_layout.addWidget(self.logout_btn)

        self.home_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.focus_zone_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.mind_energizer_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.insights_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.leaderboard_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.logout_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.layout.addWidget(self.home_page_btn)
        self.layout.addWidget(self.focus_zone_page_btn)
        self.layout.addWidget(self.mind_energizer_page_btn)
        self.layout.addWidget(self.insights_page_btn)
        self.layout.addWidget(self.leaderboard_page_btn)
        self.layout.addStretch()
        self.layout.addWidget(self.profile_widget)

        self.widget.setObjectName("sidebar")

        self.base.addWidget(self.widget)
        self.base.setContentsMargins(0, 0, 0, 0)

        self.setMinimumWidth(250)
        self.setContentsMargins(0, 0, 0, 0)
        