from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QLabel, QVBoxLayout, QDialog

from views.rest_page import RestPage
from utils.utils import resource_path

class RestPageController(QObject):
    is_notification = Signal()

    def __init__(self):
        super().__init__()

        self.view = RestPage()

        self.view.carousel_timer.timeout.connect(self.next_suggestion)
        self.view.sound_toggle.stateChanged.connect(self.toggle_sound)
        self.view.timer.timer.finished.connect(self.show_notification)
        self.view.timer_widget.stop_btn.clicked.connect(lambda: self.view.sound_toggle.setChecked(False))

    def next_suggestion(self):
        self.view.current_index = (self.view.current_index + 1) % len(self.view.suggestions)
        self.view.suggestion_label.setText(self.view.suggestions[self.view.current_index])

    def toggle_sound(self, state):
        if state == 2:
            self.view.sound_effect.play()
        else:
            self.view.sound_effect.stop()

    def show_notification(self):
        self.view.sound_toggle.setChecked(False)
        self.is_notification.emit()

        dialog_box = QDialog(self.view)
        dialog_box.setWindowTitle("Time's Up")
        dialog_box.setFixedSize(300, 150)
        dialog_box.setObjectName("notification")

        message_label = QLabel("Break is over. Time to get back and shine!")
        message_label.setWordWrap(True)
        message_label.setObjectName("noti_message_label")

        dialog_box_layout = QVBoxLayout(dialog_box)
        dialog_box_layout.addWidget(message_label)

        sound = QSoundEffect(source=QUrl.fromLocalFile(resource_path("resources/audio/noti_sound_effect.wav")))
        sound.setVolume(1)
        sound.play()

        dialog_box.exec()

