from PySide6.QtCore import QObject, Signal

from views.log_in_page import LogInPage
from utils.userdb_utils import login_user
from models.login_session import LoginSession

class LogInPageController(QObject):
    page_selected = Signal(str) # Signal to notify the main window controller about page changes
    log_in_attempt = Signal(str, str) # Signal to handle log-in attempts with username and password

    def __init__(self):
        super().__init__()

        # Initialize the log-in page view
        self.view = LogInPage()

        # Connect the button events to the methods
        self.view.log_in_btn.clicked.connect(lambda: self.log_in_attempt.emit(self.view.username_input.text(), self.view.password_input.text()))
        self.view.create_acc_btn.clicked.connect(lambda: self.page_selected.emit("sign_in"))

        # Connect the signal to the method
        self.log_in_attempt.connect(self.handle_log_in)

    def show_error_message(self, message):
        """Display an error message on the log-in page."""

        self.view.error_message_label.setText(message)

    def handle_log_in(self, username, password):
        """Handle the log-in attempt with the provided username and password."""

        # Validate the input fields
        if not (username and password):
            self.show_error_message("Username and password field cannot be empty.")
            return
        
        # Retrieve the user from the userdb and check credentials
        user_login_result = login_user(username, password)
        status = user_login_result['status']

        if status != "success":
            self.show_error_message(user_login_result['message'])
            return
        
        user_id = user_login_result['user_id']

        # Create a new login session singleton and set the user
        login_session = LoginSession()
        login_session.set_user(user_id, username)
        
        # Emit the signal to switch to the main page
        self.page_selected.emit("main")

        # Clear the input fields after successful log-in
        self.view.username_input.clear()
        self.view.password_input.clear()
        
            