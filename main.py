import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QComboBox, QLineEdit, QHBoxLayout, QGroupBox, QListWidget, QListWidgetItem, QMessageBox, QCheckBox
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImageReader, QIntValidator
from PyQt5.QtCore import Qt, QRect
import qtmodern.styles
import qtmodern.windows
# import qdarkstyle

class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()

        # Dictionary to store integer labels and their descriptions
        self.label_map = {}
        self.next_label = 0

        # Label adding section
        label_group = QGroupBox("Add Labels")
        label_layout = QHBoxLayout()

        # Input for label descriptions
        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText("Enter description (optional) e.g., 'Cat'")
        label_layout.addWidget(self.label_input)

        # Button to add label
        self.add_label_button = QPushButton("Add Label", self)
        self.add_label_button.clicked.connect(self.add_label)
        label_layout.addWidget(self.add_label_button)
        label_group.setLayout(label_layout)

        self.delete_label_button = QPushButton("Delete Label", self)
        self.delete_label_button.clicked.connect(self.delete_selected_label)
        label_layout.addWidget(self.delete_label_button)
        label_group.setLayout(label_layout)

        layout.addWidget(label_group)

        # Display labels in a list widget
        self.labels_list = QListWidget()
        layout.addWidget(self.labels_list)

        # Folder picking section
        folder_layout = QHBoxLayout()

        self.folder_label = QLabel("No folder selected")
        folder_layout.addWidget(self.folder_label)

        # Button to pick a folder
        self.pick_folder_button = QPushButton("Pick Image Folder", self)
        self.pick_folder_button.clicked.connect(self.pick_folder)
        folder_layout.addWidget(self.pick_folder_button)

        # Import JSON button
        self.import_json_btn = QPushButton('Import JSON', self)
        self.import_json_btn.clicked.connect(self.import_json_labels)
        folder_layout.addWidget(self.import_json_btn)

        layout.addLayout(folder_layout)

        # Resolution section
        resolution_group = QGroupBox("Set Image Scale Resolution")
        resolution_layout = QHBoxLayout()

        # Input for width
        self.width_input = QLineEdit(self)
        self.width_input.setValidator(QIntValidator())  # Only allow integers
        self.width_input.setPlaceholderText("Width - Default: 800")
        resolution_layout.addWidget(self.width_input)

        # Input for height
        self.height_input = QLineEdit(self)
        self.height_input.setValidator(QIntValidator())  # Only allow integers
        self.height_input.setPlaceholderText("Height - Default: 600")
        resolution_layout.addWidget(self.height_input)
        resolution_group.setLayout(resolution_layout)
        layout.addWidget(resolution_group)

        # Dataset Checkbox
        self.dataset_checkbox = QCheckBox("Create Dataset", self)
        self.dataset_checkbox.stateChanged.connect(self.toggle_dataset_options)
        layout.addWidget(self.dataset_checkbox)

        # YAML Options in a GroupBox
        self.dataset_options_group = QGroupBox("Dataset Options", self)
        dataset_options_layout = QVBoxLayout(self.dataset_options_group)

        # Train images folder
        self.dataset_folder_label = QLabel("Dataset Folder:", self)
        self.dataset_folder_btn = QPushButton("Select Dataset Folder", self)
        self.dataset_folder_btn.clicked.connect(self.select_dataset_folder)
        dataset_options_layout.addWidget(self.dataset_folder_label)
        dataset_options_layout.addWidget(self.dataset_folder_btn)

        self.train_percentage_label = QLabel("Train Images Percentage:", self)
        self.train_percentage_input = QLineEdit(self)
        self.train_percentage_input.setValidator(QIntValidator(0, 100))  # Only allow integers from 0 to 100
        self.train_percentage_input.setPlaceholderText("70")  # Default suggestion
        dataset_options_layout.addWidget(self.train_percentage_label)
        dataset_options_layout.addWidget(self.train_percentage_input)

        # Validation percentage
        self.val_percentage_label = QLabel("Validation Images Percentage:", self)
        self.val_percentage_input = QLineEdit(self)
        self.val_percentage_input.setValidator(QIntValidator(0, 100))  # Only allow integers from 0 to 100
        self.val_percentage_input.setPlaceholderText("15")  # Default suggestion
        dataset_options_layout.addWidget(self.val_percentage_label)
        dataset_options_layout.addWidget(self.val_percentage_input)

        # Test percentage
        self.test_percentage_label = QLabel("Test Images Percentage:", self)
        self.test_percentage_input = QLineEdit(self)
        self.test_percentage_input.setValidator(QIntValidator(0, 100))  # Only allow integers from 0 to 100
        self.test_percentage_input.setPlaceholderText("15")  # Default suggestion
        dataset_options_layout.addWidget(self.test_percentage_label)
        dataset_options_layout.addWidget(self.test_percentage_input)

        # Create YAML file checkbox
        self.yaml_checkbox = QCheckBox("Create Yaml File", self)
        dataset_options_layout.addWidget(self.yaml_checkbox)

        layout.addWidget(self.dataset_options_group)

        # Start button section
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_main_window)
        self.start_button.setEnabled(False)  # Initially disabled, will be enabled when a folder is selected

        layout.addWidget(self.start_button)

        self.dataset_options_group.hide() # Hide it initially

        self.setLayout(layout)

    def delete_selected_label(self):
        selected_items = self.labels_list.selectedItems()
        if not selected_items:  # If no label is selected
            return

        for item in selected_items:
            # Extract the label number from the item text
            label_number = int(item.text().split(" - ")[0])
            # Remove the item from the list widget
            self.labels_list.takeItem(self.labels_list.row(item))
            # Remove the label from label_map
            if label_number in self.label_map:
                del self.label_map[label_number]

    def toggle_dataset_options(self, state):
        if state == Qt.Checked:
            self.dataset_options_group.show()
            self.yaml_checkbox.setChecked(True)
        else:
            self.dataset_options_group.hide()
            self.yaml_checkbox.setChecked(False)

    def select_dataset_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Dataset Folder")
        if folder:
            self.dataset_folder_btn.setText(folder)  # Display the selected folder path on the button


    def create_yaml_file(self):
        yaml_file_path = os.path.join(self.dataset_folder_btn.text(), 'dataset.yaml')

        # Create the YAML file
        with open(yaml_file_path, 'w') as yaml_file:
            yaml_file.write(f"train: {os.path.join('../train/images')}\n")
            yaml_file.write(f"val: {os.path.join('../val/images')}\n")
            yaml_file.write(f"test: {os.path.join('../test/images')}\n\n")
            yaml_file.write(f"nc: {len(self.label_map)}\n")

            # Write class names
            yaml_file.write("names: [")
            for i, name in enumerate(self.label_map.values()):
                if i > 0:
                    yaml_file.write(", ")
                yaml_file.write(f"'{name}'")
            yaml_file.write("]\n")

        # Notify the user that the YAML file was created
        QMessageBox.information(self, "Success", f"YAML file saved at {yaml_file_path}")

    def add_label(self):
        description = self.label_input.text().strip()
        self.label_map[str(self.next_label)] = description if description else str(self.next_label)
        display_text = f"{self.next_label} - {description}" if description else str(self.next_label)
        self.labels_list.addItem(QListWidgetItem(display_text))
        self.next_label += 1
        self.label_input.clear()

    def import_json_labels(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Import JSON File", "", "JSON Files (*.json);;All Files (*)",
                                                  options=options)
        if filePath:
            try:
                with open(filePath, 'r') as file:
                    data = json.load(file)
                    highest_key = -1
                    for key, value in data.items():
                        int_key = int(key)
                        if int_key > highest_key:
                            highest_key = int_key

                        # Check if the label key already exists
                        if int_key not in self.label_map:
                            # Add the label to label_map
                            self.label_map[int_key] = value
                            # Add to the UI list with consistent formatting
                            self.labels_list.addItem(f"{int_key} - {value}")

                    # Set the next_label to be one more than the highest key found
                    self.next_label = highest_key + 1
            except Exception as e:
                # Display any errors in a message box
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def pick_folder(self):
        # Open a QFileDialog to pick a folder
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:  # Check if a folder was selected
            self.folder_label.setText(folder)
            self.start_button.setEnabled(True)  # Enable the start button

    def start_main_window(self):
        folder_path = self.folder_label.text()
        image_paths = [folder_path + '/' + f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]  # You can add more extensions if needed

        # Check if there are valid image files in the selected folder
        if not image_paths:
            self.folder_label.setText("No valid image files found!")
            return

        try:
            width = int(self.width_input.text()) if self.width_input.text() else 800
            height = int(self.height_input.text()) if self.height_input.text() else 600
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid integers for width and height.")
            return

        if self.dataset_checkbox.isChecked():
            train_percentage = int(
                self.train_percentage_input.text()) if self.train_percentage_input.text() else 70  # Default 70
            val_percentage = int(self.val_percentage_input.text()) if self.val_percentage_input.text() else 15  # Default 15
            test_percentage = int(
                self.test_percentage_input.text()) if self.test_percentage_input.text() else 15  # Default 15

            # Ensure the total is 100
            if train_percentage + val_percentage + test_percentage != 100:
                QMessageBox.warning(self, "Invalid Input", "Matematik Hocana....")
                return

        if self.yaml_checkbox.isChecked():
            if self.dataset_folder_btn.text() == "Select Dataset Folder":
                QMessageBox.warning(self, "Error", "Please select dataset folder.")
                return
            # Create the YAML file at the top of the images directory
            self.create_yaml_file()

        # Start the main ImageWidget and close this SetupWindow
        self.main_window = ImageWidget(image_paths, self.label_map, (width, height), [train_percentage, val_percentage, test_percentage] if self.dataset_checkbox.isChecked() else None, self.dataset_folder_btn.text() if self.dataset_checkbox.isChecked() else None)
        self.main_window.setWindowTitle("YOLO DATA LABELER BY MELIH TASKIN")
        self.main_window.show()
        self.close()

