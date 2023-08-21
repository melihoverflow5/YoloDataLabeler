import os

from PyQt5.QtWidgets import QApplication


class ImageWindowPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # Connect view signals to presenter methods
        self.view.next_button.clicked.connect(self.handle_next_image)
        self.view.undo_button.clicked.connect(self.handle_undo_last_rectangle)

        self.view.rectangle_added.connect(self.on_rectangle_added)
        self.view.rectangle_removed.connect(self.on_rectangle_removed)

    def on_rectangle_added(self, rectangle, label):
        self.model.save_rectangle(rectangle, label)

    def on_rectangle_removed(self):
        self.model.undo_last_rectangle()

    def handle_next_image(self):
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
        if self.model.is_create_dataset():
            self.save_tmp()
        else:
            self.model.create_save_paths()
            self.save_images(os.path.join(self.model.save_path, "scaled_images"))
            self.model.save_calculations(self.model.get_calculations(), os.path.join(self.model.save_path, "labels"))

    def handle_undo_last_rectangle(self):
        self.view.remove_last_rectangle()

    def load_initial_image(self):
        initial_image_path = self.model.get_current_image_path()
        if initial_image_path:
            self.view.set_image(initial_image_path)

    def save_tmp(self):
        tmp_path = self.model.tmp_path
        images_path = os.path.join(tmp_path, "images")
        labels_path = os.path.join(tmp_path, "labels")

        self.model.create_tmp_paths()

        calculations = self.model.get_calculations()

        self.save_images(images_path)
        self.model.save_calculations(calculations, labels_path)

    def save_images(self, path):
        filename = self.model.get_filename(".jpg")
        filepath = os.path.join(path, filename)

        self.view.image.save(filepath)

    def exit_app(self):
        self.save()
        QApplication.quit()

    def start(self):
        # Load the initial image and start the view
        self.load_initial_image()
        self.view.show()