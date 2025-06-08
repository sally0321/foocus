from PySide6.QtCore import QObject

from views.main_window import MainWindow

class MainWindowController(QObject):
    def __init__(self):
        super().__init__()

        self.main_window = MainWindow()

        # Connect buttons
        self.main_window.sidebar.page_selected.connect(self.switch_content_page)
        self.main_window.log_in_page.page_selected.connect(self.switch_app_page)
        self.main_window.sign_in_page.page_selected.connect(self.switch_app_page)

        self.main_window.home_page.page_selected.connect(self.switch_content_page)
        self.main_window.mind_energizer_page.page_selected.connect(self.switch_content_page)
        self.main_window.mindfulness_activity_selection_page.page_selected.connect(self.switch_content_page)
        self.main_window.physical_exercise_selection_page.page_selected.connect(self.switch_content_page)

        self.main_window.focus_zone_page.view.attention_detector.is_notification.connect(self.bring_window_to_front)
        self.main_window.focus_zone_page.view.attention_detector.page_selected.connect(self.switch_content_page)

        self.main_window.rest_page.is_notification.connect(self.bring_window_to_front)

    def run(self):
        self.main_window.showMaximized()

    def switch_app_page(self, app_page_name):
        app_page = self.main_window.app_pages.get(app_page_name)
        if app_page:
            match (app_page_name):
                case "main":
                    self.main_window.home_page.load_home_page()
            self.main_window.app_pages_stack.setCurrentWidget(app_page)

    def switch_content_page(self, content_page_name):
        content_page = self.main_window.content_pages.get(content_page_name)
        if content_page:
            match (content_page_name):
                case "home":
                    self.main_window.home_page.load_home_page()
                case "insights":
                    self.main_window.insights_page.load_insights()
            self.main_window.content_pages_stack.setCurrentWidget(content_page)

    def bring_window_to_front(self):
        self.main_window.showMaximized()  
        self.main_window.raise_()      # Bring window to front
        self.main_window.activateWindow()  # Give focus