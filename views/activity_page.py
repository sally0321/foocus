from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

from models.data import ActivityPageConfig
from controllers.timer_widget_controller import TimerWidgetController
from utils.utils import resource_path

class ActivityPage(QWidget):
    def __init__(self, activity_page_config: ActivityPageConfig):
        super().__init__()

        self.page_config = activity_page_config

        self.layout = QVBoxLayout(self)

        self.page_title = QLabel(activity_page_config.title, alignment=Qt.AlignCenter)
        self.page_title.setProperty("role", "activity_page_title")
        self.back_btn = QPushButton(icon=QIcon(resource_path("resources/icons/back_icon.png")), parent=self.page_title) 
        self.back_btn.move(10, 10) 
        self.back_btn.setObjectName("back_btn")
        self.layout.addWidget(self.page_title)
        
        self.video = QWebEngineView(url=QUrl(activity_page_config.video_embed_link))
        self.layout.addWidget(self.video)
        
        if activity_page_config.text:
            self.description = QLabel(activity_page_config.text, alignment=Qt.AlignCenter, wordWrap=True)
            self.description.setProperty("role", "activity_page_description")
            self.layout.addWidget(self.description)
        if activity_page_config.timer_duration:
            self.timer = TimerWidgetController(activity_page_config.timer_duration)
            self.timer_widget = self.timer.view
            self.layout.addWidget(self.timer_widget)
        
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)