import random

from PySide6.QtCore import QObject, Signal

from models.data import ActivityPageConfig
from views.activity_selection_page import ActivitySelectionPage

class ActivitySelectionPageController(QObject):
    page_selected = Signal(str) # Signal to notify the main window controller about page changes

    def __init__(self, page_title, activity_page_configs: list[ActivityPageConfig]):
        super().__init__()

        # Initialize activity selection page view
        self.view = ActivitySelectionPage(page_title, activity_page_configs)

        # Store the activity page configurations
        self.activity_page_configs = activity_page_configs

        # Connect each activity selection button to emit the corresponding page name when clicked for switching pages
        for idx, activity_page_config in enumerate(activity_page_configs):
            btn = self.view.activity_selection_btns[idx]
            btn.clicked.connect(lambda _, page_name=activity_page_config.page_name: self.page_selected.emit(page_name))

        # Connect Pick for Me button to emit a random activity page name
        activity_pages = [activity_page_config.page_name for activity_page_config in activity_page_configs]
        self.view.pick_for_me_btn.clicked.connect(lambda: self.page_selected.emit(random.choice(activity_pages)))
        
        self.view.back_btn.clicked.connect(lambda: self.page_selected.emit("back"))