from PySide6.QtCore import QObject

from models.login_session import LoginSession
from views.main_window import MainWindow

class MainWindowController(QObject):
    def __init__(self):
        super().__init__()

        self.main_window = MainWindow()
        self.visited_content_pages = []

        # Connect buttons
        self.main_window.sidebar.page_selected.connect(self.switch_page)
        self.main_window.log_in_page.page_selected.connect(self.switch_page)
        self.main_window.sign_in_page.page_selected.connect(self.switch_page)
        self.main_window.home_page.page_selected.connect(self.switch_page)
        self.main_window.focus_zone_page.view.attention_detector.page_selected.connect(self.switch_page)
        self.main_window.mind_energizer_page.page_selected.connect(self.switch_page)
        self.main_window.mindfulness_activity_selection_page.page_selected.connect(self.switch_page)
        self.main_window.mindfulness_activity_1_page.page_selected.connect(self.switch_page)
        self.main_window.mindfulness_activity_2_page.page_selected.connect(self.switch_page)
        self.main_window.mindfulness_activity_3_page.page_selected.connect(self.switch_page)
        self.main_window.physical_exercise_1_page.page_selected.connect(self.switch_page)
        self.main_window.physical_exercise_2_page.page_selected.connect(self.switch_page)
        self.main_window.physical_exercise_3_page.page_selected.connect(self.switch_page)
        self.main_window.physical_exercise_selection_page.page_selected.connect(self.switch_page)
        self.main_window.rest_page.page_selected.connect(self.switch_page)

        self.main_window.focus_zone_page.view.attention_detector.is_notification_start.connect(self.bring_window_to_front)
        self.main_window.rest_page.is_notification.connect(self.bring_window_to_front)
        self.main_window.physical_exercise_1_page.is_notification.connect(self.bring_window_to_front)
        self.main_window.physical_exercise_2_page.is_notification.connect(self.bring_window_to_front)
        self.main_window.physical_exercise_3_page.is_notification.connect(self.bring_window_to_front)

    def run(self):
        self.main_window.showMaximized()

    def switch_app_page(self, app_page_name):
        app_page = self.main_window.app_pages.get(app_page_name)
        if app_page:
            match (app_page_name):
                case "main":
                    login_session = LoginSession()
                    username = login_session.get_username()
                    self.main_window.home_page.load_home_page()
                    self.main_window.sidebar.view.user_profile_btn.setText(username)
                case "log_in":
                    login_session = LoginSession()
                    login_session.clear_user()
                    self.visited_content_pages = []
                case "sign_in":
                    login_session = LoginSession()
                    login_session.clear_user()
                    self.visited_content_pages = []
                    
            self.main_window.app_pages_stack.setCurrentWidget(app_page)

    def switch_content_page(self, content_page_name):
        content_page = self.main_window.content_pages.get(content_page_name)
        if content_page:
            self.visited_content_pages.append(content_page_name)
            match (content_page_name):
                case "home":
                    self.main_window.home_page.load_home_page()
                case "insights":
                    self.main_window.insights_page.load_insights()
                case "leaderboard":
                    self.main_window.leaderboard_page.load_leaderboard()
            self.main_window.content_pages_stack.setCurrentWidget(content_page)
    
    def switch_page(self, page_name):
        if page_name == "back":
            self.visited_content_pages.pop()
            self.switch_content_page(self.visited_content_pages[-1])
        elif self.main_window.app_pages.get(page_name):
            self.switch_app_page(page_name)
        elif self.main_window.content_pages.get(page_name):
            self.switch_content_page(page_name)

    def bring_window_to_front(self):
        self.main_window.showMaximized()  
        self.main_window.raise_()      # Bring window to front
        self.main_window.activateWindow()  # Give focus
