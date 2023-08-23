import os
from PyQt5.QtWidgets import QApplication, QMessageBox


class ImageWindowPresenter:
    """
    The presenter for the ImageWindowView.
    """
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # Connect view signals to presenter methods
        self.view.next_button.clicked.connect(self.handle_next_image)
        self.view.undo_button.clicked.connect(self.handle_undo_last_rectangle)
        self.view.discard_button.clicked.connect(self.handle_discard_image)

        self.view.rectangle_added.connect(self.on_rectangle_added)
        self.view.rectangle_removed.connect(self.on_rectangle_removed)

    def on_rectangle_added(self, rectangle, label):
        """
        Handles the rectangle_added signal from the view.
        :param rectangle: Rectangle object
        :param label: Label string
        :return: None
        """
        self.model.save_rectangle(rectangle, label)

    def on_rectangle_removed(self):
        """
        Handles the rectangle_removed signal from the view.
        :return: None
        """
        self.model.undo_last_rectangle()

    def handle_next_image(self):
        """
        Handles the next_image signal from the view.
        :return: None
        """
        self.save()

        next_image_path = self.model.get_next_image_path()
        if next_image_path:
            self.view.set_image(next_image_path)
            self.view.rectangles = []
            self.view.check_next_button_status()
            self.view.check_discard_button_status()
        self.create_exit_button()

    def handle_discard_image(self):
        """
        Handles the discard_image signal from the view.
        :return: None
        """
        next_image_path = self.model.get_next_image_path()
        if next_image_path:
            self.view.set_image(next_image_path)
            self.view.rectangles = []
            self.view.check_next_button_status()
            self.view.check_discard_button_status()
        self.create_exit_button()

    def save(self):
        """
        Saves the current image and rectangle calculations.
        :return: None
        """
        if self.model.is_create_dataset():
            self.save_tmp()
        else:
            self.model.create_save_paths()
            self.save_images(os.path.join(self.model.save_path, "scaled_images"))
            self.model.save_calculations(self.model.get_calculations(self.view.image), os.path.join(self.model.save_path, "labels"))

    def handle_undo_last_rectangle(self):
        """
        Handles the undo_last_rectangle signal from the view.
        :return: None
        """
        self.view.remove_last_rectangle()

    def load_initial_image(self):
        """
        Loads the initial image from the model.
        :return: None
        """
        initial_image_path = self.model.get_current_image_path()
        if initial_image_path:
            self.view.set_image(initial_image_path)

    def save_tmp(self):
        """
        Saves the current image and rectangle calculations to a temporary folder.
        :return: None
        """
        tmp_path = self.model.tmp_path
        images_path = os.path.join(tmp_path, "images")
        labels_path = os.path.join(tmp_path, "labels")

        self.model.create_tmp_paths()

        calculations = self.model.get_calculations(self.view.image)

        self.save_images(images_path)
        self.model.save_calculations(calculations, labels_path)

    def create_exit_button(self):
        """
        Creates the exit button if the current image is the last image.
        :return: None
        """
        if self.model.is_last_image():
            self.view.discard_button.setText("Discard and Exit")
            self.view.discard_button.clicked.disconnect()
            self.view.discard_button.clicked.connect(lambda: self.exit_app(True))
        if self.model.is_last_image():
            self.view.next_button.setText("Exit")
            self.view.next_button.clicked.disconnect()
            self.view.next_button.clicked.connect(self.exit_app)

    def save_images(self, path):
        """
        Saves the current image to the given path.
        :param path: Path to save the images
        :return: None
        """
        filename = self.model.get_filename(".jpg")
        filepath = os.path.join(path, filename)

        self.view.image.save(filepath)

    def exit_app(self, discard=False):
        """
        Exits the application with splitting the dataset.
        :return: None
        """
        if not discard:
            self.save()

        if self.model.is_create_dataset():
            tmp_images = self.model.get_tmp_images()
            tmp_labels = self.model.get_tmp_labels()

            x, y = self.model.calculate_percentages()

            train_images, test_images, train_labels, test_labels = self.model.split_dataset(tmp_images, tmp_labels, x)
            if not train_images:
                self.show_error("Your labels are not valid for stratified data splitting. "
                                "You can manually split your data.")
                self.model.move_to_dataset_folder_for_exception(tmp_images, tmp_labels)
            val_images, test_images, val_labels, test_labels = self.model.split_dataset(test_images, test_labels, y)
            if not val_images:
                self.show_error(
                    "Your labels are not valid for stratified data splitting. You can manually split your data.")
                self.model.move_to_dataset_folder_for_exception(tmp_images, tmp_labels)
            else:
                self.model.move_to_dataset_folder(train_images, train_labels, val_images,
                                                  val_labels, test_images, test_labels)
        self.model.clear_temp()
        QApplication.quit()

    def start(self):
        """
        Starts the presenter.
        :return: None
        """
        self.load_initial_image()
        self.view.show()

    def show_error(self, message):
        """
        Shows an error message.
        :param message: Error message
        :return: None
        """
        QMessageBox.critical(self.view, "Error", message)
