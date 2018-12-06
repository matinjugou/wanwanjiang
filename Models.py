from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from Items import *


class StartScene(QGraphicsScene):
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent=None):
        super(StartScene, self).__init__(parent=parent)
        self.setSceneRect(0, 0, self.parent().width(), self.parent().height())
        self.itemMap = dict()
        self.__init_items__()

    def __init_items__(self):
        self.startGameButton = StartGameButton(self.__start_game__)
        self.startGameButton.setPos(self.width() / 2, self.height() / 2)
        self.addItem(self.startGameButton)

    def __start_game__(self):
        self.Signal_ChangeModel.emit(2)


class GameScene(QGraphicsScene):
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent=None):
        super(GameScene, self).__init__(parent=parent)
        self.setSceneRect(0, 0, self.parent().width(), self.parent().height())
        self.itemMap = dict()
        self.__init_items__()
        self.timer = QTimer()
        self.timer.start(15)
        self.timer.timeout.connect(self.__timer__clock__)

    def __init_items__(self):
        self.wanwanjiang = Wanwanjiang()
        self.wanwanjiang.setPos(350, 672)
        self.itemMap['wanwanjiang'] = [self.wanwanjiang, self.wanwanjiang.init_state]
        self.addItem(self.wanwanjiang)

        self.quitgamebutton = QuitGameButton(self.__quit_game__)
        self.quitgamebutton.setPos(690, 10)
        self.addItem(self.quitgamebutton)

    def keyPressEvent(self, event: QKeyEvent):
        old_state = self.itemMap['wanwanjiang'][1]
        self.wanwanjiang.handle_keypress_event(old_state, event)

    def keyReleaseEvent(self, event: QKeyEvent):
        old_state = self.itemMap['wanwanjiang'][1]
        self.wanwanjiang.handle_keyrelease_event(old_state, event)

    def __quit_game__(self):
        self.Signal_ChangeModel.emit(1)

    def __update__(self):
        for obj in self.itemMap:
            tuple = self.itemMap[obj]
            tuple[1]["x"] += tuple[1]["speedX"]
            tuple[1]["y"] += tuple[1]["speedY"]
        self.__draw__()

    def __draw__(self):
        for obj in self.itemMap:
            tuple = self.itemMap[obj]
            tuple[0].setPos(tuple[1]["x"], tuple[1]["y"])

    @pyqtSlot(name="GameTimeClock")
    def __timer__clock__(self):
        self.__update__()
