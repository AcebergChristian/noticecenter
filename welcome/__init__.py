import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class Welcome(QWidget):
    def __init__(self):
        super().__init__()

        # 无边框
        self.setWindowFlag(Qt.FramelessWindowHint)

        # 初始化组件 布局
        self.initmainwindow()

    def initmainwindow(self):
        logoQH = QHBoxLayout()
        logoQH.setContentsMargins(6, 6, 6, 6)
        logolabel = QLabel()
        logolabel.setFixedSize(440, 240)
        logolabel.setScaledContents(True)

        everyapplogo = QPixmap("pic/welcome.jpg")  # 替换为你的图像文件路径

        logolabel.setPixmap(everyapplogo)
        logoQH.addWidget(logolabel)

        self.setStyleSheet("border-radius:8px")
        self.setLayout(logoQH)
