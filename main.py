import sys

from PyQt5.QtWidgets import QApplication, QWidget
from Controllers import MainController
from PyQt5.QtGui import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_controller = MainController()
    main_controller.show()
    sys.exit(app.exec_())
