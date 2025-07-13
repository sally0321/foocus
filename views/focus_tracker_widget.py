from PySide6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class FocusTrackerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Create a matplotlib figure and canvas for plotting
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        
        self.ax = self.figure.add_subplot(111)
        self.reset_plot()
        self.figure.tight_layout()
        
        self.layout.addWidget(self.canvas)

    def reset_plot(self):
        """Reset the plot to its initial state."""
        self.ax.clear()
        self.ax.set_ylim(0, 0.5)
        self.ax.set_yticks(np.linspace(0, 0.5, 6))
        self.ax.set_xticks(np.linspace(0, 50, 6))
        self.ax.set_xticklabels([]) # Hide x-axis tick labels for cleaner look
        self.ax.set_title("Focus Tracker")
        self.ax.set_xlabel("Elasped Time")
        self.ax.set_ylabel("Eye Aspect Ratio (EAR)")
        self.canvas.draw_idle()


