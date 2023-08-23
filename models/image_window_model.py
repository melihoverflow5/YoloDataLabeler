import os
import tempfile
from sklearn.model_selection import train_test_split
import shutil


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
        self.tmp_path = tempfile.mkdtemp()

    def get_next_image_path(self):
        """
        Returns the next image path in the list of image paths.
        :return: The path of the next image.
        """
        path = None
        self.current_image_index += 1
        if self.current_image_index <= len(self.image_paths):
            path = self.image_paths[self.current_image_index]
        return path

    def get_current_image_path(self):
        """
        Returns the current image path in the list of image paths.
        :return: The path of the current image.
        """
        return self.image_paths[self.current_image_index]

    def is_last_image(self):
        """
        Returns True if the current image is the last image in the list of image paths.
        :return: True if the current image is the last image in the list of image paths.
        """
        return self.current_image_index >= len(self.image_paths) - 1

    def is_create_dataset(self):
        """
        Returns True if the user has selected to create a dataset.
        :return: True if the user has selected to create a dataset.
        """
        return self.dataset_folder != ""

    def save_rectangle(self, rectangle, label):
        """
        Saves the rectangle and label to the list of rectangles.
        :param rectangle: The rectangle to save.
        :param label: The label to save.
        :return: None
        """
        self.rectangles.append((rectangle, label))

    def undo_last_rectangle(self):
        """
        Removes the last rectangle from the list of rectangles.
        :return: None
        """
        if self.rectangles:
            self.rectangles.pop()

    def get_calculations(self):
        """
        Returns the calculations of the rectangles.
        :return: The calculations of the rectangles.
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
        :param calculations: The calculations to save.
        :param path: The path to save the calculations to.
        :return: None
        """
        filename = self.get_filename(".txt")
        self.clear_data()
        if calculations:
            filepath = os.path.join(path, filename)
            os.makedirs(path, exist_ok=True)
            with open(filepath, "w") as f:
                for calc in calculations:
                    f.write(f"{calc}\n")

    def calculate_percentages(self):
        """
        Calculates the percentages for the train, validation and test sets.
        :return: The percentages for the train, validation and test sets.
        """
        r = 100 - self.percentages[0]

        # Compute the split percentages for the remaining data
        y = self.percentages[2] / r

        # Convert percentages to float representation and return
        return [1 - self.percentages[0] / 100, y]

    def get_filename(self, extension):
        """
        Returns the filename of the current image with the given extension.
        :param extension: The extension to add to the filename.
        :return: The filename of the current image with the given extension.
        """
        filename_without_extension = os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0]
        filename = filename_without_extension + extension
        return filename

    def create_save_paths(self):
        """
        Creates the save paths for the images and labels.
        :return: None
        """
        images_path = os.path.join(self.save_path, "scaled_images")
        labels_path = os.path.join(self.save_path, "labels")
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)

    def create_tmp_paths(self):
        """
        Creates the temporary paths for the images and labels.
        :return: None
        """
        tmp_path = self.tmp_path
        images_path = os.path.join(tmp_path, "images")
        labels_path = os.path.join(tmp_path, "labels")
        os.makedirs(tmp_path, exist_ok=True)
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)

    def create_dataset_paths(self):
        """
        Creates the dataset paths for the images and labels.
        :return: Returns the dataset paths for the images and labels.
        """
        train_images_dir = os.path.join(self.dataset_folder, "train", "images")
        train_labels_dir = os.path.join(self.dataset_folder, "train", "labels")
        val_images_dir = os.path.join(self.dataset_folder, "val", "images")
        val_labels_dir = os.path.join(self.dataset_folder, "val", "labels")
        test_images_dir = os.path.join(self.dataset_folder, "test", "images")
        test_labels_dir = os.path.join(self.dataset_folder, "test", "labels")

        os.makedirs(train_images_dir, exist_ok=True)
        os.makedirs(train_labels_dir, exist_ok=True)
        os.makedirs(val_images_dir, exist_ok=True)
        os.makedirs(val_labels_dir, exist_ok=True)
        os.makedirs(test_images_dir, exist_ok=True)
        os.makedirs(test_labels_dir, exist_ok=True)

        return train_images_dir, train_labels_dir, val_images_dir, val_labels_dir, test_images_dir, test_labels_dir

    def move_to_dataset_folder_for_exception(self, tmp_images, tmp_labels):
        """
        Moves the images and labels to the dataset folder.
        :param tmp_images: The temporary images.
        :param tmp_labels: The temporary labels.
        :return: None
        """
        images_folder = os.path.join(self.dataset_folder, "images")
        labels_folder = os.path.join(self.dataset_folder, "labels")
        self.move_files(tmp_images, images_folder)
        self.move_files(tmp_labels, labels_folder)

    def get_tmp_labels(self):
        """
        Returns the temporary label files.
        :return: The temporary label files.
        """
        label_dir = os.path.join(self.tmp_path, "labels")
        label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
        label_files = [os.path.join(label_dir, f) for f in label_files]
        return label_files

    def get_tmp_images(self):
        """
        Returns the temporary image files.
        :return: The temporary image files.
        """
        image_dir = os.path.join(self.tmp_path, "images")
        images = [f for f in os.listdir(image_dir)]
        images = [os.path.join(image_dir, f) for f in images]
        return images

    def split_dataset(self, image_files, label_files, percentage):
        """
        Splits the dataset into train, validation and test sets.
        :param image_files: The image files.
        :param label_files: The label files.
        :param percentage: The percentage to split the test data.
        :return: The train images, test images, train labels and test labels.
        """
        global_label_counts = {}

        for lbl_file in label_files:
            seen_labels_in_file = set()  # To store unique labels for this specific file

            with open(lbl_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    lbl = int(line.split()[0])
                    seen_labels_in_file.add(lbl)

            # Add the unique labels from this file to the global count
            for unique_lbl in seen_labels_in_file:
                global_label_counts[unique_lbl] = global_label_counts.get(unique_lbl, 0) + 1

        labels_appearing_once = [label for label, count in global_label_counts.items() if count == 1]
        if labels_appearing_once:
            print(f"The following labels appear only once: {labels_appearing_once}")
            return None, None, None, None

        # Assign single label to multilabel images based on least frequent label
        single_labels = []
        for lbl_file in label_files:
            with open(lbl_file, 'r') as f:
                labels = set(int(line.split()[0]) for line in f.readlines())

                if len(labels) > 1:
                    # If it's multilabel, assign the least frequent label among its labels
                    least_common_label = min(labels, key=lambda label_count: global_label_counts.get(label_count, 0))
                    single_labels.append(least_common_label)
                else:
                    # If it's a single label, just append it
                    single_labels.append(list(labels)[0])

        # Split dataset using the new single labels
        train_images, test_images, train_labels, test_labels = train_test_split(
            image_files, label_files, random_state=42, test_size=percentage, shuffle=True, stratify=single_labels)

        return train_images, test_images, train_labels, test_labels

    def move_files(self, files, destination_folder):
        """
        Moves the files to the destination folder.
        :param files: The files to move.
        :param destination_folder: The destination folder to move the files to.
        :return: None
        """
        os.makedirs(destination_folder, exist_ok=True)
        for file in files:
            shutil.move(file, destination_folder)

    def move_to_dataset_folder(self, train_images, train_labels, val_images, val_labels, test_images, test_labels):
        """
        Moves the images and labels to the dataset folder.
        :param train_images: The train images.
        :param train_labels: The train labels.
        :param val_images: The validation images.
        :param val_labels: The validation labels.
        :param test_images: The test images.
        :param test_labels: The test labels.
        :return: None
        """
        train_images_dir, train_labels_dir, val_images_dir, val_labels_dir, \
            test_images_dir, test_labels_dir = self.create_dataset_paths()
        # Create a list of pairs of files and their destination directories
        datasets = [
            (train_images, train_images_dir),
            (train_labels, train_labels_dir),
            (val_images, val_images_dir),
            (val_labels, val_labels_dir),
            (test_images, test_images_dir),
            (test_labels, test_labels_dir)
        ]

        # Loop through the pairs to move files
        for files, dest_dir in datasets:
            self.move_files(files, dest_dir)

    def clear_temp(self):
        """
        Clears the temp files.
        :return: None
        """
        shutil.rmtree(self.tmp_path)

    def clear_data(self):
        """
        Clears the rectangles.
        :return: None
        """
        self.rectangles = []
