from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import QSoundEffect

from models.data import ActivityPageConfig
from views.activity_page import ActivityPage

class ActivityPageController(QObject):
    def __init__(self, activity_page_config: ActivityPageConfig):
        super().__init__()

        self.view = ActivityPage(activity_page_config)

        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile("resources/audio/completion_noti_sound_effect.wav"))
        self.sound_effect.setVolume(1.0)

        if activity_page_config.timer_duration:
            self.view.timer.timer.finished.connect(lambda: self.sound_effect.play())
    
  
    
        