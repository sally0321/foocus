from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget

from controllers.activity_page_controller import ActivityPageController
from controllers.activity_selection_page_controller import ActivitySelectionPageController
from controllers.home_page_controller import HomePageController
from controllers.leaderboard_page_controller import LeaderboardPageController
from controllers.mind_energizer_page_controller import MindEnergizerPageController
from controllers.rest_page_controller import RestPageController
from controllers.sidebar_widget_controller import SidebarController
from controllers.log_in_page_controller import LogInPageController
from controllers.sign_in_page_controller import SignInPageController
from controllers.focus_zone_page_controller import FocusZonePageController
from controllers.insights_page_controller import InsightsPageController
from models.data import ActivityPageConfig

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  
        
        # Stack for switching between main app pages (login, sign in, main content)
        self.app_pages_stack = QStackedWidget()
        
        # Widget and layout for the main content area (sidebar + content pages stack)
        self.content_area_widget = QWidget()
        self.content_area_widget_layout = QHBoxLayout(self.content_area_widget)
        
        # Stack for switching between content pages (home, focus zone, insights, etc.)
        self.content_pages_stack = QStackedWidget()

        # Initialize controllers for all pages and sidebar
        self.sidebar = SidebarController()
        self.log_in_page = LogInPageController()
        self.sign_in_page = SignInPageController()
        self.home_page = HomePageController()
        self.focus_zone_page = FocusZonePageController()
        self.insights_page = InsightsPageController()
        self.mind_energizer_page = MindEnergizerPageController()
        self.rest_page = RestPageController()
        self.leaderboard_page = LeaderboardPageController()
        
        # Create configs for mindfulness activities
        mindfulness_activity_1_page_config = ActivityPageConfig(page_title="The Wheel of Awareness", description="Expand your focus by gently guiding your attention through different aspects of your experience.\nThis practice helps you strengthen your awareness by moving attention across your senses, thoughts, and feelings. It cultivates calmness, clarity, and mental flexibility — supporting you in regaining focus when distractions arise.", video_embed_link="https://www.youtube.com/embed/kZrjmPPvE7k?si=4Xhg2hxAkch6i5L5", timer_duration=0, page_name="mindfulness_activity_1")
        mindfulness_activity_2_page_config = ActivityPageConfig(page_title="Leaves on a Stream", description="Let go of thoughts by imagining them floating away on a gentle stream.\nThis exercise invites you to observe your thoughts without judgment. As each thought arises, place it on a leaf and watch it drift away. It promotes mental clarity and emotional distance from distractions, helping you return to a centered, focused state.", video_embed_link="https://www.youtube.com/embed/Ml-yuYraZkA?si=rfxn9jEaBtkWY5gG", timer_duration=0, page_name="mindfulness_activity_2")
        mindfulness_activity_3_page_config = ActivityPageConfig(page_title="Eye of the Hurricane", description="Find calm at the center of life’s storms, just like the stillness at the eye of a hurricane.\nThis guided activity encourages you to notice the chaos around you while anchoring yourself in an inner place of calm. It builds emotional resilience and focus, allowing you to stay grounded even when your mind feels scattered.", video_embed_link="https://www.youtube.com/embed/HPFayxlm_ms?si=Yy7yeFQYAUxBuV6T", timer_duration=0, page_name="mindfulness_activity_3")
        # Store configs in a list for selection page rendering
        self.mindfulness_activity_page_configs = [mindfulness_activity_1_page_config, mindfulness_activity_2_page_config, mindfulness_activity_3_page_config]
        
        # Create Controllers for mindfulness activity selection and individual activity pages
        self.mindfulness_activity_selection_page = ActivitySelectionPageController("Mindfulness Activity", self.mindfulness_activity_page_configs)
        self.mindfulness_activity_1_page = ActivityPageController(mindfulness_activity_1_page_config)
        self.mindfulness_activity_2_page = ActivityPageController(mindfulness_activity_2_page_config)
        self.mindfulness_activity_3_page = ActivityPageController(mindfulness_activity_3_page_config)

        # Create configs for physical exercise activities
        physical_exercise_1_page_config = ActivityPageConfig(page_title="High Knee Jog in Place", description="", video_embed_link="https://www.youtube.com/embed/IpnHwUwrVVY?si=lFJ1Ap-0PKZ9RcI0", timer_duration=30, page_name="physical_exercise_1")
        physical_exercise_2_page_config = ActivityPageConfig(page_title="Star Jump", description="", video_embed_link="https://www.youtube.com/embed/VVEO_J1tIXU?si=yI216dgsgMbnaIvG", timer_duration=300, page_name="physical_exercise_2")
        physical_exercise_3_page_config = ActivityPageConfig(page_title="Brisk Walking", description="", video_embed_link="https://www.youtube.com/embed/tVpUCkMLgms?si=x58F0AWgP2YyQDtF", timer_duration=300, page_name="physical_exercise_3")
        # Store configs in a list for selection page rendering
        self.physical_exercise_page_configs = [physical_exercise_1_page_config, physical_exercise_2_page_config, physical_exercise_3_page_config]
        
        # Create Controllers for physical exercise selection and individual activity pages
        self.physical_exercise_selection_page = ActivitySelectionPageController("Physical Exercise", self.physical_exercise_page_configs)
        self.physical_exercise_1_page = ActivityPageController(physical_exercise_1_page_config)
        self.physical_exercise_2_page = ActivityPageController(physical_exercise_2_page_config)
        self.physical_exercise_3_page = ActivityPageController(physical_exercise_3_page_config)

        # Mapping app-level page name to their views
        self.app_pages = {
            "log_in": self.log_in_page.view,
            "sign_in": self.sign_in_page.view,
            "main": self.content_area_widget
        }

        # Mapping content-level page name to their views
        self.content_pages = {
            "home": self.home_page.view,
            "focus_zone": self.focus_zone_page.view,
            "insights": self.insights_page.view,
            "mind_energizer": self.mind_energizer_page.view,
            "mindfulness_activity_selection": self.mindfulness_activity_selection_page.view,
            mindfulness_activity_1_page_config.page_name: self.mindfulness_activity_1_page.view,
            mindfulness_activity_2_page_config.page_name: self.mindfulness_activity_2_page.view,
            mindfulness_activity_3_page_config.page_name: self.mindfulness_activity_3_page.view,
            "physical_exercise_selection": self.physical_exercise_selection_page.view,
            physical_exercise_1_page_config.page_name: self.physical_exercise_1_page.view,
            physical_exercise_2_page_config.page_name: self.physical_exercise_2_page.view,
            physical_exercise_3_page_config.page_name: self.physical_exercise_3_page.view,
            "rest": self.rest_page.view,
            "leaderboard": self.leaderboard_page.view
        }

        # Add the views of app-level pages to the app pages stack
        for app_pages in self.app_pages.values():
            self.app_pages_stack.addWidget(app_pages)

        # Add the views of content-level pages to the content pages stack
        for content_pages in self.content_pages.values():
            self.content_pages_stack.addWidget(content_pages)

        # Add sidebar and content pages stack to the main content area 
        self.content_area_widget_layout.addWidget(self.sidebar.view)
        self.content_area_widget_layout.addWidget(self.content_pages_stack)

        self.app_pages_stack.setContentsMargins(0, 0, 0, 0)
        self.content_pages_stack.setContentsMargins(0, 0, 0, 0)

        self.content_area_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area_widget_layout.setSpacing(0)
        
        self.setWindowTitle("Foocus.")
        self.setCentralWidget(self.app_pages_stack)
    
        


