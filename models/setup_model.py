import os
import json


class SetupModel:

    def __init__(self):
        # Dictionary to store integer labels and their descriptions
        self.label_map = {}
        self.next_label = 0
        self.images_folder_path = ""
        self.dataset_folder_path = ""

    def add_label(self, description):
        """
        Adds a label to the model and returns the display text to be added to the list widget
        :param description:
        :return:
        """
        self.label_map[str(self.next_label)] = description if description else str(self.next_label)
        display_text = f"{self.next_label} - {description}" if description else str(self.next_label)
        self.next_label += 1

        return display_text  # Return the display text to be added to the list widget

    def delete_label(self, label_number):
        """
        Deletes a label from the model
        :param label_number:
        :return:
        """
        if label_number in self.label_map:
            del self.label_map[label_number]

    def import_json_labels(self, file_path):
        """
        Imports labels from a JSON file
        :param file_path:
        :return:
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.label_map.clear()
            highest_key = -1
            for key, value in data.items():
                int_key = int(key)
                if int_key > highest_key:
                    highest_key = int_key
                # Check if the label key already exists
                if int_key not in self.label_map:
                    # Add the label to label_map
                    self.label_map[int_key] = value

            # Set the next_label to be one more than the highest key found
            self.next_label = highest_key + 1

    def set_images_folder(self, folder):
        """
        Sets the path of the folder containing images
        :param folder:
        :return:
        """
        self.images_folder_path = folder

    def get_image_paths(self):
        """
        Returns a list of paths of images in the images folder
        :return:
        """
        return [self.images_folder_path + '/' +
                f for f in os.listdir(self.images_folder_path) if f.endswith(('.jpg', '.png'))]

    def set_dataset_folder(self, folder):
        """
        Sets the path of the folder containing images
        :param folder:
        :return:
        """
        self.dataset_folder_path = folder

    def create_yaml_file(self):
        """
        Creates a YAML file in the dataset folder
        :return:
        """
        yaml_file_path = os.path.join(self.dataset_folder_path, 'dataset.yaml')
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

    # Additional methods to get, set or manipulate data can be added here
