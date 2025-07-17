from PySide6.QtCore import QObject

from views.focus_zone_page import FocusZonePage

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

        self.view.timer.timer.finished.connect(self.view.attention_detector.show_completion_notification) # show notification must come before stopping camera which resets the states
        self.view.timer.timer.finished.connect(self.stop_camera)

        # Connect the button events to the methods
        self.view.timer.view.play_pause_btn.clicked.disconnect(self.view.timer.toggle_timer) # Disconnect toggle_timer to trigger the toggle_camera first due to the delay in switching on the camera
        self.view.timer.view.play_pause_btn.clicked.connect(self.toggle_camera)
        self.view.timer.view.play_pause_btn.clicked.connect(self.view.timer.toggle_timer) # Toggle the timer after toggling the camera so the timer starts after the camera is ready

        self.view.timer.view.stop_btn.clicked.connect(self.stop_camera)
        self.view.timer.view.restart_btn.clicked.connect(self.restart_camera)

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

        