class ImageWidget(QWidget):
    def __init__(self, image_paths, label_map=None, resolution=(800, 600), percentages=None, dataset_folder=None):
        super().__init__()

        self.image_paths = image_paths
        self.current_image_index = 0
        self.label_map = label_map if label_map else {}
        self.percentages = percentages
        self.dataset_folder = dataset_folder


        # Define the maximum display size
        self.display_size = resolution

        # Load and scale the first image
        self.image = self.load_and_scale_image(self.image_paths[self.current_image_index])

        # Set the initial window size
        self.adjust_window_size()

        # List to store the drawn rectangles and their labels
        self.rectangles = []

        # Drawing attributes
        self.startPoint = None
        self.endPoint = None
        self.isDrawing = False

        # Add Next button
        self.next_button = QPushButton("Next Image", self)
        self.next_button.clicked.connect(self.load_next_image)
        self.position_button()

        # Add Undo button
        self.undo_button = QPushButton("Undo", self)
        self.undo_button.clicked.connect(self.undo_last_rectangle)
        self.position_undo_button()

        # Add ComboBox
        self.comboBox = QComboBox(self)
        for key, value in self.label_map.items():
            self.comboBox.addItem(value, userData=key)
        self.position_combobox()

    def adjust_window_size(self):
        self.setFixedSize(self.image.size().width(), self.image.size().height() + 40)

    def position_button(self):
        self.next_button.resize(100, 30)
        self.next_button.move(self.image.width() - 110, self.image.height() + 5)

    def position_undo_button(self):
        self.undo_button.resize(100, 30)
        self.undo_button.move(self.image.width() - 280, self.image.height() + 5)

    def position_combobox(self):
        self.comboBox.resize(100, 30)
        self.comboBox.move(self.image.width() - 390, self.image.height() + 5)

    def load_and_scale_image(self, path):
        # reader = QImageReader(path)
        # reader.setScaledSize(reader.size().scaled(self.display_size[0], self.display_size[1], Qt.KeepAspectRatio))
        pixmap = QPixmap(path)
        resized_pixmap = pixmap.scaled(self.display_size[0], self.display_size[1])
        # Extracting filename from the path and prepending 'scaled_' for the saved image.
        if self.dataset_folder is None:
            base_path = os.path.dirname(path)
            top_directory = os.path.dirname(base_path)
            scaledImages_dir = os.path.join(top_directory, 'scaledImages')
            os.makedirs(scaledImages_dir, exist_ok=True)  # Make sure this is before saving the image

            scaled_path = os.path.join(scaledImages_dir, path.split("/")[-1])
            self.save_image(scaled_path, resized_pixmap)
        else:
            if self.current_image_index <= int(len(self.image_paths) * self.percentages[0] / 100):
                path = os.path.join(self.dataset_folder, 'train/images', path.split("/")[-1])
                os.makedirs(os.path.dirname(path), exist_ok=True)
                self.save_image(path, resized_pixmap)
            elif self.current_image_index <= int(len(self.image_paths) * (self.percentages[0] + self.percentages[1]) / 100):
                path = os.path.join(self.dataset_folder, 'val/images', path.split("/")[-1])
                os.makedirs(os.path.dirname(path), exist_ok=True)
                self.save_image(path, resized_pixmap)
            else:
                path = os.path.join(self.dataset_folder, 'test/images', path.split("/")[-1])
                os.makedirs(os.path.dirname(path), exist_ok=True)
                self.save_image(path, resized_pixmap)
        return resized_pixmap

    def calculate_rectangles(self):
        outputs = []
        for rectangle, label_text in self.rectangles:
            label = self.comboBox.itemData(self.comboBox.findText(label_text))  # Get the integer value of the label
            x_center = ((rectangle.topLeft().x() + rectangle.bottomRight().x()) / 2) / self.image.width()
            y_center = ((rectangle.topLeft().y() + rectangle.bottomRight().y()) / 2) / self.image.height()
            width = (rectangle.bottomRight().x() - rectangle.topLeft().x()) / self.image.width()
            height = (rectangle.bottomRight().y() - rectangle.topLeft().y()) / self.image.height()

            output = f"{label} {x_center} {y_center} {width} {height}"
            outputs.append(output)

        return outputs

    def write_to_file(self, calculations):
        # Extract image filename without extension
        filename_without_extension = os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0]
        filename = filename_without_extension + ".txt"
        if calculations is not None:
            # Construct the path for the new .txt file
            # It will be saved in a 'labels' directory at the top of the image path
            if self.dataset_folder is None:
                base_path = os.path.dirname(self.image_paths[self.current_image_index])
                top_directory = os.path.dirname(base_path)
                labels_dir = os.path.join(top_directory, 'labels')
                filepath = os.path.join(labels_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
            else:
                base_path = os.path.join(self.dataset_folder)
                if self.current_image_index <= int(len(self.image_paths) * self.percentages[0] / 100):
                    train_dir = os.path.join(base_path, 'train/labels')
                    filepath = os.path.join(train_dir, filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                elif self.current_image_index <= int(len(self.image_paths) * (self.percentages[0] + self.percentages[1]) / 100):
                    val_dir = os.path.join(base_path, 'val/labels')
                    filepath = os.path.join(val_dir, filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                else:
                    test_dir = os.path.join(base_path, 'test/labels')
                    filepath = os.path.join(test_dir, filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "w") as f:
                for calc in calculations:
                    f.write(f"{calc}\n")

    def save_image(self, path, pixmap):
        pixmap.save(path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image)

        for rectangle, label in self.rectangles:
            pen = QPen(Qt.red, 3, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(rectangle)
            painter.drawText(rectangle.center(), label)  # Draw the label in the top-left corner of the rectangle

        if self.startPoint and self.endPoint:
            pen = QPen(Qt.red, 3, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(QRect(self.startPoint, self.endPoint))
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_within_image_bounds(event.pos()):
            self.startPoint = event.pos()
            self.endPoint = event.pos()
            self.isDrawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.isDrawing and self.is_within_image_bounds(event.pos()):
            self.endPoint = event.pos()
            self.update()  # Trigger a paint event

    def mouseReleaseEvent(self, event):
        if self.isDrawing:
            self.endPoint = event.pos()
            self.isDrawing = False
            if self.startPoint != self.endPoint:
                current_label = self.comboBox.currentText()
                self.rectangles.append((QRect(self.startPoint, self.endPoint), current_label))
            self.update()

    def undo_last_rectangle(self):
        if self.rectangles:
            self.rectangles.pop()

            # Reset the temporary drawing points
            self.startPoint = None
            self.endPoint = None

            self.update()

    def load_next_image(self):
        calculations = self.calculate_rectangles()
        self.write_to_file(calculations)

        self.rectangles = []
        self.startPoint = None  # Clear the start and end points.
        self.endPoint = None
        self.current_image_index += 1

        if self.current_image_index >= len(self.image_paths) - 1:
            self.next_button.setText("Exit")
            self.next_button.clicked.disconnect(self.load_next_image)  # Remove the old connection
            self.next_button.clicked.connect(self.close_app)  # Connect to the close function



        self.image = self.load_and_scale_image(self.image_paths[self.current_image_index])
        self.adjust_window_size()
        self.position_button()
        self.position_undo_button()
        self.position_combobox()
        self.update()

    def close_app(self):
        calculations = self.calculate_rectangles()
        self.write_to_file(calculations)

        self.close()

    def is_within_image_bounds(self, point):
        return QRect(0, 0, self.image.width(), self.image.height()).contains(point)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    # def load_stylesheet(filename):
    #     with open(filename, "r") as f:
    #         return f.read()
    #
    # qss = load_stylesheet("style.qss")
    # app.setStyleSheet(qss)

    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    setup_window = SetupWindow()
    setup_window.setWindowTitle("YOLO DATA LABELER BY MELIH TASKIN")
    setup_window.show()

    setup_window_modern = qtmodern.windows.ModernWindow(setup_window)
    setup_window_modern.show()

    sys.exit(app.exec_())