from PySide6.QtCore import QObject, Signal

from views.focus_zone_page import FocusZonePage

class FocusZonePageController(QObject):

    def __init__(self):
        super().__init__()

        self.view = FocusZonePage()

        self.view.attention_detector.latest_ear_value.connect(self.view.focus_tracker.update_plot)
        self.view.attention_detector.is_stop.connect(self.view.focus_tracker.reset_plot)
        self.view.attention_detector.is_stop.connect(self.view.timer.stop_timer)
        self.view.attention_detector.is_notification_start.connect(self.view.timer.toggle_timer)
        self.view.attention_detector.is_notification_end.connect(self.view.timer.toggle_timer)

        self.view.timer.view.play_pause_btn.clicked.connect(self.toggle_camera)
        self.view.timer.view.stop_btn.clicked.connect(self.stop_camera)
        self.view.timer.view.restart_btn.clicked.connect(self.restart_camera)
        self.view.timer.timer.finished.connect(self.stop_camera)

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

        