from collections import deque
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import copy as copy
import socket
import time
import threading
import fileinput


class PModel(QGraphicsScene):
    def __init__(self, parent: 'QGraphicsScene' = None):
        super(PModel, self).__init__(parent)
    pass