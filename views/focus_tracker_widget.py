import sys
import random

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class FocusTrackerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        
        self.ax = self.figure.add_subplot(111)
        self.ax.set_ylim(0, 0.5)
        self.ax.set_yticks(np.linspace(0, 0.5, 6))
        self.ax.set_xticks(np.linspace(0, 50, 6))
        self.ax.set_title("Focus Tracker")
        self.ax.set_xlabel("Frames")
        self.ax.set_ylabel("EAR")
        self.figure.tight_layout()
        
        self.layout.addWidget(self.canvas)


