from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt

class LeaderboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.page_title_label = QLabel("Meet the Attention Span Legends!", alignment=Qt.AlignCenter)
        self.page_title_label.setObjectName("leaderboard_page_title")

        self.week_period_label = QLabel("", alignment=Qt.AlignCenter)
        self.week_period_label.setObjectName("week_period_label")

        self.leaderboard = QWidget()
        self.leaderboard_layout = QGridLayout(self.leaderboard)

        # Create the leaderboard column title labels
        self.rank_column_label = QLabel("Rank", alignment=Qt.AlignCenter)
        self.user_column_label = QLabel("User", alignment=Qt.AlignCenter)
        self.attention_span_column_label = QLabel("Average Attention Span", alignment=Qt.AlignCenter)
        self.rank_column_label.setProperty("role", "leaderboard_column_title")
        self.user_column_label.setProperty("role", "leaderboard_column_title")
        self.attention_span_column_label.setProperty("role", "leaderboard_column_title")

        # Create the labels for the row top 1
        self.first_rank_label = QLabel(alignment=Qt.AlignCenter)
        self.first_user_label = QLabel("Awaiting Legend...", alignment=Qt.AlignCenter)
        self.first_attention_span_label = QLabel(alignment=Qt.AlignCenter)
        self.first_rank_label.setObjectName("first_rank_label")
        self.first_user_label.setProperty("role", "top3_user_label")
        self.first_attention_span_label.setProperty("role", "top3_attention_span_label")

        # Create the labels for the row top 2
        self.second_rank_label = QLabel(alignment=Qt.AlignCenter)
        self.second_user_label = QLabel("Awaiting Legend...", alignment=Qt.AlignCenter)
        self.second_attention_span_label = QLabel(alignment=Qt.AlignCenter)
        self.second_rank_label.setObjectName("second_rank_label")
        self.second_user_label.setProperty("role", "top3_user_label")
        self.second_attention_span_label.setProperty("role", "top3_attention_span_label")

        # Create the labels for the row top 3
        self.third_rank_label = QLabel(alignment=Qt.AlignCenter)
        self.third_user_label = QLabel("Awaiting Legend...", alignment=Qt.AlignCenter)
        self.third_attention_span_label = QLabel(alignment=Qt.AlignCenter)
        self.third_rank_label.setObjectName("third_rank_label")
        self.third_user_label.setProperty("role", "top3_user_label")
        self.third_attention_span_label.setProperty("role", "top3_attention_span_label")

        # Create the labels for the row top 4
        self.fourth_rank_label = QLabel("4", alignment=Qt.AlignCenter)
        self.fourth_user_label = QLabel("Awaiting Legend...", alignment=Qt.AlignCenter)
        self.fourth_attention_span_label = QLabel(alignment=Qt.AlignCenter)
        self.fourth_rank_label.setProperty("role", "rank_num_label")
        self.fourth_user_label.setProperty("role", "user_label")
        self.fourth_attention_span_label.setProperty("role", "attention_span_label")

        # Create the labels for the row top 5
        self.fifth_rank_label = QLabel("5", alignment=Qt.AlignCenter)
        self.fifth_user_label = QLabel("Awaiting Legend...", alignment=Qt.AlignCenter)
        self.fifth_attention_span_label = QLabel(alignment=Qt.AlignCenter)
        self.fifth_rank_label.setProperty("role", "rank_num_label")
        self.fifth_user_label.setProperty("role", "user_label")
        self.fifth_attention_span_label.setProperty("role", "attention_span_label")

        self.user_labels = [self.first_user_label, self.second_user_label, self.third_user_label, self.fourth_user_label, self.fifth_user_label]
        self.attention_span_labels = [self.first_attention_span_label, self.second_attention_span_label, self.third_attention_span_label, self.fourth_attention_span_label, self.fifth_attention_span_label]

        # Create a spacing label to format the leaderboard by creating space between rank and user columns
        spacing_label = QLabel()
        spacing_label.setObjectName("leaderboard_spacing_label")

        self.leaderboard_layout.addWidget(self.rank_column_label, 0, 0, 1, 1)
        self.leaderboard_layout.addWidget(spacing_label, 0, 1, 1, 1)  
        self.leaderboard_layout.addWidget(self.user_column_label, 0, 2, 1, 1)
        self.leaderboard_layout.addWidget(self.attention_span_column_label, 0, 3, 1, 1)

        self.leaderboard_layout.addWidget(self.first_rank_label, 1, 0, 1, 1)
        self.leaderboard_layout.addWidget(self.first_user_label, 1, 2, 1, 1)
        self.leaderboard_layout.addWidget(self.first_attention_span_label, 1, 3, 1, 1)

        self.leaderboard_layout.addWidget(self.second_rank_label, 2, 0, 1, 1)
        self.leaderboard_layout.addWidget(self.second_user_label, 2, 2, 1, 1)
        self.leaderboard_layout.addWidget(self.second_attention_span_label, 2, 3, 1, 1)

        self.leaderboard_layout.addWidget(self.third_rank_label, 3, 0, 1, 1)
        self.leaderboard_layout.addWidget(self.third_user_label, 3, 2, 1, 1)
        self.leaderboard_layout.addWidget(self.third_attention_span_label, 3, 3, 1, 1)

        self.leaderboard_layout.addWidget(self.fourth_rank_label, 4, 0, 1, 1)
        self.leaderboard_layout.addWidget(self.fourth_user_label, 4, 2, 1, 1)
        self.leaderboard_layout.addWidget(self.fourth_attention_span_label, 4, 3, 1, 1)

        self.leaderboard_layout.addWidget(self.fifth_rank_label, 5, 0, 1, 1)
        self.leaderboard_layout.addWidget(self.fifth_user_label, 5, 2, 1, 1)
        self.leaderboard_layout.addWidget(self.fifth_attention_span_label, 5, 3, 1, 1)

        self.leaderboard_layout.setHorizontalSpacing(0)

        self.layout.addWidget(self.page_title_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.week_period_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.leaderboard, alignment=Qt.AlignHCenter)
        self.layout.addStretch(1)
