from PyQt5.QtWidgets import QMessageBox, QFileDialog

from models.image_window_model import ImageWindowModel
from presenters.image_window_presenter import ImageWindowPresenter
from views.image_window_view import ImageWindowView


class SetupPresenter:
    def __init__(self, view, model):
        # Store references to the view and model
        self.view = view
        self.model = model

        # Connect view signals to presenter methods
        self.view.add_label_button.clicked.connect(self.add_label)
        self.view.delete_label_button.clicked.connect(self.delete_label)
        self.view.select_folder_button.clicked.connect(self.select_images_folder)
        self.view.dataset_checkbox.toggled.connect(self.toggle_dataset_options)
        self.view.start_button.clicked.connect(self.start_processing)
        self.view.import_json_btn.clicked.connect(self.import_json)
        self.view.dataset_folder_btn.clicked.connect(self.select_dataset_folder)

    # Presenter methods
    # These methods handle interactions between the view and model
    def add_label(self):
        """
        Adds a label to the model and updates the view
        :return: None
        """
        label_text = self.view.label_input.text().strip()
        if label_text:
            display_text = self.model.add_label(label_text)
            self.view.labels_list.addItem(display_text)
            self.view.label_input.clear()
            self.enable_start_button()

    def delete_label(self):
        """
        Deletes a label from the model and updates the view
        :return: None
        """
        current_item = self.view.labels_list.currentItem()
        if current_item:
            label_number = int(current_item.text().split(" - ")[0])
            self.model.delete_label(label_number)
            self.view.labels_list.takeItem(self.view.labels_list.row(current_item))
            self.enable_start_button()

    def select_images_folder(self):
        """
        Opens a dialog to select a folder containing images
        :return: None
        """
        folder_name = QFileDialog.getExistingDirectory(self.view, "Select a folder")
        if folder_name:
            self.model.set_images_folder(folder_name)
            self.view.folder_label.setText(folder_name)
            self.enable_start_button()

    def toggle_dataset_options(self, checked):
        """
        Shows or hides the dataset options group
        :param checked: Whether the checkbox is checked
        :return: None
        """
        if checked:
            self.view.dataset_options_group.show()
            self.view.yaml_checkbox.setChecked(True)
        else:
            self.view.dataset_options_group.hide()
            self.view.yaml_checkbox.setChecked(False)
            self.model.dataset_folder_path = ""
            self.view.dataset_folder_btn.setText("Select a folder")

        self.enable_start_button()

    def start_processing(self):
        """
        Starts the processing of images
        :return: None
        """
        image_paths = self.get_validated_image_paths()

        width, height = self.get_resolution()

        train_percentage, val_percentage, test_percentage = self.get_percentages()

        self.create_yaml_file()

        self.image_window_model = ImageWindowModel(
            image_paths, self.model.label_map, (train_percentage, val_percentage, test_percentage),
            self.model.dataset_folder_path)
        self.image_window_view = ImageWindowView((width, height), self.model.label_map)
        self.image_window_presenter = ImageWindowPresenter(self.image_window_view, self.image_window_model)

        self.image_window_presenter.start()
        self.view.close()

    def import_json(self):
        """
        Opens a dialog to select a JSON file containing labels
        :return: None
        """
        file_name = QFileDialog.getOpenFileName(self.view, "Open JSON", "", "JSON Files (*.json);;All Files (*)")[0]
        if file_name:
            self.model.import_json_labels(file_name)
            self.view.labels_list.clear()
            for key, value in self.model.label_map.items():
                self.view.labels_list.addItem(f"{key} - {value}")
            self.enable_start_button()

    def select_dataset_folder(self):
        """
        Opens a dialog to select a folder to save the dataset
        :return: None
        """
        dataset_folder = QFileDialog.getExistingDirectory(self.view, "Select a dataset folder")
        if dataset_folder:
            self.model.set_dataset_folder(dataset_folder)
            self.view.dataset_folder_btn.setText(dataset_folder)
            self.enable_start_button()

    # Helper methods
    def show_error(self, message):
        """
        Shows an error message
        :param message: The message to show
        :return: None
        """
        QMessageBox.critical(self.view, "Error", message)

    def validate_percentage_total(self, train, val, test):
        """
        Validates that the percentages add up to 100
        :param train: Percentage of training images
        :param val: Percentage of validation images
        :param test: Percentage of test images
        :return: True if the percentages add up to 100, False otherwise
        """
        if train + val + test != 100:
            self.show_error("Train, validation, and test percentages must add up to 100.")
            return False
        return True

    def get_validated_image_paths(self):
        """
        Returns a list of paths of images in the images folder
        :return: A list of paths of images in the images folder
        """
        image_paths = self.model.get_image_paths()

        # Check if there are images in the folder
        if not image_paths:
            self.show_error("No images found in the selected folder")
            return

        return image_paths

    def get_resolution(self):
        """
        Returns the resolution of the images
        :return: The resolution of the images
        """
        try:
            width = int(self.view.width_input.text()) if self.view.width_input.text() else 800
            height = int(self.view.height_input.text()) if self.view.height_input.text() else 600
        except ValueError:
            self.show_error("Invalid resolution")
            return
        return width, height

    def get_percentages(self):
        """
        Returns the percentages of training, validation, and test images
        :return: The percentages of training, validation, and test images
        """
        train_percentage = int(
            self.view.train_percentage_input.text()) if self.view.train_percentage_input.text() else 70
        val_percentage = int(self.view.val_percentage_input.text()) if self.view.val_percentage_input.text() else 15
        test_percentage = int(
            self.view.test_percentage_input.text()) if self.view.test_percentage_input.text() else 15

        # Ensure the total is 100
        if not self.validate_percentage_total(train_percentage, val_percentage, test_percentage):
            return

        return train_percentage, val_percentage, test_percentage

    def enable_start_button(self):
        """
        Enables the start button
        :return: None
        """
        if self.model.images_folder_path == "" or self.model.label_map == {}:
            self.view.start_button.setEnabled(False)
        else:
            if self.view.dataset_checkbox.isChecked():
                if self.model.dataset_folder_path == "":
                    self.view.start_button.setEnabled(False)
                else:
                    self.view.start_button.setEnabled(True)
            else:
                self.view.start_button.setEnabled(True)

    def create_yaml_file(self):
        """
        Creates a YAML file in the dataset folder
        :return: None
        """
        if self.view.yaml_checkbox.isChecked():
            if self.model.dataset_folder_path == "":
                self.show_error("Select a dataset folder")
                return

        self.model.create_yaml_file()
