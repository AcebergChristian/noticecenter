import random
import sys
from PySide6.QtWidgets import *
from PySide6 import *
from PySide6.QtCore import Slot
from topnav import Topnav
from workbench import Workbench
from appmanag import Appmanag
from tablewid import Tablewid
from bottombar import Bottombar



class Rightcontent(QWidget):
    def __init__(self):
        super().__init__()
        
        
        #右侧最大布局
        self.rightcontent_layout = QVBoxLayout()
        
        
        #导入的顶部导航栏
        self.topnav_group = Topnav()
        self.rightcontent_layout.addWidget(self.topnav_group.topnav_group)
        #self.rightcontent_layout.addStretch()
        
        
        #堆叠布局
        self.rightstack_layout = QStackedLayout()
        #对堆叠布局数据
        self.rightcontentdata = [{"title":"工作台"},
                                 {"title":"应用管理"},
                                 {"title":"调用日志"}]
        
        ####堆叠布局之工作台
        self.stacklayout_workbench = Workbench()
        
        #####堆叠布局之apps
        self.stacklayout_appmanag = Appmanag()
        
        #####堆叠布局之表格主体
        self.stacklayout_tablewid = Tablewid()
        

        #堆叠布局导入四个tab
        self.rightstack_layout.addWidget(self.stacklayout_workbench.layout_QV_group)
        self.rightstack_layout.addWidget(self.stacklayout_appmanag.scrolllayout)
        self.rightstack_layout.addWidget(self.stacklayout_tablewid.tablewid_group)

        
        #堆叠布局纺放入大布局里
        self.rightcontent_layout.addLayout(self.rightstack_layout)


        #导入右侧bottombar
        self.bottombar_group = Bottombar()
        self.rightcontent_layout.addWidget(self.bottombar_group.bottombar_group)
        
        
    
    #接受leftmenu发出的信号方法
    @Slot(str)
    def getmenuindex(self, msg):
        self.stacklayout_workbench.reinitUI()
        self.rightstack_layout.setCurrentIndex(msg["index"])
        
        