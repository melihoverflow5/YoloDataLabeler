import sys
from PyQt5.QtWidgets import QApplication
from models.setup_model import SetupModel
from presenters.setup_presenter import SetupPresenter
from views.setup_view import SetupView
import qtmodern.styles
import qtmodern.windows


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)

    model = SetupModel()
    view = SetupView()
    presenter = SetupPresenter(view, model)

    view.setWindowTitle("YOLO DATA LABELER BY MELIH TASKIN")
    view.show()

    setup_presenter_modern = qtmodern.windows.ModernWindow(view)
    setup_presenter_modern.show()

    sys.exit(app.exec_())
