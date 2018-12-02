from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from Items import *


class StartMenu(QGraphicsScene):
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent=None):
        super(StartMenu, self).__init__(parent=parent)
        self.setSceneRect(0, 0, self.parent().width(), self.parent().height())
        self.itemMap = dict()
        self.__init__items__()
        self.timer = QTimer()
        self.timer.start(10)
        self.timer.timeout.connect(self.__timer__clock__)

        self.playerSpeed = 10

    def __init__items__(self):
        self.wanwanjiang = Wanwanjiang()
        self.wanwanjiang.setPos(350, 672)
        self.itemMap['wanwanjiang'] = [self.wanwanjiang, 350, 672, 0, 0]
        self.addItem(self.wanwanjiang)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Left:
            self.itemMap['wanwanjiang'][3] = -1 * self.playerSpeed
        elif event.key() == Qt.Key_Right:
            self.itemMap['wanwanjiang'][3] = self.playerSpeed
        elif event.key() == Qt.Key_Up:
            self.playerSpeed += 1
        elif event.key() == Qt.Key_Down:
            self.playerSpeed = abs(self.playerSpeed - 1)

    def keyReleaseEvent(self, event: QKeyEvent):
        print("Key Release")
        self.itemMap['wanwanjiang'][3] = 0

    @pyqtSlot()
    def __timer__clock__(self):
        for obj in self.itemMap:
            tuple = self.itemMap[obj]
            tuple[1] += tuple[3]
            tuple[2] += tuple[4]
            tuple[0].setPos(tuple[1], tuple[2])
