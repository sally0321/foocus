from collections import deque

from PySide6.QtCore import QObject, Signal
import numpy as np

from views.focus_tracker_widget import FocusTrackerWidget

MAX_POINTS = 50

class FocusTrackerWidgetController(QObject):
    
    def __init__(self):
        super().__init__()

        self.view = FocusTrackerWidget()

        self.ear_values = deque(maxlen=MAX_POINTS)

    def update_plot(self, latest_ear_value):
        self.ear_values.append(latest_ear_value)

        self.view.ax.clear()
        self.view.ax.plot(self.ear_values, label="EAR", color="#04bfbf")
        self.view.ax.set_ylim(0, 0.5)
        self.view.ax.set_yticks(np.linspace(0, 0.5, 6))
        self.view.ax.set_xticks(np.linspace(0, 50, 6))
        self.view.ax.set_title("Focus Tracker")
        self.view.ax.set_xlabel("Frames")
        self.view.ax.set_ylabel("EAR")
        self.view.ax.legend()
        self.view.figure.tight_layout()

        self.view.canvas.draw_idle()

    def reset_plot(self):
        self.ear_values.clear()
        self.view.ax.clear()
        self.view.ax.set_title("Focus Tracker")
        self.view.ax.set_xlabel("Frames")
        self.view.ax.set_ylabel("EAR")
        self.view.ax.set_ylim(0, 0.5)
        self.view.ax.set_yticks(np.linspace(0, 0.5, 6))
        self.view.ax.set_xticks(np.linspace(0, 50, 6))
        self.view.figure.tight_layout()
        self.view.canvas.draw_idle()

        

