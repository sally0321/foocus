from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class InsightsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)

        self.attention_span_history = QWidget()
        self.avg_attention_span = QWidget()
        self.longest_attention_span = QWidget()
        self.unfocus_frequency = QWidget()

        self.attention_span_history_layout = QVBoxLayout(self.attention_span_history)
        self.avg_attention_span_layout = QVBoxLayout(self.avg_attention_span)
        self.longest_attention_span_layout = QVBoxLayout(self.longest_attention_span)
        self.unfocus_frequency_layout = QVBoxLayout(self.unfocus_frequency)

        # Create the attention span history figure and canvas that display the 5 most recent attention spans
        self.attention_span_history_figure = Figure(figsize=(5, 3))
        self.attention_span_history_canvas = FigureCanvas(self.attention_span_history_figure)
        self.attention_span_history_ax = self.attention_span_history_figure.add_subplot(111)
        self.attention_span_history_ax.set_title("Focus History")
        self.attention_span_history_ax.set_xlabel("Study Sessions")
        self.attention_span_history_ax.set_ylabel("Attention Span (minutes)")
        self.attention_span_history_ax.set_xlim(left=0)
        self.attention_span_history_ax.set_ylim(bottom=0)
        self.attention_span_history_figure.tight_layout()
        self.attention_span_history_layout.addWidget(self.attention_span_history_canvas)

        # Set figure background to transparent
        self.attention_span_history_figure.patch.set_facecolor('none')
        self.attention_span_history_ax.set_facecolor('none')
        self.attention_span_history_canvas.setAttribute(Qt.WA_TranslucentBackground)
        self.attention_span_history_canvas.setStyleSheet("background: transparent;")

        # Create the average attention span widget
        self.avg_attention_span_h1 = QLabel("Average")
        self.avg_attention_span_h2 = QLabel("Attention Span")
        self.avg_attention_span_stat = QLabel("18")
        self.avg_attention_span_h3 = QLabel("Minutes")
        self.avg_attention_span_layout.addStretch(1)
        self.avg_attention_span_layout.addWidget(self.avg_attention_span_h1, alignment=Qt.AlignHCenter)
        self.avg_attention_span_layout.addWidget(self.avg_attention_span_h2, alignment=Qt.AlignHCenter)
        self.avg_attention_span_layout.addWidget(self.avg_attention_span_stat, alignment=Qt.AlignHCenter)
        self.avg_attention_span_layout.addWidget(self.avg_attention_span_h3, alignment=Qt.AlignHCenter)
        self.avg_attention_span_layout.addStretch(1)

        # Create the longest attention span widget
        self.longest_attention_span_h1 = QLabel("Longest")
        self.longest_attention_span_h2 = QLabel("Attention Span")
        self.longest_attention_span_stat = QLabel("21")
        self.longest_attention_span_h3 = QLabel("Minutes")
        self.longest_attention_span_layout.addStretch(1)
        self.longest_attention_span_layout.addWidget(self.longest_attention_span_h1, alignment=Qt.AlignHCenter)
        self.longest_attention_span_layout.addWidget(self.longest_attention_span_h2, alignment=Qt.AlignHCenter)
        self.longest_attention_span_layout.addWidget(self.longest_attention_span_stat, alignment=Qt.AlignHCenter)
        self.longest_attention_span_layout.addWidget(self.longest_attention_span_h3, alignment=Qt.AlignHCenter)
        self.longest_attention_span_layout.addStretch(1)

        # Create the unfocus frequency widget containing the highest and lowest unfocus frequency widgets
        self.unfocus_frequency_h1 = QLabel("Frequency")
        self.unfocus_frequency_h2 = QLabel("of losing focus per session")
        self.unfocus_frequency_h2.setWordWrap(True)
        self.unfocus_frequency_h2.setAlignment(Qt.AlignCenter)
        
        # Create the highest unfocus frequency widget
        self.unfocus_frequency_highest_widget = QWidget()
        self.unfocus_frequency_highest_widget_layout = QVBoxLayout(self.unfocus_frequency_highest_widget)
        self.unfocus_frequency_highest_h3 = QLabel("Highest")
        self.unfocus_frequency_highest_stat = QLabel("15")
        self.unfocus_frequency_highest_widget_layout.addStretch(1)
        self.unfocus_frequency_highest_widget_layout.addWidget(self.unfocus_frequency_highest_h3, alignment=Qt.AlignHCenter)
        self.unfocus_frequency_highest_widget_layout.addWidget(self.unfocus_frequency_highest_stat, alignment=Qt.AlignHCenter)
        self.unfocus_frequency_highest_widget_layout.addStretch(1)
        
        # Create the lowest unfocus frequency widget
        self.unfocus_frequency_lowest_widget = QWidget()
        self.unfocus_frequency_lowest_widget_layout = QVBoxLayout(self.unfocus_frequency_lowest_widget)
        self.unfocus_frequency_lowest_h3 = QLabel("Lowest")
        self.unfocus_frequency_lowest_stat = QLabel("3")
        self.unfocus_frequency_lowest_widget_layout.addStretch(1)
        self.unfocus_frequency_lowest_widget_layout.addWidget(self.unfocus_frequency_lowest_h3, alignment=Qt.AlignHCenter)
        self.unfocus_frequency_lowest_widget_layout.addWidget(self.unfocus_frequency_lowest_stat, alignment=Qt.AlignHCenter)        
        self.unfocus_frequency_lowest_widget_layout.addStretch(1)
        
        self.unfocus_frequency_layout.addStretch(1)
        self.unfocus_frequency_layout.addWidget(self.unfocus_frequency_h1, alignment=Qt.AlignHCenter)
        self.unfocus_frequency_layout.addWidget(self.unfocus_frequency_h2, alignment=Qt.AlignHCenter)
        self.unfocus_frequency_layout.addStretch(1)
        self.unfocus_frequency_layout.addWidget(self.unfocus_frequency_highest_widget, alignment=Qt.AlignHCenter)
        self.unfocus_frequency_layout.addStretch(1)
        self.unfocus_frequency_layout.addWidget(self.unfocus_frequency_lowest_widget, alignment=Qt.AlignHCenter)
        self.unfocus_frequency_layout.addStretch(1)

        self.attention_span_history.setObjectName("attention_span_history")
        self.avg_attention_span.setObjectName("avg_attention_span")
        self.longest_attention_span.setObjectName("longest_attention_span")
        self.unfocus_frequency.setObjectName("unfocus_frequency")

        self.avg_attention_span_h1.setObjectName("avg_attention_span_h1")
        self.avg_attention_span_h2.setObjectName("avg_attention_span_h2")
        self.avg_attention_span_stat.setObjectName("avg_attention_span_stat")
        self.avg_attention_span_h3.setObjectName("avg_attention_span_h3")

        self.longest_attention_span_h1.setObjectName("longest_attention_span_h1")
        self.longest_attention_span_h2.setObjectName("longest_attention_span_h2")
        self.longest_attention_span_stat.setObjectName("longest_attention_span_stat")
        self.longest_attention_span_h3.setObjectName("longest_attention_span_h3")

        self.unfocus_frequency_h1.setObjectName("unfocus_frequency_h1")
        self.unfocus_frequency_h2.setObjectName("unfocus_frequency_h2")
        self.unfocus_frequency_highest_widget.setObjectName("unfocus_frequency_highest_widget")
        self.unfocus_frequency_highest_h3.setObjectName("unfocus_frequency_highest_h3")
        self.unfocus_frequency_highest_stat.setObjectName("unfocus_frequency_highest_stat")
        self.unfocus_frequency_lowest_widget.setObjectName("unfocus_frequency_lowest_widget")
        self.unfocus_frequency_lowest_h3.setObjectName("unfocus_frequency_lowest_h3")
        self.unfocus_frequency_lowest_stat.setObjectName("unfocus_frequency_lowest_stat")

        self.layout.addWidget(self.attention_span_history, 1, 1, 1, 3)
        self.layout.addWidget(self.avg_attention_span, 3, 1, 1, 1)
        self.layout.addWidget(self.longest_attention_span, 3, 3, 1, 1)
        self.layout.addWidget(self.unfocus_frequency, 1, 5, 3, 1)

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(2, 1)
        self.layout.setRowStretch(4, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(2, 1)
        self.layout.setColumnStretch(4, 1)
        self.layout.setColumnStretch(6, 1)