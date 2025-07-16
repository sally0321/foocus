from PySide6.QtCore import QObject, Signal, Qt, QTimer, QUrl
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from views.focus_zone_page import FocusZonePage
from utils.utils import resource_path
from datetime import datetime

class FocusZonePageController(QObject):

    def __init__(self):
        super().__init__()

        # Initialize the focus zone page view
        self.view = FocusZonePage()

        # Connect the signals to the methods
        self.view.attention_detector.latest_ear_value.connect(self.view.focus_tracker.update_plot)
        self.view.attention_detector.is_stop.connect(self.view.focus_tracker.reset_focus_tracker)
        self.view.attention_detector.is_stop.connect(self.view.timer.stop_timer)
        self.view.attention_detector.is_notification_start.connect(self.view.timer.toggle_timer)
        self.view.attention_detector.is_notification_end.connect(self.view.timer.toggle_timer)

        self.view.timer.timer.finished.connect(self.show_completion_notification) # show notification must come before stopping camera which resets the states
        self.view.timer.timer.finished.connect(self.stop_camera)

        # Connect the button events to the methods
        self.view.timer.view.play_pause_btn.clicked.disconnect(self.view.timer.toggle_timer) # Disconnect toggle_timer to trigger the toggle_camera first due to the delay in switching on the camera
        self.view.timer.view.play_pause_btn.clicked.connect(self.toggle_camera)
        self.view.timer.view.play_pause_btn.clicked.connect(self.view.timer.toggle_timer) # Toggle the timer after toggling the camera so the timer starts after the camera is ready

        self.view.timer.view.stop_btn.clicked.connect(self.stop_camera)
        self.view.timer.view.restart_btn.clicked.connect(self.restart_camera)
        
        # Initialize the audio output and media player for sound effects
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile(resource_path("resources/audio/completion_noti_sound_effect.wav")))

    def toggle_camera(self):
        """Toggle the camera on or off based on the timer state."""

        self.view.attention_detector.toggle_camera()
    
    def stop_camera(self):
        """Stop the camera when the timer is stopped."""

        self.view.attention_detector.stop_camera()
    
    def restart_camera(self):
        """Restart the camera when the timer is restarted."""

        if self.view.timer.timer._initial_time > 0:
            self.view.attention_detector.stop_camera()
            self.view.attention_detector.start_camera()

    def show_completion_notification(self, duration_ms=5000):
        """Show a notification when the focus session is completed."""

        # Determine the position of the notification based on the user's looking direction
        # The position of the notification is always opposite to the user's looking direction
        looking_direction = self.view.attention_detector.looking_direction
        match (looking_direction):
            case ("LEFT", "UP"):
                # Notification is displayed at the bottom right corner
                x = self.view.width() - 80
                y = self.view.height() - 80
            case ("LEFT", "DOWN"):
                # Notification is displayed at the upper right corner
                x = self.view.width() - 80
                y = 40
            case ("RIGHT", "UP"):
                # Notification is displayed at the bottom left corner
                x = 20
                y = self.view.height() - 80
            case ("RIGHT", "DOWN"):
                # Notification is displayed at the upper left corner
                x = 20
                y = 40

        # Create a notification widget        
        self.notif = QWidget() 
        self.notif.adjustSize()
        self.notif.move(x, y)
        layout = QVBoxLayout(self.notif)

        # Ensure the notification is always shown on top of other windows
        self.notif.setWindowFlags(
            Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        # Set the background color of the widget to transparent
        self.notif.setAttribute(Qt.WA_TranslucentBackground)
        self.notif.setAttribute(Qt.WA_ShowWithoutActivating)

        # Session completion message
        label = QLabel("Focus session completed! 🎉")
        label.setObjectName("completion_notification_label")
        layout.addWidget(label)
        
        self.notif.show()

        # Set the audio setting and play the audio
        self.audio_output.setVolume(0.1)
        self.media_player.setPosition(0)  # Play the audio from beginning
        self.media_player.play()

        # Automatically close the notification after a delay
        QTimer.singleShot(duration_ms, lambda: (self.notif.close(), setattr(self, 'notif', None)))
        