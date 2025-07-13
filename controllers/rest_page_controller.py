from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QLabel, QVBoxLayout, QDialog

from views.rest_page import RestPage
from utils.utils import resource_path

class RestPageController(QObject):
    is_notification = Signal() # Signal to notify the main window controller about the notification
    page_selected = Signal(str) # Signal to notify the main window controller about page changes

    def __init__(self):
        super().__init__()

        self.view = RestPage()

        # Connect events to methods
        self.view.carousel_timer.timeout.connect(self.next_suggestion)
        self.view.sound_toggle.stateChanged.connect(self.toggle_sound)
        self.view.timer.timer.finished.connect(self.show_notification)
        self.view.timer_widget.stop_btn.clicked.connect(lambda: self.view.sound_toggle.setChecked(False))
        self.view.back_btn.clicked.connect(lambda: self.page_selected.emit("back"))

    def next_suggestion(self):
        """Iterate through the suggestions in the carousel."""

        self.view.current_index = (self.view.current_index + 1) % len(self.view.suggestions)
        self.view.suggestion_label.setText(self.view.suggestions[self.view.current_index])

    def toggle_sound(self, state):
        """Toggle the sound effect based on the checkbox state."""
        
        if state == 2: # Checked state
            self.view.sound_effect.play()
        else:
            self.view.sound_effect.stop()

    def show_notification(self):
        """Show a notification dialog when the timer finishes."""
        
        # Reset the sound toggle state and emit the notification signal
        self.view.sound_toggle.setChecked(False)
        self.is_notification.emit()

        # Create and display the notification dialog
        dialog_box = QDialog(self.view)
        dialog_box.setWindowTitle("Time's Up")
        dialog_box.setFixedSize(300, 150)
        dialog_box.setObjectName("notification")

        message_label = QLabel("Break is over. Time to get back and shine!")
        message_label.setWordWrap(True)
        message_label.setObjectName("noti_message_label")

        dialog_box_layout = QVBoxLayout(dialog_box)
        dialog_box_layout.addWidget(message_label)

        # Play the notification sound effect
        sound = QSoundEffect(source=QUrl.fromLocalFile(resource_path("resources/audio/noti_sound_effect.wav")))
        sound.setVolume(1)
        sound.play()

        dialog_box.exec()

