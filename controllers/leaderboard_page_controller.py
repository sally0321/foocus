from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
from requests.exceptions import ConnectionError

from models.login_session import LoginSession
from views.leaderboard_page import LeaderboardPage
from utils.cloud_sessiondb_utils import get_weekly_top5_attention_span

class LeaderboardPageController(QObject):
    def __init__(self):
        super().__init__()

        self.view = LeaderboardPage()

    def load_leaderboard(self):
        self.view.subtitle_label.setText("") 

        try: 
            get_weekly_top5_attention_span_response = get_weekly_top5_attention_span()
            if get_weekly_top5_attention_span_response['status'] != "success":
                raise Exception
        except ConnectionError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Connection Error")
            msg.setText("You're currently offline, so the leaderboard couldn't be loaded. Please check your internet connection and try again.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Unexpected Error")
            msg.setText("Uh oh, an unexpected error occurs. Please refresh the page again.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            print(e)
            return
        
        data = get_weekly_top5_attention_span_response['data']

        start_date = data['week_period']['start']
        end_date = data['week_period']['end']
        top5_user_data = data['top5_users'] 

        self.view.subtitle_label.setText(f"Week {start_date} to {end_date}") 

        login_session = LoginSession()
        current_user_id = login_session.get_user_id()
        current_username = login_session.get_username()

        for i in range(5):
            user_data = top5_user_data[i] if i < len(top5_user_data) else {}
            username = user_data.get('username', 'Awaiting legend...')
            user_id = user_data.get('user_id', '')
            avg_attention_span = user_data.get('avg_attention_span', 0)

            if user_id == current_user_id:
                username = f"{username} (You)"

            if avg_attention_span == 0:
                formatted_avg_attention_span = ""
            elif avg_attention_span < 60:
                formatted_avg_attention_span = f"{avg_attention_span} seconds"
            elif avg_attention_span < 3600:
                formatted_avg_attention_span = f"{round(avg_attention_span / 60, 1)} minutes"
            else:
                formatted_avg_attention_span = f"{round(avg_attention_span / 3600, 1)} hours"
            
            self.view.user_labels[i].setText(username)
            self.view.attention_span_labels[i].setText(formatted_avg_attention_span)
            

            
           
    
        