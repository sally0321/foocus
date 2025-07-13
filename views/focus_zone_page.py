from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from controllers.timer_widget_controller import TimerWidgetController
from controllers.attention_detector_widget_controller import AttentionDetectorWidgetController
from controllers.focus_tracker_widget_controller import FocusTrackerWidgetController

class FocusZonePage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.top_widget = QWidget()
        self.top_widget.setObjectName("focus_zone_top_widget")
        self.top_widget_layout = QHBoxLayout(self.top_widget)
        self.top_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.top_widget_layout.setSpacing(0)

        self.bottom_widget = QWidget()
        self.bottom_widget.setObjectName("focus_zone_bottom_widget")
        self.bottom_widget_layout = QHBoxLayout(self.bottom_widget)
        self.bottom_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_widget_layout.setSpacing(0)

        self.timer_holder_widget = QWidget()
        self.timer_holder_widget.setObjectName("focus_zone_timer_holder_widget")
        self.timer_holder_widget_layout = QVBoxLayout(self.timer_holder_widget)
    
        # Create a timer widget with a default duration of 1500 seconds (25 minutes)
        self.timer = TimerWidgetController(1500)
        self.timer_widget = self.timer.view
        self.timer_widget.widget.setProperty("role", "focus_zone_timer")

        # Create an attention detector widget
        self.attention_detector = AttentionDetectorWidgetController()
        self.attention_detector_widget = self.attention_detector.view

        # Create a focus tracker widget
        self.focus_tracker = FocusTrackerWidgetController()
        self.focus_tracker_widget = self.focus_tracker.view
        self.focus_tracker_widget.setObjectName("focus_tracker_widget")

        self.timer_holder_widget_layout.addStretch()
        self.timer_holder_widget_layout.addWidget(self.timer_widget)
        self.timer_holder_widget_layout.addStretch()

        self.top_widget_layout.addStretch()
        self.top_widget_layout.addWidget(self.attention_detector_widget)
        self.top_widget_layout.addStretch()
        self.top_widget_layout.addWidget(self.timer_holder_widget)
        self.top_widget_layout.addStretch()

        self.bottom_widget_layout.addWidget(self.focus_tracker_widget)
        
        self.layout.addWidget(self.top_widget)
        self.layout.addWidget(self.bottom_widget)
        
        
        

