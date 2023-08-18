# YOLO Data Labeler

Welcome to the YOLO Data Labeler! Created by **Melih Taşkın**, this application offers an intuitive interface for labeling datasets specifically tailored for the YOLO model. It streamlines the process of setting up your YOLO dataset, so you can focus on building and refining your models.

## Features

- **Easy Image Selection**: Just point to your images folder and get started.
- **JSON Label Import**: Import object labels effortlessly using a simple JSON structure. For instance: `{"0": "cat", "1": "dog"}`.
- **Image Resizing**: Need your images in a specific size? Simply provide the width and height, and the app will handle the resizing.
- **Dataset Creation**: Automatically split your data into training, validation, and test sets. Just specify the destination folder and percentages for each set, and you're good to go!

## Getting Started

## Windows Users

### Using the Pre-built Executable:
1. Navigate to the `dist` folder.
2. Double-click on the provided `.exe` file to launch the application.

### Using Python:
1. Ensure you have Python installed on your machine.
2. Navigate to the root directory of the cloned repository.
3. Run the following command:
   
   ```bash
   python main.py

### Unix/Mac Users

#### Using Python:
1. Ensure you have Python installed on your machine.
2. Navigate to the root directory of the cloned repository.
3. Run the following command:
   
    ```bash
    python main.py

#### Building a `.dmg` for MacOS:

1. Ensure you have `py2app` installed. If not, install it using `pip`:
   
    ```bash
    pip install py2app
3. Navigate to the root directory of the cloned repository.
4. Run the following command to create a `.dmg` file:

    ```bash
    python setup.py py2app
6. Once built, navigate to the `dist` directory and you'll find your `.dmg` file. Open it to run the application or move it to your Applications folder.

## Contributions

Feedback, bug reports, and pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the open-source community and the YOLO model creators.
- A very special thank you to **Ahmet Koyuncu** for his invaluable support and contributions to this project.
