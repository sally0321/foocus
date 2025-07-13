from PySide6.QtCore import QObject, Signal, Qt, QTimer, QUrl
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from views.focus_zone_page import FocusZonePage
from utils.utils import resource_path

class FocusZonePageController(QObject):

    def __init__(self):
        super().__init__()

        self.view = FocusZonePage()

        self.view.attention_detector.latest_ear_value.connect(self.view.focus_tracker.update_plot)
        self.view.attention_detector.is_stop.connect(self.view.focus_tracker.reset_focus_tracker)
        self.view.attention_detector.is_stop.connect(self.view.timer.stop_timer)
        self.view.attention_detector.is_notification_start.connect(self.view.timer.toggle_timer)
        self.view.attention_detector.is_notification_end.connect(self.view.timer.toggle_timer)

        self.view.timer.view.play_pause_btn.clicked.connect(self.toggle_camera)
        self.view.timer.view.stop_btn.clicked.connect(self.stop_camera)
        self.view.timer.view.restart_btn.clicked.connect(self.restart_camera)
        self.view.timer.timer.finished.connect(self.show_completion_notification) # show notification before stopping camera which resets the states
        self.view.timer.timer.finished.connect(self.stop_camera)

        # self.sound_effect = QSoundEffect()
        # self.sound_effect.setSource(QUrl.fromLocalFile(resource_path("resources/audio/completion_noti_sound_effect.wav")))
        # self.sound_effect.setVolume(0.5)
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile(resource_path("resources/audio/completion_noti_sound_effect.wav")))

    def toggle_camera(self):
        if self.view.timer.timer._remaining_time > 0:
            self.view.attention_detector.toggle_camera()
    
    def stop_camera(self):
        self.view.attention_detector.stop_camera()
        # self.view.timer.timer._remaining_time = self.view.timer.timer._initial_time
    
    def restart_camera(self):
        if self.view.timer.timer._initial_time > 0:
            self.view.attention_detector.stop_camera()
            self.view.attention_detector.start_camera()

    def show_completion_notification(self, duration_ms=5000):
        looking_direction = self.view.attention_detector.looking_direction
        print(f"Looking direction: {looking_direction}")
        match (looking_direction):
            case ("LEFT", "UP"):
                x = self.view.width() - 80
                y = self.view.height() - 80
            case ("LEFT", "DOWN"):
                x = self.view.width() - 80
                y = 40
            case ("RIGHT", "UP"):
                x = 20
                y = self.view.height() - 80
            case ("RIGHT", "DOWN"):
                x = 20
                y = 40
                
        self.notif = QWidget()  # <-- Keep reference
        self.notif.setWindowFlags(
            Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.notif.setAttribute(Qt.WA_TranslucentBackground)
        self.notif.setAttribute(Qt.WA_ShowWithoutActivating)

        label = QLabel("Focus session completed! 🎉")
        label.setObjectName("completion_notification_label")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.notif.setLayout(layout)
        self.notif.adjustSize()
        self.notif.move(x, y)

        self.notif.show()
        self.audio_output.setVolume(0.1)
        self.media_player.setPosition(0)  # Restart from beginning
        self.media_player.play()

        # Automatically close the notification after a delay
        QTimer.singleShot(duration_ms, lambda: (self.notif.close(), setattr(self, 'notif', None)))
        