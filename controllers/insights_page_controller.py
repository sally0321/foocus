from PySide6.QtCore import QObject

from models.login_session import LoginSession
from views.insights_page import InsightsPage
from utils.sessiondb_utils import *

class InsightsPageController(QObject):
    def __init__(self):
        super().__init__()

        # Initialize the insights page view
        self.view = InsightsPage()

    def load_insights(self):
        """Load the insights data and update the view."""

        # Get the current user's information from the previously created login session singleton
        login_session = LoginSession()
        user_id = login_session.get_user_id()

        # Fetch the latest statistics for the user from the local SQLite database
        latest_attention_spans = get_recent_attention_spans(user_id, 5)
        average_attention_span = get_avg_attention_span(user_id)
        longest_attention_span = get_longest_attention_span(user_id)
        highest_unfocus_frequency = get_highest_unfocus_frequency(user_id)
        lowest_unfocus_frequency = get_lowest_unfocus_frequency(user_id)

        # Update the view with the statistics
        self.view.avg_attention_span_stat.setText(str(round(average_attention_span / 60, 1)))
        self.view.longest_attention_span_stat.setText(str(round(longest_attention_span / 60, 1)))
        self.view.unfocus_frequency_highest_stat.setText(str(highest_unfocus_frequency))
        self.view.unfocus_frequency_lowest_stat.setText(str(lowest_unfocus_frequency))

        # Extract and format the timestampss and latest attention spans for the history plot
        timestamps = [datetime.fromisoformat(ts).strftime("%Y-%m-%d\n%H:%M") for ts, _ in latest_attention_spans]
        timestamps.reverse() # Reverse the order to follow the chronological order
        attention_spans = [round(attention_span / 60, 1) for _, attention_span in latest_attention_spans]
        attention_spans.reverse() # Reverse the order to follow the chronological order
        
        # Update the attention span history plot
        self.view.attention_span_history_ax.clear()
        self.view.attention_span_history_ax.set_title("Focus History")
        self.view.attention_span_history_ax.set_xlabel("Study Sessions")
        self.view.attention_span_history_ax.set_ylabel("Attention Span (minutes)")
        if not attention_spans:
            # Display a message in the center of the plot
            self.view.attention_span_history_ax.text(
                0.5, 0.5, "No data available yet",
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.view.attention_span_history_ax.transAxes,
                fontsize=12,
                color='gray'
            )

            # Hide the x and y ticks
            self.view.attention_span_history_ax.set_xticks([])  
            self.view.attention_span_history_ax.set_yticks([])  
        else:
            # Plot the attention spans with timestamps
            self.view.attention_span_history_ax.plot(timestamps, attention_spans, color='#04bfbf', marker='.')
        
        self.view.attention_span_history_canvas.draw()