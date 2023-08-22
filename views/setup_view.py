from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLineEdit, QPushButton, QListWidget,
                             QLabel, QCheckBox)
from PyQt5.QtGui import QIntValidator


class SetupView(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout(self)

        # Label adding section
        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Enter description (optional) e.g., 'Cat'")

        self.add_label_button = QPushButton("Add Label", self)
        self.delete_label_button = QPushButton("Delete Label", self)

        label_group = QGroupBox("Add Labels")
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.label_input)
        label_layout.addWidget(self.add_label_button)
        label_layout.addWidget(self.delete_label_button)
        label_group.setLayout(label_layout)
        layout.addWidget(label_group)

        # Display labels in a list widget
        self.labels_list = QListWidget()
        layout.addWidget(self.labels_list)

        # Folder selecting section
        self.folder_label = QLabel("No folder selected")
        self.select_folder_button = QPushButton("Select Image Folder", self)
        self.import_json_btn = QPushButton('Import JSON', self)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.select_folder_button)
        folder_layout.addWidget(self.import_json_btn)
        layout.addLayout(folder_layout)

        # Resolution section
        self.width_input = QLineEdit(self)
        self.width_input.setValidator(QIntValidator())  # Only allow integers
        self.width_input.setPlaceholderText("Width - Default: 800")

        self.height_input = QLineEdit(self)
        self.height_input.setValidator(QIntValidator())  # Only allow integers
        self.height_input.setPlaceholderText("Height - Default: 600")

        resolution_group = QGroupBox("Set Image Scale Resolution")
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(self.width_input)
        resolution_layout.addWidget(self.height_input)
        resolution_group.setLayout(resolution_layout)
        layout.addWidget(resolution_group)

        # Dataset Checkbox
        self.dataset_checkbox = QCheckBox("Create Dataset", self)
        layout.addWidget(self.dataset_checkbox)

        # Dataset Options in a GroupBox
        self.dataset_options_group = QGroupBox("Dataset Options", self)
        self.dataset_folder_btn = QPushButton("Select Dataset Folder", self)
        self.train_percentage_input = QLineEdit(self)
        self.train_percentage_input.setValidator(QIntValidator(0, 100))  # Only allow integers from 0 to 100
        self.train_percentage_input.setPlaceholderText("70")  # Default suggestion

        self.val_percentage_input = QLineEdit(self)
        self.val_percentage_input.setValidator(QIntValidator(0, 100))  # Only allow integers from 0 to 100
        self.val_percentage_input.setPlaceholderText("15")  # Default suggestion

        self.test_percentage_input = QLineEdit(self)
        self.test_percentage_input.setValidator(QIntValidator(0, 100))  # Only allow integers from 0 to 100
        self.test_percentage_input.setPlaceholderText("15")  # Default suggestion

        self.yaml_checkbox = QCheckBox("Create Yaml File", self)

        dataset_options_layout = QVBoxLayout(self.dataset_options_group)
        dataset_options_layout.addWidget(self.dataset_folder_btn)
        dataset_options_layout.addWidget(self.train_percentage_input)
        dataset_options_layout.addWidget(self.val_percentage_input)
        dataset_options_layout.addWidget(self.test_percentage_input)
        dataset_options_layout.addWidget(self.yaml_checkbox)

        layout.addWidget(self.dataset_options_group)

        # Start button section
        self.start_button = QPushButton("Start", self)
        self.start_button.setEnabled(False)  # Initially disabled
        layout.addWidget(self.start_button)

        self.dataset_options_group.hide()  # Hide it initially
        self.setLayout(layout)
