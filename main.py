import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from mainwindow import MainWindow
from welcome import Welcome
import time

class RunUI:
    def __init__(self):
        app = QApplication(sys.argv)
        print("欢迎登陆noticecenter...")

        self.welcome = Welcome()
        self.welcome.resize(440,240)
        self.window = MainWindow()
        self.window.resize(1060, 680)

        self.welcome.show()
        
        # 创建定时器
        timer = QTimer()
        timer.setSingleShot(True)  # 仅执行一次
        timer.timeout.connect(self.show_window)

        # 设置10秒后显示欢迎界面
        timer.start(3000)

        # 执行事件循环
        sys.exit(app.exec())
    
    def show_window(self):
        # 关闭欢迎界面并显示主窗口
        self.welcome.hide()
        self.window.show()
    
if __name__ == "__main__":
    runUI = RunUI()
    

    
        

    
    

    
    
    
    
    

    
    


    
    



