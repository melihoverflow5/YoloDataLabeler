import os
import tempfile


class ImageWindowModel:
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
        self.current_image_index += 1
        return self.image_paths[self.current_image_index]

    def get_current_image_path(self):
        return self.image_paths[self.current_image_index]

    def is_last_image(self):
        return self.current_image_index >= len(self.image_paths) - 1

    def is_last_two_images(self):
        return self.current_image_index >= len(self.image_paths) - 2

    def is_create_dataset(self):
        return self.dataset_folder != ""

    def save_rectangle(self, rectangle, label):
        self.rectangles.append((rectangle, label))

    def undo_last_rectangle(self):
        if self.rectangles:
            self.rectangles.pop()

    def get_calculations(self):
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
        filename = self.get_filename(".txt")
        self.clear_data()
        if calculations != []:
            filepath = os.path.join(path, filename)
            os.makedirs(path, exist_ok=True)
            with open(filepath, "w") as f:
                for calc in calculations:
                    f.write(f"{calc}\n")

    def get_filename(self, extension):
        filename_without_extension = os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0]
        filename = filename_without_extension + extension
        return filename

    def create_save_paths(self):
        images_path = os.path.join(self.save_path, "scaled_images")
        labels_path = os.path.join(self.save_path, "labels")
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)

    def create_tmp_paths(self):
        tmp_path = self.tmp_path
        images_path = os.path.join(tmp_path, "images")
        labels_path = os.path.join(tmp_path, "labels")
        os.makedirs(tmp_path, exist_ok=True)
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)
    def clear_data(self):
        self.rectangles = []
