# YOLO Data Labeler

Welcome to the YOLO Data Labeler! Created by **Melih Taşkın**, this application offers an intuitive interface for labeling datasets specifically tailored for the YOLO model. It streamlines the process of setting up your YOLO dataset, so you can focus on building and refining your models.

## Features

- **Easy Image Selection**: Just point to your images folder and get started.
- **JSON Label Import**: Import object labels effortlessly using a simple JSON structure. For instance:
  ```json
  {
     "0": "cat",
     "1": "dog"
  }
- **Image Resizing**: Need your images in a specific size? Simply provide the width and height, and the app will handle the resizing.
- **Dataset Creation**: Automatically split your data into training, validation, and test sets. Just specify the destination folder and percentages for each set, and you're good to go!

## 🛡️ Data Privacy & Security

One of the distinct advantages of using this Data Labeler is that all labeling operations are **entirely local**. Unlike many online data labeling platforms, which may store, reuse, or even share your data, our tool ensures:

1. **No Data Uploads**: Your data never leaves your machine.
2. **Full User Control**: You have complete control over your labeled data, ensuring it remains confidential and proprietary.
3. **No Hidden Agendas**: We don't have backend processes that process or store your data. Your intellectual property remains solely yours.

By prioritizing local processing, our tool provides both the convenience of an intuitive labeling interface and the peace of mind that comes with top-notch data privacy and security.

## Getting Started

### Windows Users

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
