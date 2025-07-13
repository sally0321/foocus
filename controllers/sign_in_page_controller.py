from PySide6.QtCore import QObject, Signal

from views.sign_in_page import SignInPage
from utils.userdb_utils import register_user
from models.login_session import LoginSession

class SignInPageController(QObject):
    page_selected = Signal(str) # Signal to notify the main window controller about page changes
    sign_in_attempt = Signal(str, str, str) # Signal to handle sign-in attempts with username, password, and password confirmation
    
    def __init__(self):
        super().__init__()

        # Initialize the sign-in page view
        self.view = SignInPage()

        # Connect the button events to the methods
        self.view.sign_in_btn.clicked.connect(lambda: self.sign_in_attempt.emit(self.view.username_input.text(), self.view.password_input.text(), self.view.password_confirmation_input.text()))
        self.view.back_to_log_in_btn.clicked.connect(lambda: self.page_selected.emit("log_in"))

        # Connect the signal to the method
        self.sign_in_attempt.connect(self.handle_sign_in)

    def show_error_message(self, message):
        """Display an error message on the sign-in page."""

        self.view.error_message_label.setText(message)

    def handle_sign_in(self, username, password, password_confirmation):
        """Handle the sign-in attempt by validating inputs and registering the user."""

        # Validate inputs
        if not (username and password and password_confirmation):
            self.show_error_message("Username, password and password confirmation fields cannot be empty.")
            return
        if password != password_confirmation:
            self.show_error_message("Password and password confirmation must be the same.")
            return
        
        # Register the user in the userdb
        user_registration_result = register_user(username, password)
        status = user_registration_result['status']

        if status != "success":
            self.show_error_message(user_registration_result['message'])
            return

        user_id = user_registration_result['user_id']

        # Create a new loginin session singleton and set the user
        login_session = LoginSession()
        login_session.set_user(user_id, username)
        
        # Emit the signal to switch to the main page
        self.page_selected.emit("main")

        # Clear the input fields after successful sign-in
        self.view.username_input.clear()
        self.view.password_input.clear()
        self.view.password_confirmation_input.clear()        

