from PyQt5.QtCore import *
from Models import *


class MainController(QMainWindow):
    def __init__(self):
        super(MainController, self).__init__()
        self.MainView = QGraphicsView()
        self.MainView.setFixedSize(700, 672)
        self.GameView = QGraphicsView()
        self.current_model = None
        self.setWindowTitle("Wanwanjiang")
        self.setCentralWidget(self.MainView)
        self.MainView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MainView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__load_main_model__()

    def __load_main_model__(self):
        self.setFixedSize(700, 672)
        self.current_model = StartScene(self)
        self.current_model.Signal_ChangeModel.connect(self.__change_model__)
        self.MainView.setScene(self.current_model)

    def __load_game_model__(self):
        self.setFixedSize(700, 672)
        self.current_model = GameScene(self)
        self.current_model.Signal_ChangeModel.connect(self.__change_model__)
        self.MainView.setScene(self.current_model)

    def __load_end_fail_model__(self):
        self.setFixedSize(700, 672)
        self.current_model = EndSceneFail(self)
        self.current_model.Signal_ChangeModel.connect(self.__change_model__)
        self.MainView.setScene(self.current_model)

    def __load_end_succ_model__(self):
        self.setFixedSize(700, 672)
        self.current_model = EndSceneSuccess(self)
        self.current_model.Signal_ChangeModel.connect(self.__change_model__)
        self.MainView.setScene(self.current_model)

    @pyqtSlot(int, name="ChangeModel")
    def __change_model__(self, model_code):
        if model_code == 1:
            self.__load_main_model__()
        if model_code == 2:
            self.__load_game_model__()
        if model_code == 3:
            self.__load_end_fail_model__()
        if model_code == 4:
            self.__load_end_succ_model__()
        if model_code == 5:
            QMessageBox.information(self, "惊喜",
                                    "惊喜：https://blog.magichc7.com/post/forwanwanjiang.html",
                                    QMessageBox.Yes)



