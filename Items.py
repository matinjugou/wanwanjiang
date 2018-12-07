from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Wanwanjiang(QGraphicsPixmapItem):
    def __init__(self, parent):
        super(Wanwanjiang, self).__init__()
        print(parent)
        self.__picture__ = dict()
        self.__picture__["normal"] = QPixmap("resources//pic//wanwanjiang.png")
        self.__picture__["bonus"] = QPixmap("resources//pic//wanwanjiang_bonus.png")
        self.__picture__["weak"] = QPixmap("resources//pic//wanwanjiang_weak.png")
        self.setPixmap(self.__picture__["normal"])
        self.setOffset(QPointF(-1 * self.__picture__["normal"].width() / 2,
                               -1 * self.__picture__["normal"].height() + 5))

        self.behaviorMap = {"normal": self.normal_behavior,
                            "weak": self.weak_behavior,
                            "bonus": self.bonus_behavior}

        self.init_state = {"x": 700 / 2,
                           "y": 672,
                           "speedX": 0,
                           "speedY": 0,
                           "status": "normal",
                           "alive": True
                           }
        self.scene_parent = parent
        self.collidCount = 0

    def handle_keypress_event(self, state, event):
        self.behaviorMap[state["status"]](state, event)

    def self_update(self, state):
        state["x"] += state["speedX"]
        state["y"] += state["speedY"]
        if state["x"] < (self.__picture__["normal"].width() / 2):
            state["x"] = self.__picture__["normal"].width() / 2
        if state["x"] > (700 - self.__picture__["normal"].width() / 2):
            state["x"] = 700 - self.__picture__["normal"].width() / 2
        objlist = self.collidingItems()
        for obj in objlist:
            if isinstance(obj, FallObject):
                self.scene_parent.add_score(obj.score)
                if obj.status != "normal":
                    state["status"] = obj.status
                    self.collidCount = 0
                else:
                    if state["status"] != "normal":
                        if self.collidCount < 2:
                            self.collidCount += 1
                        else:
                            state["status"] = "normal"
                            self.collidCount = 0
                self.scene_parent.remove_item(obj.name)
        self.setPixmap(self.__picture__[state["status"]])

    @staticmethod
    def handle_keyrelease_event(state, event):
        state["speedX"] = 0

    @staticmethod
    def normal_behavior(state, event):
        if event.key() == Qt.Key_Left:
            state["speedX"] = -7
        elif event.key() == Qt.Key_Right:
            state["speedX"] = 7

    @staticmethod
    def weak_behavior(state, event):
        if event.key() == Qt.Key_Left:
            state["speedX"] = -5
        elif event.key() == Qt.Key_Right:
            state["speedX"] = 5

    @staticmethod
    def bonus_behavior(state, event):
        if event.key() == Qt.Key_Left:
            state["speedX"] = -12
        elif event.key() == Qt.Key_Right:
            state["speedX"] = 12


class Background(QGraphicsPixmapItem):
    def __init__(self):
        super(Background, self).__init__()
        self.__picture__ = QPixmap("resources//pic//background.png")
        self.setPixmap(self.__picture__)


class HappyWanwanjiang(QGraphicsPixmapItem):
    def __init__(self):
        super(HappyWanwanjiang, self).__init__()
        self.__picture__ = QPixmap("resources//pic//happy_end.png")
        self.setPixmap(self.__picture__)
        self.setOffset(-1 * self.__picture__.width() / 2,
                       -1 * self.__picture__.height() / 2)


class NormalWanwanjiang(QGraphicsPixmapItem):
    def __init__(self):
        super(NormalWanwanjiang, self).__init__()
        self.__picture__ = QPixmap("resources//pic//normalwanwanjiang.png")
        self.setPixmap(self.__picture__)
        self.setOffset(-1 * self.__picture__.width() / 2,
                       -1 * self.__picture__.height() / 2)


class SadWanwanjiang(QGraphicsPixmapItem):
    def __init__(self):
        super(SadWanwanjiang, self).__init__()
        self.__picture__ = QPixmap("resources//pic//sad_end.png")
        self.setPixmap(self.__picture__)
        self.setOffset(-1 * self.__picture__.width() / 2,
                       -1 * self.__picture__.height() / 2)


class StartGameButton(QGraphicsPixmapItem):
    def __init__(self, start_game_call):
        super(StartGameButton, self).__init__()
        self.__picture__ = QPixmap("resources//pic//startgame.png")
        self.setPixmap(self.__picture__)
        self.start_game_call = start_game_call

        self.setOffset(QPointF(-1 * self.__picture__.width() / 2,
                               -1 * self.__picture__.height() / 2))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print("StartGame")
        self.start_game_call()


class QuitGameButton(QGraphicsPixmapItem):
    def __init__(self, quit_game_call):
        super(QuitGameButton, self).__init__()
        self.__picture__ = QPixmap("resources//pic//quitgame.png")
        self.setPixmap(self.__picture__)
        self.quit_game_call = quit_game_call

        self.setOffset(QPointF(-1 * self.__picture__.width(), 0))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print("QuitGame")
        self.quit_game_call()


class ConfirmButton(QGraphicsPixmapItem):
    def __init__(self, confirm_call):
        super(ConfirmButton, self).__init__()
        self.__picture__ = QPixmap("resources//pic//confirm.png")
        self.setPixmap(self.__picture__)
        self.confirm_call = confirm_call

        self.setOffset(QPointF(-1 * self.__picture__.width() / 2,
                               -1 * self.__picture__.height() / 2))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print("QuitGame")
        self.confirm_call()


class FallObject(QGraphicsPixmapItem):
    def __init__(self, score, status, img, name, parent=None):
        super(FallObject, self).__init__()
        self.__picture__ = QPixmap("resources//pic//" + img)
        self.setPixmap(self.__picture__)
        self.setOffset(QPointF(-1 * self.__picture__.width() / 2,
                               -1 * self.__picture__.height()))

        self.score = score
        self.status = status
        self.name = name
        self.parent = parent

    def self_update(self, state):
        state["speedY"] += 0.2
        state["x"] += state["speedX"]
        state["y"] += state["speedY"]
        if state["y"] > 700:
            self.parent.remove_item(self.name)
