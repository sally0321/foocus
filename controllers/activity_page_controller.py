from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QLabel, QVBoxLayout, QDialog

from models.data import ActivityPageConfig
from views.activity_page import ActivityPage
from utils.utils import resource_path

class ActivityPageController(QObject):
    is_notification = Signal() # Signal to notify the main window controller about the notification
    page_selected = Signal(str) # Signal to notify the main window controller about page changes

    def __init__(self, activity_page_config: ActivityPageConfig):
        super().__init__()

        # Initialize the activity page view
        self.view = ActivityPage(activity_page_config)

        self.view.back_btn.clicked.connect(lambda: self.page_selected.emit("back"))

        # Initialize the sound effect
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(resource_path("resources/audio/completion_noti_sound_effect.wav")))
        self.sound_effect.setVolume(1.0)
        
        # If there is a timer in the activity page, connect the timer finish signal to play the sound effect
        if activity_page_config.timer_duration:
            self.view.timer.timer.finished.connect(lambda: self.sound_effect.play())