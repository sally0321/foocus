from PySide6.QtCore import QObject, Signal

from models.login_session import LoginSession
from utils.sessiondb_utils import get_longest_attention_span, get_total_attention_span
from views.home_page import HomePage

class HomePageController(QObject):
    page_selected = Signal(str)

    def __init__(self):
        super().__init__()

        self.view = HomePage()

        self.view.focus_now_btn.clicked.connect(lambda: self.page_selected.emit("focus_zone"))

    def load_home_page(self):
        login_session = LoginSession()
        user_id = login_session.get_user_id()

        total_attention_span = get_total_attention_span(user_id)

        if total_attention_span / 360 > 1:
            total_attention_span_in_hours = round(total_attention_span / 360, 1)
            self.view.total_focus_duration_stat.setText(str(total_attention_span_in_hours))
            self.view.total_focus_duration_h3.setText("Hours")
        else:
            total_attention_span_in_minutes = round(total_attention_span / 60, 1)
            self.view.total_focus_duration_stat.setText(str(total_attention_span_in_minutes))
            self.view.total_focus_duration_h3.setText("Minutes")

        longest_attention_span = get_longest_attention_span(user_id)
        longest_attention_span_in_minutes = round(longest_attention_span / 60, 1)
        self.view.longest_focus_streak_stat.setText(str(longest_attention_span_in_minutes))
        
