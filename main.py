import sys

from PyQt5.QtWidgets import QApplication, QWidget
from Controllers import MainController
from PyQt5.QtGui import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fid = QFontDatabase.addApplicationFont("resources//font//youyuan.ttf")
    fontFamilies = QFontDatabase.applicationFontFamilies(fid)
    if list(fontFamilies).__len__() > 0:
        fontName = fontFamilies[0]
        font = QFont(fontName)
        app.setFont(font)
    main_controller = MainController()
    main_controller.show()
    sys.exit(app.exec_())
