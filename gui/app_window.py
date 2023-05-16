from PyQt5.QtWidgets import QTableWidget, QHBoxLayout, QMainWindow, QTableWidgetItem, QPushButton, QListWidget, QCheckBox, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QComboBox, QLabel, QSpinBox
from PyQt5.QtCore import Qt, QSettings
from automark.automark import process_collection_xml
from automark.xml import RekordboxXml

from automark.cue_points import drop_mark_num, hot_cue_points, memory_cue_points, loop_cue_points, cue_points

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rekordbox Auto Cue Points")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and main layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)

        # Button to load XML
        self.load_button = QPushButton("Load XML")
        self.load_button.clicked.connect(self.load_xml)
        self.main_layout.addWidget(self.load_button)

        # Playlist selection
        self.playlist_list = QListWidget()
        self.playlist_list.setSelectionMode(QListWidget.MultiSelection)
        self.main_layout.addWidget(self.playlist_list)

        # Process entire collection
        self.process_all = QCheckBox("Process entire collection")
        self.main_layout.addWidget(self.process_all)

        # Remove existing marks
        self.remove_existing_marks = QCheckBox("Overwrite existing marks")
        self.remove_existing_marks.setChecked(True)
        self.main_layout.addWidget(self.remove_existing_marks)

        # Retain first tempo
        self.retain_first_tempo = QCheckBox("Retain first tempo")
        self.retain_first_tempo.setChecked(True)
        self.main_layout.addWidget(self.retain_first_tempo)

        # Drop marker selection
        self.drop_marker_label = QLabel("Drop marker:")
        self.main_layout.addWidget(self.drop_marker_label)
        self.drop_marker = QComboBox()
        self.drop_marker.addItem("Hot Cue A", 0)
        self.drop_marker.addItem("Hot Cue B", 1)
        self.drop_marker.addItem("Hot Cue C", 2)
        self.drop_marker.addItem("Hot Cue D", 3)
        self.drop_marker.addItem("Hot Cue E", 4)
        self.drop_marker.addItem("Hot Cue F", 5)
        self.drop_marker.addItem("Hot Cue G", 6)
        self.drop_marker.addItem("Hot Cue H", 7)
        self.drop_marker.setCurrentIndex(drop_mark_num)
        self.main_layout.addWidget(self.drop_marker)

        # Cue point rules
        self.hot_cues_label = QLabel("Cue points")
        self.main_layout.addWidget(self.hot_cues_label)
        self.cue_points_table = QTableWidget(0, 4)  # 0 rows, 4 columns
        self.cue_points_table.setHorizontalHeaderLabels(["Num", "Type", "Name", "Beats"])
        self.main_layout.addWidget(self.cue_points_table)

        self.add_cue_point_button = QPushButton("Add Cue Point")
        self.add_cue_point_button.clicked.connect(self.add_cue_point)
        self.remove_cue_point_button = QPushButton("Remove Cue Point")
        self.remove_cue_point_button.clicked.connect(self.remove_cue_point)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_cue_point_button)
        button_layout.addWidget(self.remove_cue_point_button)
        self.main_layout.addLayout(button_layout)

        # Process button
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_playlists)
        self.main_layout.addWidget(self.process_button)

        # Log/progress text area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.main_layout.addWidget(self.log_area)

        self.setCentralWidget(self.central_widget)

        # Load settings
        self.settings = QSettings("MyCompany", "MyApp")
        self.last_dir = self.settings.value("last_dir", "")

    def load_xml(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open XML", self.last_dir, "XML Files (*.xml)")
        if filename:
            self.xml_path = filename
            self.log_area.append(f"Loaded XML: {filename}")
            # Load XML and populate playlist_list
            self.collection = RekordboxXml(self.xml_path)
            self.playlist_list.clear()
            for playlist in self.collection._root_node.get_playlists():
                self.playlist_list.addItem(playlist.name)

            # Remember the directory
            self.last_dir = filename
            self.settings.setValue("last_dir", self.last_dir)

    def add_cue_point(self):
        self.cue_points_table.insertRow(self.cue_points_table.rowCount())

    def remove_cue_point(self):
        selected_rows = [item.row() for item in self.cue_points_table.selectedItems()]
        for row in sorted(selected_rows, reverse=True):
            self.cue_points_table.removeRow(row)

    def load_defaults(self):
        for mark in cue_points:
            self.cue_points_table.insertRow(self.cue_points_table.rowCount())
            self.cue_points_table.setItem(self.cue_points_table.rowCount() - 1, 0, QTableWidgetItem(str(mark["num"])))
            self.cue_points_table.setItem(self.cue_points_table.rowCount() - 1, 1, QTableWidgetItem(mark["type"]))
            self.cue_points_table.setItem(self.cue_points_table.rowCount() - 1, 2, QTableWidgetItem(mark["name"]))
            self.cue_points_table.setItem(self.cue_points_table.rowCount() - 1, 3, QTableWidgetItem(str(mark["beats"])))

    def process_playlists(self):
        if self.process_all.isChecked():
            selected_playlists = None
            self.log_area.append("Processing entire collection")
        else:
            selected_playlists = [item.text() for item in self.playlist_list.selectedItems()]
            self.log_area.append(f"Processing playlists: {', '.join(selected_playlists)}")
            
        drop_marker_num = self.drop_marker.currentData()

        cue_points = []
        for row in range(self.cue_points_table.rowCount()):
            num = int(self.cue_points_table.item(row, 0).text())
            type = self.cue_points_table.item(row, 1).text()
            name = self.cue_points_table.item(row, 2).text()
            beats = int(self.cue_points_table.item(row, 3).text())
            cue_points.append({"num": num, "type": type, "name": name, "beats": beats})

        # Call process_collection_xml with the selected playlists and options
        process_collection_xml(
            self.xml_path,
            selected_playlists,
            remove_existing_marks=self.remove_existing_marks.isChecked(),
            retain_first_tempo=self.retain_first_tempo.isChecked(),
            drop_mark_num=drop_marker_num,
            cue_points=cue_points
        )

    def run(self):
        self.show()