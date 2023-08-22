from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, pyqtSignal


class ImageWindowView(QWidget):
    rectangle_added = pyqtSignal(object, int)
    rectangle_removed = pyqtSignal()

    def __init__(self, resolution=(800, 600), label_map=None):
        super().__init__()

        # Define the maximum display size
        self.display_size = resolution
        self.image = QPixmap(self.display_size[0], self.display_size[1])  # Placeholder for image
        self.rectangles = []
        self.label_map = label_map if label_map else {}

        # Drawing attributes
        self.startPoint = None
        self.endPoint = None
        self.isDrawing = False

        # Add Next button
        self.next_button = QPushButton("Next Image", self)

        # Add Discard button
        self.discard_button = QPushButton("Discard Image", self)

        # Add Undo button
        self.undo_button = QPushButton("Undo", self)

        # Add ComboBox
        self.comboBox = QComboBox(self)
        for key, value in self.label_map.items():
            self.comboBox.addItem(value, userData=key)

        self.checkNextButtonStatus()
        self.checkDiscardButtonStatus()
        self.update_ui()

    def update_ui(self):
        """
        Updates the UI.
        :return:
        """
        self.adjust_window_size()
        self.position_elements()

    def adjust_window_size(self):
        """
        Adjusts the window size to fit the image.
        :return:
        """
        self.setFixedSize(self.image.size().width(), self.image.size().height() + 40)

    def position_elements(self):
        """
        Positions the elements in the window.
        :return:
        """
        self.next_button.resize(100, 30)
        self.next_button.move(self.image.width() - 110, self.image.height() + 5)

        self.discard_button.resize(100, 30)
        self.discard_button.move(self.image.width() - 220, self.image.height() + 5)

        self.undo_button.resize(100, 30)
        self.undo_button.move(125, self.image.height() + 5)

        self.comboBox.resize(100, 30)
        self.comboBox.move(15, self.image.height() + 5)

    def load_and_scale_image(self, path):
        """
        Loads and scales the image to fit the display size.
        :param path:
        :return:
        """
        pixmap = QPixmap(path)
        scaled_pixmap = pixmap.scaled(self.display_size[0], self.display_size[1])
        return scaled_pixmap

    def set_image(self, path):
        """
        Sets the image to be displayed.
        :param path:
        :return:
        """
        self.image = self.load_and_scale_image(path)
        self.update_ui()
        self.update()

    def add_rectangle(self, rectangle, label):
        """
        Adds a rectangle to the list of rectangles.
        :param rectangle:
        :param label:
        :return:
        """
        self.rectangle_added.emit(rectangle, self.comboBox.itemData(self.comboBox.currentIndex()))
        self.rectangles.append((rectangle, label))
        self.checkNextButtonStatus()
        self.checkDiscardButtonStatus()
        self.update()

    def remove_last_rectangle(self):
        """
        Removes the last rectangle from the list of rectangles.
        :return:
        """
        self.rectangle_removed.emit()
        if self.rectangles:
            self.rectangles.pop()

            # Reset the temporary drawing points
            self.startPoint = None
            self.endPoint = None
            self.checkNextButtonStatus()
            self.checkDiscardButtonStatus()
            self.update()

    def paintEvent(self, event):
        """
        Paints the image and rectangles.
        :param event:
        :return:
        """
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image)

        for rectangle, label in self.rectangles:
            pen = QPen(Qt.red, 3, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(rectangle)
            painter.drawText(rectangle.center(), label)

        if self.startPoint and self.endPoint:
            pen = QPen(Qt.red, 3, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(QRect(self.startPoint, self.endPoint))
        painter.end()

    def mousePressEvent(self, event):
        """
        Handles the mousePressEvent.
        :param event:
        :return:
        """
        if event.button() == Qt.LeftButton and self.is_within_image_bounds(event.pos()):
            self.startPoint = event.pos()
            self.endPoint = event.pos()
            self.isDrawing = True
            self.update()

    def mouseMoveEvent(self, event):
        """
        Handles the mouseMoveEvent.
        :param event:
        :return:
        """
        if self.isDrawing and self.is_within_image_bounds(event.pos()):
            self.endPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """
        Handles the mouseReleaseEvent.
        :param event:
        :return:
        """
        if self.isDrawing:
            self.endPoint = event.pos()
            self.isDrawing = False
            if self.startPoint != self.endPoint:
                current_label = self.comboBox.currentText()
                self.add_rectangle(QRect(self.startPoint, self.endPoint), current_label)
            self.startPoint = None
            self.endPoint = None

    def checkNextButtonStatus(self):
        """
        Checks the status of the next button.
        :return:
        """
        if self.rectangles:
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

    def checkDiscardButtonStatus(self):
        """
        Checks the status of the next button.
        :return:
        """
        if self.rectangles:
            self.discard_button.setEnabled(False)
        else:
            self.discard_button.setEnabled(True)

    def is_within_image_bounds(self, point):
        """
        Returns True if the point is within the image bounds.
        :param point:
        :return:
        """
        return QRect(0, 0, self.image.width(), self.image.height()).contains(point)
