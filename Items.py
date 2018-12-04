from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Wanwanjiang(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super(Wanwanjiang, self).__init__(parent=parent)
        self.__picture__ = QPixmap("resources//pic//wanwanjiang.png")
        self.setPixmap(self.__picture__)
        self.setOffset(QPointF(-1 * self.__picture__.width() / 2,
                               -1 * self.__picture__.height()))

        self.behaviorMap = {"normal": self.normal_behavior,
                            "weak": self.weak_behavior,
                            "bonus": self.bonus_behavior}

        self.init_state = {"x": 700 / 2,
                           "y": 672,
                           "speedX": 0,
                           "speedY": 0,
                           "status": "normal"
                           }

    def handle_keypress_event(self, state, event):
        self.behaviorMap[state["status"]](state, event)

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


class StartGameButton(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super(StartGameButton, self).__init__(parent=parent)
        self.__picture__ = QPixmap("resources//pic//wanwanjiang.png")
        self.setPixmap(self.__picture__)

        self.setOffset(QPointF(-1 * self.__picture__.width() / 2,
                               -1 * self.__picture__.height()))


class ResumeGameButton(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super(ResumeGameButton, self).__init__(parent=parent)
        self.__picture__ = list()
        self.__picture__.append(QPixmap("resources//pic//wanwanjiang.png"))
        self.__picture__.append(QPixmap("resources//pic//wanwanjiang.png"))
        self.setPixmap(self.__picture__[0])

        self.setOffset(QPointF(-1 * self.__picture__[0].width() / 2,
                               -1 * self.__picture__[0].height()))

    @pyqtSlot(int, name='resumeGame')
    def __change_pic__(self, status_code):
        if status_code == 0:
            self.setPixmap(self.__picture__[0])
        if status_code == 1:
            self.setPixmap(self.__picture__[1])


class FallObject(QGraphicsPixmapItem):
    def __init__(self, score, speed, parent=None):
        super(FallObject, self).__init__(parent=parent)
        self.__picture__ = QPixmap("resources//pic//wanwanjiang.png")
        self.setPixmap(self.__picture__)

        self.score = score
        self.speed = speed
