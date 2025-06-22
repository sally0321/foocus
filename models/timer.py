from PySide6.QtCore import QObject, QTimer, Signal

class Timer(QObject):
    remaining_time = Signal(int)
    finished = Signal()

    def __init__(self, initial_time):
        super().__init__()
        self._initial_time = initial_time
        self._remaining_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)

    def set_time(self, seconds):
        self._initial_time = seconds
        self._remaining_time = seconds
        self.remaining_time.emit(self._remaining_time)

    def start(self):
        if self._remaining_time > 0:
            self.timer.start(1000)

    def pause(self):
        self.timer.stop()

    def restart(self):
        self.reset()
        self.start()
    
    def reset(self):
        self._remaining_time = self._initial_time
        self.remaining_time.emit(self._remaining_time)

    def stop(self):
        self.timer.stop()
        self._remaining_time = 0
        self.remaining_time.emit(0)

    def _tick(self):
        self._remaining_time -= 1
        self.remaining_time.emit(self._remaining_time)
        if self._remaining_time <= 0:
            self.timer.stop()
            self.finished.emit()
