from PySide6.QtCore import QObject, Signal

from views.leaderboard_page import LeaderboardPage

class LeaderboardPageController(QObject):
    def __init__(self):
        super().__init__()

        self.view = LeaderboardPage()
    
    
        