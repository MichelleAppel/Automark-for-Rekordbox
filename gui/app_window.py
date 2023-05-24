from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QSettings

from .widgets import XMLLoadButton, PlaylistSelectionWidget, CollectionProcessCheckbox, MarksOverrideCheckbox, \
    RetainFirstTempoCheckbox, DropMarkerSelectionWidget, HotCuePointsWidget, MemoryCuePointsWidget, ProcessButton, \
    LogArea, PresetWidget

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rekordbox Auto Cue Points")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.central_widget = QWidget(self)

        # Widgets dictionary
        self.widgets = {}

        # Widget initialization
        self.load_button = XMLLoadButton(self.widgets)
        self.playlist_selection = PlaylistSelectionWidget(self.widgets)
        self.collection_process = CollectionProcessCheckbox(self.widgets)
        self.marks_override = MarksOverrideCheckbox()
        self.retain_first_tempo = RetainFirstTempoCheckbox()
        self.preset_widget = PresetWidget()
        self.drop_marker_selection = DropMarkerSelectionWidget()
        self.hot_cue_points = HotCuePointsWidget()
        self.memory_cue_points = MemoryCuePointsWidget()
        self.process_button = ProcessButton()
        self.log_area = LogArea()
        

        # Add widgets to the dictionary
        self.widgets['playlist_list'] = self.playlist_selection.playlist_list
        self.widgets['log_area'] = self.log_area

        # Setting up layout
        self.setup_layout()

        # Set window properties
        self.setWindowTitle("Rekordbox Auto Cue Points")
        self.setGeometry(100, 100, 800, 600)

    def setup_layout(self):
        self.main_layout = QVBoxLayout(self.central_widget)
        self.cue_points_layout = QHBoxLayout()

        # Add widgets to the layout
        self.main_layout.addWidget(self.load_button)
        self.main_layout.addWidget(self.preset_widget)
        
        self.main_layout.addWidget(self.playlist_selection)
        self.main_layout.addWidget(self.collection_process)
        self.main_layout.addWidget(self.marks_override)
        self.main_layout.addWidget(self.retain_first_tempo)


        self.main_layout.addWidget(self.drop_marker_selection)

        self.cue_points_layout.addWidget(self.hot_cue_points)
        self.cue_points_layout.addWidget(self.memory_cue_points)
        self.main_layout.addLayout(self.cue_points_layout)

        self.main_layout.addWidget(self.process_button)
        self.main_layout.addWidget(self.log_area)

        self.setCentralWidget(self.central_widget)

    def run(self):
        self.show()

    def closeEvent(self, event):
        settings = QSettings("Personal", "Default")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        QMainWindow.closeEvent(self, event)
