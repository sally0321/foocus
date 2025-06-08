from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.foocus_monster_widget = QWidget()
        
        self.foocus_eyes = QSvgWidget("resources/logos/foocus_eyes.svg", parent=self.foocus_monster_widget)
        self.foocus_mouth = QLabel(parent=self.foocus_monster_widget)
        
        self.total_focus_duration = QWidget(parent=self.foocus_monster_widget)
        self.total_focus_duration_layout = QVBoxLayout(self.total_focus_duration)
        self.total_focus_duration_h1 = QLabel("Total")
        self.total_focus_duration_h2 = QLabel("Focus Duration")
        self.total_focus_duration_stat = QLabel("0")
        self.total_focus_duration_h3 = QLabel("Hours")
        self.total_focus_duration_layout.addStretch(1)
        self.total_focus_duration_layout.addWidget(self.total_focus_duration_h1, alignment=Qt.AlignHCenter)
        self.total_focus_duration_layout.addWidget(self.total_focus_duration_h2, alignment=Qt.AlignHCenter)
        self.total_focus_duration_layout.addWidget(self.total_focus_duration_stat, alignment=Qt.AlignHCenter)
        self.total_focus_duration_layout.addWidget(self.total_focus_duration_h3, alignment=Qt.AlignHCenter)
        self.total_focus_duration_layout.addStretch(1)

        self.longest_focus_streak = QWidget(parent=self.foocus_monster_widget)
        self.longest_focus_streak_layout = QVBoxLayout(self.longest_focus_streak)
        self.longest_focus_streak_h1 = QLabel("Longest")
        self.longest_focus_streak_h2 = QLabel("Focus Streak")
        self.longest_focus_streak_stat = QLabel("0")
        self.longest_focus_streak_h3 = QLabel("Minutes")
        self.longest_focus_streak_layout.addStretch(1)
        self.longest_focus_streak_layout.addWidget(self.longest_focus_streak_h1, alignment=Qt.AlignHCenter)
        self.longest_focus_streak_layout.addWidget(self.longest_focus_streak_h2, alignment=Qt.AlignHCenter)
        self.longest_focus_streak_layout.addWidget(self.longest_focus_streak_stat, alignment=Qt.AlignHCenter)
        self.longest_focus_streak_layout.addWidget(self.longest_focus_streak_h3, alignment=Qt.AlignHCenter)
        self.longest_focus_streak_layout.addStretch(1)

        self.btn_widget = QWidget()
        self.btn_widget_layout = QVBoxLayout(self.btn_widget)
        self.focus_now_btn = QPushButton("Focus Now")
        self.focus_now_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_widget_layout.addWidget(self.focus_now_btn)

        self.foocus_eyes.setGeometry(270, 60, 750, 300)
        self.foocus_mouth.setGeometry(0, 400, 1500, 200)
        self.total_focus_duration.setGeometry(370, 400, 250, 250)
        self.longest_focus_streak.setGeometry(670, 400, 250, 250)

        self.foocus_monster_widget.setObjectName("foocus_monster")
        self.foocus_eyes.setObjectName("foocus_eyes")
        self.foocus_mouth.setObjectName("foocus_mouth")

        self.total_focus_duration.setObjectName("total_focus_duration")
        self.total_focus_duration_h1.setObjectName("total_focus_duration_h1")
        self.total_focus_duration_h2.setObjectName("total_focus_duration_h2")
        self.total_focus_duration_stat.setObjectName("total_focus_duration_stat")
        self.total_focus_duration_h3.setObjectName("total_focus_duration_h3")
        self.longest_focus_streak.setObjectName("longest_focus_streak")
        self.longest_focus_streak_h1.setObjectName("longest_focus_streak_h1")
        self.longest_focus_streak_h2.setObjectName("longest_focus_streak_h2")
        self.longest_focus_streak_stat.setObjectName("longest_focus_streak_stat")
        self.longest_focus_streak_h3.setObjectName("longest_focus_streak_h3")

        self.btn_widget.setObjectName("btn_widget")
        self.focus_now_btn.setObjectName("focus_now_btn")

        self.btn_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_widget_layout.setSpacing(0)

        self.layout.addWidget(self.foocus_monster_widget)
        self.layout.addWidget(self.btn_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)



        