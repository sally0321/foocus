from PySide6.QtCore import QObject, Signal

from views.mind_energizer_page import MindEnergizerPage

class MindEnergizerPageController(QObject):
    page_selected = Signal(str) # Signal to notify the main window controller about page changes
    
    def __init__(self):
        super().__init__()

        # Initialize the mind energizer page view
        self.view = MindEnergizerPage()

        # Connect the button click events to emit the page selection signal for switching pages
        self.view.mindfulness_activity_btn.clicked.connect(lambda: self.page_selected.emit("mindfulness_activity_selection"))
        self.view.physical_activity_btn.clicked.connect(lambda: self.page_selected.emit("physical_exercise_selection"))
        self.view.rest_btn.clicked.connect(lambda: self.page_selected.emit("rest"))

