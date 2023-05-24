from PyQt5.QtWidgets import QTableWidget, QHBoxLayout, QMainWindow, QTableWidgetItem, QPushButton, QListWidget, QCheckBox, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QComboBox, QLabel, QGroupBox
from PyQt5.QtCore import Qt, QSettings
from automark.automark import process_collection_xml

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
        self.process_all.stateChanged.connect(self.toggle_playlist_selection)
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
        self.cue_points_label = QLabel("Cue points")
        self.main_layout.addWidget(self.cue_points_label)

        # Hot cue points
        self.hot_cue_points_box = QGroupBox("Hot Cues")
        self.hot_cue_layout = QVBoxLayout()
        self.hot_cue_points_box.setLayout(self.hot_cue_layout)
        self.hot_cue_points_table = QTableWidget(0, 3)  # 0 rows, 3 columns
        self.hot_cue_points_table.setHorizontalHeaderLabels(["Letter", "Name", "Beats"])
        self.hot_cue_layout.addWidget(self.hot_cue_points_table)
        self.main_layout.addWidget(self.hot_cue_points_box)

        # Memory cue points
        self.memory_cue_points_box = QGroupBox("Memory Cues")
        self.memory_cue_layout = QVBoxLayout()
        self.memory_cue_points_box.setLayout(self.memory_cue_layout)
        self.memory_cue_points_table = QTableWidget(0, 2)  # 0 rows, 2 columns
        self.memory_cue_points_table.setHorizontalHeaderLabels(["Name", "Beats"])
        self.memory_cue_layout.addWidget(self.memory_cue_points_table)
        self.main_layout.addWidget(self.memory_cue_points_box)

        # Add and Remove buttons for Hot Cues
        self.add_hot_cue_point_button = QPushButton("Add Hot Cue")
        self.remove_hot_cue_point_button = QPushButton("Remove Hot Cue")

        # Specify actions for the buttons
        self.add_hot_cue_point_button.clicked.connect(self.add_hot_cue_point)
        self.remove_hot_cue_point_button.clicked.connect(self.remove_hot_cue_point)
        
        hot_button_layout = QHBoxLayout()
        hot_button_layout.addWidget(self.add_hot_cue_point_button)
        hot_button_layout.addWidget(self.remove_hot_cue_point_button)
        self.hot_cue_layout.addLayout(hot_button_layout)

        # Add and Remove buttons for Memory Cues
        self.add_memory_cue_point_button = QPushButton("Add Memory Cue")
        self.remove_memory_cue_point_button = QPushButton("Remove Memory Cue")

        # Specify actions for the buttons
        self.add_memory_cue_point_button.clicked.connect(self.add_memory_cue_point)
        self.remove_memory_cue_point_button.clicked.connect(self.remove_memory_cue_point)
        
        memory_button_layout = QHBoxLayout()
        memory_button_layout.addWidget(self.add_memory_cue_point_button)
        memory_button_layout.addWidget(self.remove_memory_cue_point_button)
        self.memory_cue_layout.addLayout(memory_button_layout)

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



    def add_hot_cue_point(self):
        self.hot_cue_points_table.insertRow(self.hot_cue_points_table.rowCount())

    def remove_hot_cue_point(self):
        selected_rows = [item.row() for item in self.hot_cue_points_table.selectedItems()]
        for row in sorted(selected_rows, reverse=True):
            self.hot_cue_points_table.removeRow(row)

    def add_memory_cue_point(self):
        self.memory_cue_points_table.insertRow(self.memory_cue_points_table.rowCount())

    def remove_memory_cue_point(self):
        selected_rows = [item.row() for item in self.memory_cue_points_table.selectedItems()]
        for row in sorted(selected_rows, reverse=True):
            self.memory_cue_points_table.removeRow(row)



    def load_defaults(self):
        pass
    #     for mark in cue_points:
    #         self.cue_points_table.insertRow(self.cue_points_table.rowCount())
    #         self.cue_points_table.setItem(self.cue_points_table.rowCount() - 1, 0, QTableWidgetItem(str(mark["num"])))
    #         self.cue_points_table.setItem(self.cue_points_table.rowCount() - 1, 1, QTableWidgetItem(mark["type"]))
    #         self.cue_points_table.setItem(self.cue_points_table.rowCount() - 1, 2, QTableWidgetItem(mark["name"]))
    #         self.cue_points_table.setItem(self.cue_points_table.rowCount() - 1, 3, QTableWidgetItem(str(mark["beats"])))

    def toggle_playlist_selection(self, state):
        # If state is nonzero (i.e., the checkbox is checked), disable the playlist selection widget.
        # Otherwise, enable it.
        self.playlist_list.setDisabled(state != 0)

    def process_playlists(self):
        if self.process_all.isChecked():
            selected_playlists = None
            self.log_area.append("Processing entire collection")
        else:
            selected_playlists = [item.text() for item in self.playlist_list.selectedItems()]
            self.log_area.append(f"Processing playlists: {', '.join(selected_playlists)}")
            
        drop_marker_num = self.drop_marker.currentData()

        # Reading cue points from tables
        hot_cue_points = []
        for row in range(self.hot_cue_points_table.rowCount()):
            letter = self.hot_cue_points_table.item(row, 0).text()
            num = ord(letter.upper()) - ord('A')
            name = self.hot_cue_points_table.item(row, 1).text()
            beats = int(self.hot_cue_points_table.item(row, 2).text())
            hot_cue_points.append({"num": num, "type": "HOT_CUE", "name": name, "beats": beats})

        memory_cue_points = []
        for row in range(self.memory_cue_points_table.rowCount()):
            name = self.memory_cue_points_table.item(row, 0).text()
            beats = int(self.memory_cue_points_table.item(row, 1).text())
            memory_cue_points.append({"num": -1, "type": "MEMORY_CUE", "name": name, "beats": beats})

        cue_points = hot_cue_points + memory_cue_points

        # Call process_collection_xml with the selected playlists and options
        process_collection_xml(
            # [code omitted for brevity]
            cue_points=cue_points
        )

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