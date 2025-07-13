from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QCheckBox, QSizePolicy
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtGui import QCursor, QIcon

from utils.utils import resource_path

from controllers.timer_widget_controller import TimerWidgetController

class RestPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.top_widget = QWidget()
        self.top_widget_layout = QVBoxLayout(self.top_widget)
        self.top_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.top_widget_layout.setSpacing(0)

        self.bottom_widget = QWidget()
        self.bottom_widget_layout = QVBoxLayout(self.bottom_widget)
        self.bottom_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_widget_layout.setSpacing(0)

        # Suggestions of activities to do during the break
        self.suggestions = [
            "🚶‍♀️ Stretch your legs.",
            "🧘 Take 5 deep breaths.",
            "☕ Make a cup of tea.",
            "📱 Text someone hello.",
            "🎵 Listen to your favorite song.",
            "🧍‍♂️ Just sit and breathe for a while."
        ]
        self.current_index = 0
        self.suggestion_label = QLabel(self.suggestions[self.current_index])
        self.suggestion_label.setAlignment(Qt.AlignCenter)
        self.suggestion_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.suggestion_label.setObjectName("rest_page_suggestion_label")

        # Carousel timer to change the suggestion every 10 seconds
        self.carousel_timer = QTimer(self)
        self.carousel_timer.start(10000)  

        # Toggle the checkbox to play ambient music during the break
        self.sound_toggle = QCheckBox("Ambient Sound: Ocean Waves")
        self.sound_effect = QSoundEffect(source=QUrl.fromLocalFile(resource_path("resources/audio/ocean_sound_effect.wav")))
        self.sound_effect.setVolume(1)
        self.sound_effect.setLoopCount(-1)

        self.top_widget_layout.addStretch(3)
        self.top_widget_layout.addWidget(self.suggestion_label)
        self.top_widget_layout.addStretch(2)
        self.top_widget_layout.addWidget(self.sound_toggle, alignment=Qt.AlignHCenter)
        self.top_widget_layout.addStretch(1)

        self.back_btn = QPushButton(icon=QIcon(resource_path("resources/icons/back_icon.png")), parent=self.top_widget) 
        self.back_btn.move(10, 10) 
        self.back_btn.setObjectName("back_btn")
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Create a timer with default 5 minutes countdown for a break session
        self.timer = TimerWidgetController(300)
        self.timer_widget = self.timer.view
        self.bottom_widget_layout.addWidget(self.timer_widget)

        self.top_widget.setObjectName("rest_page_top_widget")
        self.bottom_widget.setObjectName("rest_page_bottom_widget")
        self.timer_widget.setObjectName("rest_page_timer")

        self.layout.addWidget(self.top_widget)
        self.layout.addWidget(self.bottom_widget)