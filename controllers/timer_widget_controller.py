from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox

from views.timer_widget import TimerWidget
from models.timer import Timer
from utils.utils import resource_path

class TimerWidgetController(QObject):
    def __init__(self, initial_time):
        super().__init__()

        # Initialize the timer with the given initial time
        self.timer = Timer(initial_time)

        # Create the timer widget view
        self.view = TimerWidget(initial_time)

        # Connect the timer widget button events to the timer methods
        self.view.play_pause_btn.clicked.connect(self.toggle_timer)
        self.view.restart_btn.clicked.connect(self.restart_timer)
        self.view.stop_btn.clicked.connect(self.stop_timer)

        # Connect the timer widget signals to the timer methods
        self.timer.remaining_time.connect(self.update_time_display)
        self.timer.finished.connect(self.handle_timer_finished)

        self._is_running =False

    def toggle_timer(self):
        """Toggle the timer state between running and paused."""
        
        # Disable inputs while the timer is running or paused, only anable them when the timer is stopped
        self.view.minutes_input.setDisabled(True)
        self.view.seconds_input.setDisabled(True)

        if not self._is_running:
            # Set timer based on user's input
            if self.timer._remaining_time == 0:
                minutes = self.view.minutes_input.value()
                seconds = self.view.seconds_input.value()
                total_seconds = minutes * 60 + seconds
                if total_seconds  <= 0:
                    QMessageBox.warning(self.view, "Oppsie", "It seems like you have forgotten to set the timer.")
                else:
                    self.timer.set_time(total_seconds)
            # Start timer
            if self.timer._remaining_time > 0:
                self.timer.start()
                self._is_running = True
                self.view.play_pause_btn.setIcon(QIcon(resource_path("resources/icons/pause_icon.png")))
        else:
            # Pause timer
            self.timer.pause()
            self._is_running = False
            self.view.play_pause_btn.setIcon(QIcon(resource_path("resources/icons/play_icon.png")))

    def restart_timer(self):
        """Restart the timer with the initial time."""

        # Disable inputs while the timer is running, only anable them when the timer is stopped
        self.view.minutes_input.setDisabled(True)
        self.view.seconds_input.setDisabled(True)

        self.timer.restart()
        self._is_running = True
        self.view.play_pause_btn.setIcon(QIcon(resource_path("resources/icons/pause_icon.png")))

    def stop_timer(self):
        """Stop the timer."""

        # Enable inputs when the timer is stopped
        self.view.minutes_input.setEnabled(True)
        self.view.seconds_input.setEnabled(True)

        self.timer.stop()
        self._is_running = False
        self.view.play_pause_btn.setIcon(QIcon(resource_path("resources/icons/play_icon.png")))

    def handle_timer_finished(self):
        """Handle the timer finished event."""

        # Enable inputs when the timer is stopped
        self.view.minutes_input.setEnabled(True)
        self.view.seconds_input.setEnabled(True)
        
        self._is_running = False
        self.view.play_pause_btn.setIcon(QIcon(resource_path("resources/icons/play_icon.png")))

    def update_time_display(self, seconds):
        """Update the time display in the timer widget."""

        mins = seconds // 60
        secs = seconds % 60
        self.view.time_display.setText(f"{mins:02}:{secs:02}")


