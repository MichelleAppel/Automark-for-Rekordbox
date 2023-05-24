from PyQt5.QtWidgets import QPushButton, QFileDialog, QListWidget, QAbstractItemView, QLabel, QVBoxLayout, QWidget, QCheckBox, QPlainTextEdit, QTableWidget, QGroupBox
from PyQt5.QtCore import pyqtSlot, QSettings

import json

from automark.xml import RekordboxXml

class XMLLoadButton(QPushButton):
    def __init__(self, widgets):
        super().__init__("Load XML")

        self.widgets = widgets

        self.clicked.connect(self.load_xml)

        # Load settings
        self.settings = QSettings("Personal", "Default")
        self.last_dir = self.settings.value("last_dir", "")


    @pyqtSlot()
    def load_xml(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open XML", self.last_dir, "XML Files (*.xml)")
        if filename:
            self.xml_path = filename
            self.widgets['log_area'].appendPlainText(f"Loaded XML: {filename}")

            # Load XML and populate playlist_list
            self.collection = RekordboxXml(self.xml_path)
            self.widgets['playlist_list'].clear()
            for playlist in self.collection._root_node.get_playlists():
                self.widgets['playlist_list'].addItem(playlist.name)

            # Remember the directory
            self.last_dir = filename
            self.settings.setValue("last_dir", self.last_dir)


class PlaylistSelectionWidget(QWidget):
    def __init__(self, widgets):
        super().__init__()

        self.widgets = widgets

        self.playlist_list = QListWidget()
        self.playlist_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.playlist_list.itemSelectionChanged.connect(self.playlist_selection_changed)

        self.playlist_list_label = QLabel("Playlists:")

        self.playlist_selection_layout = QVBoxLayout()
        self.playlist_selection_layout.addWidget(self.playlist_list_label)
        self.playlist_selection_layout.addWidget(self.playlist_list)

        self.setLayout(self.playlist_selection_layout)

    def playlist_selection_changed(self):
        self.widgets['log_area'].appendPlainText(f"Selected playlists: {[x.text() for x in self.widgets['playlist_list'].selectedItems()]}")


class CollectionProcessCheckbox(QWidget):
    def __init__(self, widgets):
        super().__init__()

        self.widgets = widgets

        self.process_all = QCheckBox("Process entire collection")
        self.process_all.stateChanged.connect(self.toggle_playlist_selection)

        self.process_all_layout = QVBoxLayout()
        self.process_all_layout.addWidget(self.process_all)

        self.setLayout(self.process_all_layout)

    def toggle_playlist_selection(self):
        if self.process_all.isChecked():
            self.widgets['playlist_list'].setEnabled(False)
        else:
            self.widgets['playlist_list'].setEnabled(True)


class MarksOverrideCheckbox(QWidget):
    def __init__(self):
        super().__init__()

        self.remove_existing_marks = QCheckBox("Overwrite existing marks")
        self.remove_existing_marks.setChecked(True)

        self.remove_existing_marks_layout = QVBoxLayout()
        self.remove_existing_marks_layout.addWidget(self.remove_existing_marks)

        self.setLayout(self.remove_existing_marks_layout)


class RetainFirstTempoCheckbox(QWidget):
    def __init__(self):
        super().__init__()

        self.retain_first_tempo = QCheckBox("Retain first tempo")
        self.retain_first_tempo.setChecked(True)

        self.retain_first_tempo_layout = QVBoxLayout()
        self.retain_first_tempo_layout.addWidget(self.retain_first_tempo)

        self.setLayout(self.retain_first_tempo_layout)


from PyQt5.QtWidgets import QLabel, QVBoxLayout, QComboBox, QWidget

class DropMarkerSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.drop_marker_label = QLabel("Drop marker:")

        # Initialize QComboBox
        self.drop_marker_combo = QComboBox()

        # Add items to the combo box
        self.add_items_to_combo_box()

        # Set the current index, assuming drop_mark_num is a variable holding the index value
        # You may want to replace this with the correct logic for getting the current index
        self.drop_marker_combo.setCurrentIndex(3)

        # Set layout
        self.drop_marker_selection_layout = QVBoxLayout()
        self.drop_marker_selection_layout.addWidget(self.drop_marker_label)
        self.drop_marker_selection_layout.addWidget(self.drop_marker_combo)

        self.setLayout(self.drop_marker_selection_layout)

    def add_items_to_combo_box(self):
        self.drop_marker_combo.addItem("Hot Cue A", 0)
        self.drop_marker_combo.addItem("Hot Cue B", 1)
        self.drop_marker_combo.addItem("Hot Cue C", 2)
        self.drop_marker_combo.addItem("Hot Cue D", 3)
        self.drop_marker_combo.addItem("Hot Cue E", 4)
        self.drop_marker_combo.addItem("Hot Cue F", 5)
        self.drop_marker_combo.addItem("Hot Cue G", 6)
        self.drop_marker_combo.addItem("Hot Cue H", 7)


class HotCuePointsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.hot_cue_points_box = QGroupBox("Hot Cues")
        self.hot_cue_layout = QVBoxLayout()
        self.hot_cue_points_box.setLayout(self.hot_cue_layout)

        self.hot_cue_points_table = QTableWidget(0, 3)  # 0 rows, 3 columns
        self.hot_cue_points_table.setHorizontalHeaderLabels(["Letter", "Name", "Beats"])
        self.hot_cue_layout.addWidget(self.hot_cue_points_table)

        self.add_hot_cue_point_button = QPushButton("Add Hot Cue")
        self.add_hot_cue_point_button.clicked.connect(self.add_hot_cue_point)
        self.remove_hot_cue_point_button = QPushButton("Remove Hot Cue")
        self.remove_hot_cue_point_button.clicked.connect(self.remove_hot_cue_point)

        self.hot_cue_layout.addWidget(self.add_hot_cue_point_button)
        self.hot_cue_layout.addWidget(self.remove_hot_cue_point_button)

        self.setLayout(self.hot_cue_layout)

    def add_hot_cue_point(self):
        self.hot_cue_points_table.insertRow(self.hot_cue_points_table.rowCount())

    def remove_hot_cue_point(self):
        selected_rows = [item.row() for item in self.hot_cue_points_table.selectedItems()]
        for row in sorted(selected_rows, reverse=True):
            self.hot_cue_points_table.removeRow(row)


class MemoryCuePointsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.memory_cue_points_box = QGroupBox("Memory Cues")
        self.memory_cue_layout = QVBoxLayout()
        self.memory_cue_points_box.setLayout(self.memory_cue_layout)

        self.memory_cue_points_table = QTableWidget(0, 2)  # 0 rows, 2 columns
        self.memory_cue_points_table.setHorizontalHeaderLabels(["Name", "Beats"])
        self.memory_cue_layout.addWidget(self.memory_cue_points_table)

        self.add_memory_cue_point_button = QPushButton("Add Memory Cue")
        self.add_memory_cue_point_button.clicked.connect(self.add_memory_cue_point)
        self.remove_memory_cue_point_button = QPushButton("Remove Memory Cue")
        self.remove_memory_cue_point_button.clicked.connect(self.remove_memory_cue_point)

        self.memory_cue_layout.addWidget(self.add_memory_cue_point_button)
        self.memory_cue_layout.addWidget(self.remove_memory_cue_point_button)

        self.setLayout(self.memory_cue_layout)

    def add_memory_cue_point(self):
        self.memory_cue_points_table.insertRow(self.memory_cue_points_table.rowCount())

    def remove_memory_cue_point(self):
        selected_rows = [item.row() for item in self.memory_cue_points_table.selectedItems()]
        for row in sorted(selected_rows, reverse=True):
            self.memory_cue_points_table.removeRow(row)


class ProcessButton(QPushButton):
    def __init__(self):
        super().__init__("Process")


class LogArea(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setReadOnly(True)


class PresetWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.save_button = QPushButton("Save Presets")
        self.save_button.clicked.connect(self.save_presets)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Presets")
        self.load_button.clicked.connect(self.load_presets)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)

    def save_presets(self):
        presets = {
            "hot_cue_points": self.parent().hot_cue_points,
            "memory_cue_points": self.parent().memory_cue_points,
            "loop_cue_points": self.parent().loop_cue_points,
        }

        settings = QSettings()
        for preset_name, preset_value in presets.items():
            settings.setValue(preset_name, json.dumps(preset_value))

    def load_presets(self):
        settings = QSettings()
        self.parent().hot_cue_points = json.loads(settings.value("hot_cue_points", json.dumps(self.parent().hot_cue_points)))
        self.parent().memory_cue_points = json.loads(settings.value("memory_cue_points", json.dumps(self.parent().memory_cue_points)))
        self.parent().loop_cue_points = json.loads(settings.value("loop_cue_points", json.dumps(self.parent().loop_cue_points)))

        # Update the GUI elements to reflect the loaded presets
        self.parent().update_gui_elements()