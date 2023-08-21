import os

from PyQt5.QtWidgets import QApplication


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

        self.view.rectangle_added.connect(self.on_rectangle_added)
        self.view.rectangle_removed.connect(self.on_rectangle_removed)

    def on_rectangle_added(self, rectangle, label):
        """
        Handles the rectangle_added signal from the view.
        :param rectangle:
        :param label:
        :return:
        """
        self.model.save_rectangle(rectangle, label)

    def on_rectangle_removed(self):
        """
        Handles the rectangle_removed signal from the view.
        :return:
        """
        self.model.undo_last_rectangle()

    def handle_next_image(self):
        """
        Handles the next_image signal from the view.
        :return:
        """
        self.save()

        next_image_path = self.model.get_next_image_path()
        if next_image_path:
            self.view.set_image(next_image_path)
            self.view.rectangles = []

        if self.model.is_last_image():
            self.view.next_button.setText("Exit")
            self.view.next_button.clicked.disconnect(self.handle_next_image)
            self.view.next_button.clicked.connect(self.exit_app)

    def save(self):
        """
        Saves the current image and rectangle calculations.
        :return:
        """
        if self.model.is_create_dataset():
            self.save_tmp()
        else:
            self.model.create_save_paths()
            self.save_images(os.path.join(self.model.save_path, "scaled_images"))
            self.model.save_calculations(self.model.get_calculations(), os.path.join(self.model.save_path, "labels"))

    def handle_undo_last_rectangle(self):
        """
        Handles the undo_last_rectangle signal from the view.
        :return:
        """
        self.view.remove_last_rectangle()

    def load_initial_image(self):
        """
        Loads the initial image from the model.
        :return:
        """
        initial_image_path = self.model.get_current_image_path()
        if initial_image_path:
            self.view.set_image(initial_image_path)

    def save_tmp(self):
        """
        Saves the current image and rectangle calculations to a temporary folder.
        :return:
        """
        tmp_path = self.model.tmp_path
        images_path = os.path.join(tmp_path, "images")
        labels_path = os.path.join(tmp_path, "labels")

        self.model.create_tmp_paths()

        calculations = self.model.get_calculations()

        self.save_images(images_path)
        self.model.save_calculations(calculations, labels_path)

    def save_images(self, path):
        """
        Saves the current image to the given path.
        :param path:
        :return:
        """
        filename = self.model.get_filename(".jpg")
        filepath = os.path.join(path, filename)

        self.view.image.save(filepath)

    def exit_app(self):
        """
        Exits the application.
        :return:
        """
        self.save()
        QApplication.quit()

    def start(self):
        """
        Starts the presenter.
        :return:
        """
        self.load_initial_image()
        self.view.show()
