from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QLabel, QVBoxLayout, QDialog

from models.data import ActivityPageConfig
from views.activity_page import ActivityPage
from utils.utils import resource_path

class ActivityPageController(QObject):
    is_notification = Signal()
    page_selected = Signal(str)

    def __init__(self, activity_page_config: ActivityPageConfig):
        super().__init__()

        self.view = ActivityPage(activity_page_config)

        self.view.back_btn.clicked.connect(lambda: self.page_selected.emit("back"))

        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(resource_path("resources/audio/completion_noti_sound_effect.wav")))
        self.sound_effect.setVolume(1.0)
        
        if activity_page_config.timer_duration:
            self.view.timer.timer.finished.connect(lambda: self.sound_effect.play())
            # self.view.timer.timer.finished.connect(self.show_notification)

    # def show_notification(self):
    #     self.is_notification.emit()

    #     dialog_box = QDialog(self.view)
    #     dialog_box.setWindowTitle("Time's Up")
    #     dialog_box.setFixedSize(300, 150)
    #     dialog_box.setObjectName("notification")

    #     message_label = QLabel("Break is over. Time to get back and shine!")
    #     message_label.setWordWrap(True)
    #     message_label.setObjectName("noti_message_label")

    #     dialog_box_layout = QVBoxLayout(dialog_box)
    #     dialog_box_layout.addWidget(message_label)

    #     sound = QSoundEffect(source=QUrl.fromLocalFile(resource_path("resources/audio/noti_sound_effect.wav")))
    #     sound.setVolume(1)
    #     sound.play()

    #     dialog_box.exec()
    
  
    
        