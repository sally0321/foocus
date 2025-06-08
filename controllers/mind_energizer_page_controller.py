from PySide6.QtCore import QObject, Signal

from views.mind_energizer_page import MindEnergizerPage

class MindEnergizerPageController(QObject):
    page_selected = Signal(str)
    
    def __init__(self):
        super().__init__()

        self.view = MindEnergizerPage()

        self.view.mindfulness_activity_btn.clicked.connect(lambda: self.page_selected.emit("mindfulness_activity_selection"))
        self.view.physical_activity_btn.clicked.connect(lambda: self.page_selected.emit("physical_exercise_selection"))
        self.view.rest_btn.clicked.connect(lambda: self.page_selected.emit("rest"))

