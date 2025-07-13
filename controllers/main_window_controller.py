from PySide6.QtCore import QObject

from models.login_session import LoginSession
from views.main_window import MainWindow

class MainWindowController(QObject):
    def __init__(self):
        super().__init__()

        # Initialize the main window view
        self.main_window = MainWindow()

        # Store a list of visited page for page nagivation during undo (back)
        self.visited_content_pages = []

        # Connect the page_selected signals to the switch_page method for switching pages
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

        # Connect the is_notification signal to the bring_window_to_front method for displaying the window on top of all other running apps
        self.main_window.focus_zone_page.view.attention_detector.is_notification_start.connect(self.bring_window_to_front)
        self.main_window.rest_page.is_notification.connect(self.bring_window_to_front)
        self.main_window.physical_exercise_1_page.is_notification.connect(self.bring_window_to_front)
        self.main_window.physical_exercise_2_page.is_notification.connect(self.bring_window_to_front)
        self.main_window.physical_exercise_3_page.is_notification.connect(self.bring_window_to_front)

    def run(self):
        """Show the main window."""

        self.main_window.showMaximized()

    def switch_app_page(self, app_page_name):
        """Switch the app-level pages."""

        app_page = self.main_window.app_pages.get(app_page_name)
        if app_page:
            match (app_page_name):
                case "main":
                    # Display the main content
                    # Get the current user's information through the previously created login session singleton
                    login_session = LoginSession()
                    username = login_session.get_username()
                    # Reload home page with the latest user statistics
                    self.main_window.home_page.load_home_page()
                    # Set the username to show the logged in user session
                    self.main_window.sidebar.view.user_profile_btn.setText(username)
                case "log_in":
                    # Display the login page
                    # Clear the user's information in the previously created login session singleton
                    login_session = LoginSession()
                    login_session.clear_user()
                    # Reset the visited content pages records
                    self.visited_content_pages = []
                case "sign_in":
                    # Display the signin page
                    ## Clear the user's information in the previously created login session singleton
                    login_session = LoginSession()
                    login_session.clear_user()
                    # Reset the visited content pages records
                    self.visited_content_pages = []
                    
            # Switch to the selected app page in the stacked widget
            self.main_window.app_pages_stack.setCurrentWidget(app_page)

    def switch_content_page(self, content_page_name):
        """Switch the content-level pages."""

        content_page = self.main_window.content_pages.get(content_page_name)
        if content_page:
            # Save page navigation history
            self.visited_content_pages.append(content_page_name)
            
            match (content_page_name):
                case "home":
                    # Reload the home page for the latest user statistics before displaying
                    self.main_window.home_page.load_home_page()
                case "insights":
                    # Reload the insights page for the latest user statistics before displaying
                    self.main_window.insights_page.load_insights()
                case "leaderboard":
                    # Reload the leaderboard page for the latest user statistics before displaying
                    self.main_window.leaderboard_page.load_leaderboard()
            
            # Switch to the selected content page in the stacked widget
            self.main_window.content_pages_stack.setCurrentWidget(content_page)
    
    def switch_page(self, page_name):
        """Switch between app-level and content-level pages and handle back navigation"""

        if page_name == "back":
            # Remove the current page from history
            self.visited_content_pages.pop()
            # Switch to the previous one
            self.switch_content_page(self.visited_content_pages[-1])
        elif self.main_window.app_pages.get(page_name):
            self.switch_app_page(page_name)
        elif self.main_window.content_pages.get(page_name):
            self.switch_content_page(page_name)

    def bring_window_to_front(self):
        """Brings the main window to the front of all other running apps and gives it focus."""

        self.main_window.showMaximized()  
        self.main_window.raise_()      # Bring window to front
        self.main_window.activateWindow()  # Give focus
