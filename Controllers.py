from PyQt5.QtWidgets import *
from PyQt5 import Qt


class MainController(QMainWindow):
    def __init__(self):
        super(MainController, self).__init__()
        self.MainView = QGraphicsView()
        self.GameView = QGraphicsView()
        self.setFixedSize(700, 672)
        self.current_model = None
        self.setWindowTitle("Wanwanjiang")
        self.MainView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MainView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # start game

    def _start_game(self):

        pass


