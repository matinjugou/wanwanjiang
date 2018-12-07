from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from Items import *
from Maps import *


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

    def release(self):
        pass


class GameScene(QGraphicsScene):
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent=None):
        super(GameScene, self).__init__(parent=parent)
        self.setSceneRect(0, 0, self.parent().width(), self.parent().height())
        self.itemMap = dict()
        self.timer = QTimer()
        self.timer.timeout.connect(self.__timer__clock__)
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.__add_object__)
        self.objectCount = 0
        self.clockCount = 0

        self.map = map1
        self.score = 0

        self.__init_items__()
        self.__start_clock__()

    def __init_items__(self):
        self.backgroundPNG = Background()
        self.backgroundPNG.setPos(0, 0)
        self.addItem(self.backgroundPNG)

        self.wanwanjiang = Wanwanjiang(self)
        self.wanwanjiang.setPos(350, 672)
        self.itemMap['wanwanjiang'] = [self.wanwanjiang, self.wanwanjiang.init_state]
        self.addItem(self.wanwanjiang)

        self.quitgamebutton = QuitGameButton(self.__quit_game__)
        self.quitgamebutton.setPos(690, 10)
        self.addItem(self.quitgamebutton)

        self.scoreText = QGraphicsTextItem()
        self.scoreText.setPos(10, 10)
        self.scoreText.setPlainText("当前得分：%d" % self.score)
        self.addItem(self.scoreText)

    def __start_clock__(self):
        self.timer.start(15)
        self.game_timer.start(1000)

    @pyqtSlot(name="AddObject")
    def __add_object__(self):
        self.clockCount += 1
        try:
            for obj in self.map[str(self.clockCount)]:
                name = "obj" + str(self.objectCount)
                new_obj = FallObject(obj[0], obj[2], obj[3], name, self)
                new_obj.setPos(obj[4] * 700, -10)
                self.itemMap[name] = [new_obj, {"x": obj[4] * 700,
                                                "y": -10,
                                                "speedX": 0,
                                                "speedY": obj[1],
                                                "status": obj[2],
                                                "alive": True
                                                }]
                self.addItem(new_obj)
                self.objectCount += 1
        except Exception as e:
            print(e)

    def keyPressEvent(self, event: QKeyEvent):
        old_state = self.itemMap['wanwanjiang'][1]
        self.wanwanjiang.handle_keypress_event(old_state, event)

    def keyReleaseEvent(self, event: QKeyEvent):
        old_state = self.itemMap['wanwanjiang'][1]
        self.wanwanjiang.handle_keyrelease_event(old_state, event)

    def add_score(self, score):
        self.score += score

    def remove_item(self, name):
        self.removeItem(self.itemMap[name][0])
        self.itemMap[name][1]['alive'] = False

    def __quit_game__(self):
        self.release()
        self.Signal_ChangeModel.emit(1)

    def __update__(self):
        for obj in self.itemMap:
            tuple = self.itemMap[obj]
            tuple[0].self_update(tuple[1])
        newItemMap = dict()
        for obj in self.itemMap:
            if self.itemMap[obj][1]["alive"]:
                newItemMap[obj] = self.itemMap[obj]
        self.itemMap = newItemMap
        self.scoreText.setPlainText("当前得分：%d" % self.score)
        self.__draw__()

    def __draw__(self):
        for obj in self.itemMap:
            tuple = self.itemMap[obj]
            tuple[0].setPos(tuple[1]["x"], tuple[1]["y"])

    @pyqtSlot(name="GameTimeClock")
    def __timer__clock__(self):
        self.__update__()

    def release(self):
        self.timer.stop()
        self.game_timer.stop()
