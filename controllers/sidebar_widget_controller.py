from PySide6.QtCore import QObject, Signal

from views.sidebar_widget import SidebarWidget

class SidebarController(QObject):
    page_selected = Signal(str)

    def __init__(self):
        super().__init__()

        self.view = SidebarWidget()

        self.view.home_page_btn.clicked.connect(lambda: self.page_selected.emit("home"))
        self.view.focus_zone_page_btn.clicked.connect(lambda: self.page_selected.emit("focus_zone"))
        self.view.mind_energizer_page_btn.clicked.connect(lambda: self.page_selected.emit("mind_energizer"))
        self.view.insights_page_btn.clicked.connect(lambda: self.page_selected.emit("insights"))
        self.view.leaderboard_page_btn.clicked.connect(lambda: self.page_selected.emit("leaderboard"))
        self.view.logout_btn.clicked.connect(lambda: self.page_selected.emit("log_in"))
