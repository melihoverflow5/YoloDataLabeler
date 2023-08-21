import os
import tempfile


class ImageWindowModel:
    """
    This class is responsible for storing the data and logic of the image window.
    """
    def __init__(self, image_paths, label_map=None, percentages=None, dataset_folder=None):
        self.image_paths = image_paths
        self.current_image_index = 0
        self.label_map = label_map if label_map else {}
        self.percentages = percentages
        self.dataset_folder = dataset_folder
        self.rectangles = []
        self.save_path = os.path.dirname(os.path.dirname(self.get_current_image_path()))
        self.tmp_path = os.path.join(os.path.dirname(self.get_current_image_path()), "tmp")

    def get_next_image_path(self):
        """
        Returns the next image path in the list of image paths.
        :return:
        """
        self.current_image_index += 1
        return self.image_paths[self.current_image_index]

    def get_current_image_path(self):
        """
        Returns the current image path in the list of image paths.
        :return:
        """
        return self.image_paths[self.current_image_index]

    def is_last_image(self):
        """
        Returns True if the current image is the last image in the list of image paths.
        :return:
        """
        return self.current_image_index >= len(self.image_paths) - 1

    def is_create_dataset(self):
        """
        Returns True if the user has selected to create a dataset.
        :return:
        """
        return self.dataset_folder != ""

    def save_rectangle(self, rectangle, label):
        """
        Saves the rectangle and label to the list of rectangles.
        :param rectangle:
        :param label:
        :return:
        """
        self.rectangles.append((rectangle, label))

    def undo_last_rectangle(self):
        """
        Removes the last rectangle from the list of rectangles.
        :return:
        """
        if self.rectangles:
            self.rectangles.pop()

    def get_calculations(self):
        """
        Returns a list of calculations for each rectangle.
        :return:
        """
        outputs = []
        for rectangle, label in self.rectangles:
            x_center = ((rectangle.topLeft().x() + rectangle.bottomRight().x()) / 2)
            y_center = ((rectangle.topLeft().y() + rectangle.bottomRight().y()) / 2)
            width = (rectangle.bottomRight().x() - rectangle.topLeft().x())
            height = (rectangle.bottomRight().y() - rectangle.topLeft().y())

            output = f"{label} {x_center} {y_center} {width} {height}"
            outputs.append(output)

        return outputs

    def save_calculations(self, calculations, path):
        """
        Saves the calculations to a text file.
        :param calculations:
        :param path:
        :return:
        """
        filename = self.get_filename(".txt")
        self.clear_data()
        if calculations:
            filepath = os.path.join(path, filename)
            os.makedirs(path, exist_ok=True)
            with open(filepath, "w") as f:
                for calc in calculations:
                    f.write(f"{calc}\n")

    def get_filename(self, extension):
        """
        Returns the filename of the current image with the given extension.
        :param extension:
        :return:
        """
        filename_without_extension = os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0]
        filename = filename_without_extension + extension
        return filename

    def create_save_paths(self):
        """
        Creates the save paths for the images and labels.
        :return:
        """
        images_path = os.path.join(self.save_path, "scaled_images")
        labels_path = os.path.join(self.save_path, "labels")
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)

    def create_tmp_paths(self):
        """
        Creates the temporary paths for the images and labels.
        :return:
        """
        tmp_path = self.tmp_path
        images_path = os.path.join(tmp_path, "images")
        labels_path = os.path.join(tmp_path, "labels")
        os.makedirs(tmp_path, exist_ok=True)
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)

    def clear_data(self):
        """
        Clears the rectangles.
        :return:
        """
        self.rectangles = []
