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
        self.background = QGraphicsPixmapItem(QPixmap("resources//pic//startbg.png"))
        self.background.setPos(0, 0)
        self.addItem(self.background)

        self.Wanwanjiang = NormalWanwanjiang()
        self.Wanwanjiang.setPos(self.width() / 2, self.height() / 2 - 100)
        self.addItem(self.Wanwanjiang)

        self.startGameButton = StartGameButton(self.__start_game__)
        self.startGameButton.setPos(self.width() / 2, self.height() / 2 + 100)
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
        self.zCount = 0

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

        fid = QFontDatabase.addApplicationFont("resources//font//youyuan.ttf")
        fontFamilies = QFontDatabase.applicationFontFamilies(fid)
        new_font = QFont()
        new_font.setFamily(fontFamilies[0])
        new_font.setPixelSize(14)

        self.scoreText = QGraphicsTextItem()
        self.scoreText.setPos(10, 10)
        self.scoreText.setPlainText("当前得分：%d" % self.score)
        self.scoreText.setFont(new_font)
        self.addItem(self.scoreText)

        self.statusText = QGraphicsTextItem()
        self.statusText.setPos(10, 25)
        self.statusText.setPlainText("当前状态：正常")
        self.statusText.setFont(new_font)
        self.addItem(self.statusText)

        self.zCountText = QGraphicsTextItem()
        self.zCountText.setPos(10, 40)
        self.zCountText.setPlainText("捕获庄周数：%d" % self.zCount)
        self.zCountText.setFont(new_font)
        self.addItem(self.zCountText)

        self.countDownText = QGraphicsTextItem()
        self.countDownText.setPos(10, 55)
        self.countDownText.setPlainText("剩余时间：%d" % (32 - self.clockCount))
        self.countDownText.setFont(new_font)
        self.addItem(self.countDownText)

    def __start_clock__(self):
        self.timer.start(15)
        self.game_timer.start(1000)

    @pyqtSlot(name="AddObject")
    def __add_object__(self):
        self.clockCount += 1
        if self.clockCount == 32:
            self.__quit_game__()
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
        if score == 20:
            self.zCount += 1

    def remove_item(self, name):
        self.removeItem(self.itemMap[name][0])
        self.itemMap[name][1]['alive'] = False

    def __quit_game__(self):
        self.release()
        if self.clockCount < 32:
            self.Signal_ChangeModel.emit(1)
        elif self.score >= 200 and self.zCount == 7:
            self.Signal_ChangeModel.emit(4)
        else:
            self.Signal_ChangeModel.emit(3)

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
        self.countDownText.setPlainText("剩余时间：%d" % (32 - self.clockCount))
        if self.itemMap['wanwanjiang'][1]["status"] == "normal":
            self.statusText.setPlainText("当前状态：正常")
        elif self.itemMap['wanwanjiang'][1]["status"] == "bonus":
            self.statusText.setPlainText("当前状态：兴奋！！")
        elif self.itemMap['wanwanjiang'][1]["status"] == "weak":
            self.statusText.setPlainText("当前状态：虚弱……")
        self.zCountText.setPlainText("捕获庄周数：%d" % self.zCount)
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


class EndSceneFail(QGraphicsScene):
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent=None):
        super(EndSceneFail, self).__init__(parent=parent)
        self.setSceneRect(0, 0, self.parent().width(), self.parent().height())
        self.itemMap = dict()
        self.__init_items__()

    def __init_items__(self):
        self.background = QGraphicsPixmapItem(QPixmap("resources//pic//failbg.png"))
        self.background.setPos(0, 0)
        self.addItem(self.background)

        self.sadWanwanjiang = SadWanwanjiang()
        self.sadWanwanjiang.setPos(self.width() / 2, self.height() / 2 - 100)
        self.addItem(self.sadWanwanjiang)

        self.sadText = QGraphicsPixmapItem(QPixmap("resources//pic/fail_text.png"))
        self.sadText.setPos(80, 400)
        self.addItem(self.sadText)

        self.confirmButton = ConfirmButton(self.__confirm__)
        self.confirmButton.setPos(self.width() / 2, self.height() / 2 + 200)
        self.addItem(self.confirmButton)

    def __confirm__(self):
        self.Signal_ChangeModel.emit(1)

    def release(self):
        pass


class EndSceneSuccess(QGraphicsScene):
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent=None):
        super(EndSceneSuccess, self).__init__(parent=parent)
        self.setSceneRect(0, 0, self.parent().width(), self.parent().height())
        self.itemMap = dict()
        self.__init_items__()

    def __init_items__(self):
        self.background = QGraphicsPixmapItem(QPixmap("resources//pic//winbg.png"))
        self.background.setPos(0, 0)
        self.addItem(self.background)

        self.happyWanwanjiang = HappyWanwanjiang()
        self.happyWanwanjiang.setPos(self.width() / 2, self.height() / 2 - 100)
        self.addItem(self.happyWanwanjiang)

        self.winText = QGraphicsPixmapItem(QPixmap("resources//pic/win_text.png"))
        self.winText.setPos(80, 400)
        self.addItem(self.winText)

        fid = QFontDatabase.addApplicationFont("resources//font//youyuan.ttf")
        fontFamilies = QFontDatabase.applicationFontFamilies(fid)
        new_font = QFont()
        new_font.setFamily(fontFamilies[0])
        new_font.setPixelSize(14)

        self.urlText = QGraphicsTextItem()
        self.urlText.setPos(200, 600)
        self.urlText.setPlainText("惊喜：https://shimo.im/docs/bbHma4SWYyE4MfeJ/")
        self.urlText.setFont(new_font)
        self.addItem(self.urlText)

        self.confirmButton = ConfirmButton(self.__confirm__)
        self.confirmButton.setPos(self.width() / 2, self.height() / 2 + 200)
        self.addItem(self.confirmButton)

    def __confirm__(self):
        self.Signal_ChangeModel.emit(1)

    def release(self):
        pass
