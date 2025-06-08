from sys import builtin_module_names
from turtle import color
from PySide6.QtCore import QObject

from models.login_session import LoginSession
from views.insights_page import InsightsPage
from utils.sessiondb_utils import *

class InsightsPageController(QObject):
    def __init__(self):
        super().__init__()

        self.view = InsightsPage()

    def load_insights(self):
        login_session = LoginSession()
        user_id = login_session.get_user_id()

        latest_attention_spans = get_attention_spans(user_id, 5)
        average_attention_span = get_avg_attention_span(user_id)
        longest_attention_span = get_longest_attention_span(user_id)
        highest_unfocus_frequency = get_highest_unfocus_frequency(user_id)
        lowest_unfocus_frequency = get_lowest_unfocus_frequency(user_id)

        self.view.avg_attention_span_stat.setText(str(round(average_attention_span / 60, 1)))
        self.view.longest_attention_span_stat.setText(str(round(longest_attention_span / 60, 1)))
        self.view.unfocus_frequency_highest_stat.setText(str(highest_unfocus_frequency))
        self.view.unfocus_frequency_lowest_stat.setText(str(lowest_unfocus_frequency))

        timestamps = [datetime.fromisoformat(ts).strftime("%Y-%m-%d\n%H:%M") for ts, _ in latest_attention_spans]
        timestamps.reverse()
        attention_spans = [round(span / 60, 1) for _, span in latest_attention_spans]
        attention_spans.reverse()
        self.view.attention_span_history_ax.plot(timestamps, attention_spans, color='#04bfbf')
        # self.view.attention_span_history_figure.set_alpha(0.0) 
        # self.view.attention_span_history_ax.set_alpha(0.0)


