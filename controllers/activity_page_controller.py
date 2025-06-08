from PySide6.QtCore import QObject, Signal

from models.data import ActivityPageConfig
from views.activity_page import ActivityPage

class ActivityPageController(QObject):
    def __init__(self, activity_page_config: ActivityPageConfig):
        super().__init__()

        self.view = ActivityPage(activity_page_config)
    
    
        