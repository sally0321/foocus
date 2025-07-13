from collections import deque

from PySide6.QtCore import QObject, Signal
import numpy as np

from views.focus_tracker_widget import FocusTrackerWidget

MAX_POINTS = 50

class FocusTrackerWidgetController(QObject):
    
    def __init__(self):
        super().__init__()

        # Initialize focus focus tracker widget view
        self.view = FocusTrackerWidget()

        # Store the last MAX_POINTS EAR values only
        self.ear_values = deque(maxlen=MAX_POINTS)

    def update_plot(self, latest_ear_value):
        """Update the plot with the latest EAR value."""
        self.ear_values.append(latest_ear_value)

        self.view.reset_plot()
        self.view.ax.plot(self.ear_values, label="EAR", color="#04bfbf")
        self.view.ax.legend()
    
    def reset_focus_tracker(self):
        """Reset the focus tracker widget to its initial state."""
        self.ear_values.clear()
        self.view.reset_plot()

        

