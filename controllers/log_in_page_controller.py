from PySide6.QtCore import QObject, Signal

from views.log_in_page import LogInPage
from utils.userdb_utils import login_user
from models.login_session import LoginSession

class LogInPageController(QObject):
    page_selected = Signal(str)
    log_in_attempt = Signal(str, str)

    def __init__(self):
        super().__init__()

        self.view = LogInPage()

        self.view.log_in_btn.clicked.connect(lambda: self.log_in_attempt.emit(self.view.username_input.text(), self.view.password_input.text()))
        self.view.create_acc_btn.clicked.connect(lambda: self.page_selected.emit("sign_in"))

        self.log_in_attempt.connect(self.handle_log_in)

    def show_error_message(self, message):
        self.view.error_message_label.setText(message)

    def handle_log_in(self, username, password):
        if not (username and password):
            self.show_error_message("Username and password field cannot be empty.")
            return
        
        user_login_result = login_user(username, password)
        status = user_login_result['status']

        if status != "success":
            self.show_error_message(user_login_result['message'])
            return
        
        user_id = user_login_result['user_id']
        login_session = LoginSession()
        login_session.set_user(user_id, username)
        
        self.page_selected.emit("main")
        
            