from PySide6.QtCore import QObject, QTimer, Signal
from datetime import datetime

class Timer(QObject):
    """A countdown timer that emits signals for remaining time and when finished."""
    remaining_time = Signal(int)
    finished = Signal()

    def __init__(self, default_initial_time):
        super().__init__()
        self.DEFAULT_INITIAL_TIME = default_initial_time
        self._initial_time = default_initial_time
        self._remaining_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)

    def set_time(self, seconds):
        """Set the timer to a specific number of seconds."""
        self._initial_time = seconds
        self._remaining_time = seconds
        self.remaining_time.emit(self._remaining_time)

    def start(self):
        """Start the countdown timer with 1 second interval."""
        if self._remaining_time > 0:
            self.timer.start(1000) 

    def pause(self):
        """Pause the countdown timer."""
        self.timer.stop()

    def restart(self):
        """Restart the countdown timer from the initial time."""
        self._remaining_time = self._initial_time
        self.remaining_time.emit(self._remaining_time)
        self.start()
    
    def reset(self):
        """Reset the countdown timer to the default initial time."""

        self._initial_time = self.DEFAULT_INITIAL_TIME

    def stop(self):
        """Stop the countdown timer and reset remaining time to zero."""
        self.remaining_time.emit(0)
        self.timer.stop()
        self._remaining_time = 0
        

    def _tick(self):
        """Decrement the remaining time by 1 second and emit the signal."""
        self._remaining_time -= 1
        self.remaining_time.emit(self._remaining_time)
        if self._remaining_time <= 0:
            self.finished.emit()
            self.timer.stop()
            
