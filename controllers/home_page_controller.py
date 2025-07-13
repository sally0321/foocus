from PySide6.QtCore import QObject, Signal

from models.login_session import LoginSession
from utils.sessiondb_utils import get_longest_attention_span, get_total_focus_duration
from views.home_page import HomePage

class HomePageController(QObject):
    page_selected = Signal(str) # Signal to notify the main window controller about page changes

    def __init__(self):
        super().__init__()

        # initialize the home page view
        self.view = HomePage()

        # connect the button events to the methods
        self.view.focus_now_btn.clicked.connect(lambda: self.page_selected.emit("focus_zone"))

    def load_home_page(self):
        """Load the home page data and update the view."""

        # Get the current user's information from the previously created login session singleton
        login_session = LoginSession()
        user_id = login_session.get_user_id()

        # Fetch the total focus duration and longest attention span for the user from the local SQLite database
        total_attention_span = get_total_focus_duration(user_id)
        longest_attention_span = get_longest_attention_span(user_id)

        # Update the view with the statistics
        if total_attention_span / 3600 > 1:
            total_focus_duration_in_hours = round(total_attention_span / 3600, 1)
            self.view.total_focus_duration_stat.setText(str(total_focus_duration_in_hours))
            self.view.total_focus_duration_h3.setText("Hours")
        else:
            total_focus_duration_in_minutes = round(total_attention_span / 60, 1)
            self.view.total_focus_duration_stat.setText(str(total_focus_duration_in_minutes))
            self.view.total_focus_duration_h3.setText("Minutes")

        longest_attention_span_in_minutes = round(longest_attention_span / 60, 1)
        self.view.longest_focus_streak_stat.setText(str(longest_attention_span_in_minutes))
        
