import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import *
import PyQt5.Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        self.setWindowTitle(u'测试')
        self.show()

    # 检测键盘回车按键
    def keyPressEvent(self, event):
        print("press:" + str(event.key()))
        # 举例
        if (event.key() == Qt.Key_Escape):
            print('test: ESC')
        if (event.key() == Qt.Key_A):
            print('test:A')
        if (event.key() == Qt.Key_1):
            print('test: 1')
        if (event.key() == Qt.Key_Enter):
            print(u'测试：Enter')
        if (event.key() == Qt.Key_Space):
            print(u'测试：Space')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(u"鼠标左键点击")
        elif event.button() == Qt.RightButton:
            print(u"鼠标右键点击")
        elif event.button() == Qt.MidButton:
            print(u"鼠标中键点击")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
