import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from charts.barchart import Barchart
from charts.linechart import Linechart
from charts.indicator import Indicator
 
class Workbench(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_QV_group = QGroupBox()
        self.layout_QGrid = QGridLayout()
        
        self.initUI()
        
        self.layout_QV_group.setLayout(self.layout_QGrid)

    def initUI(self):

        self.layout_QGrid.addWidget(Indicator(0).layout_group,0,0,1,2) 
        self.layout_QGrid.addWidget(Indicator(1).layout_group,0,2,1,2)
        self.layout_QGrid.addWidget(Indicator(2).layout_group,0,4,1,2) 
        self.layout_QGrid.addWidget(Indicator(3).layout_group,0,6,1,2)

        self.layout_QGrid.addWidget(Barchart().layout_group,1,0,1,4)
        self.layout_QGrid.addWidget(Linechart().layout_group,1,4,1,4)
        
        
    def reinitUI(self):
        #清空self.layout_QGrid 下面所有组件  
        for i in reversed(range(self.layout_QGrid.count())):
                item = self.layout_QGrid.itemAt(i)
                widget = item.widget()
                if widget:
                    self.layout_QGrid.removeWidget(widget)
                    widget.setParent(None)
        
        #重新添加self.layout_QGrid 下面所有组件  
        self.layout_QGrid.addWidget(Indicator(0).layout_group,0,0,1,2) 
        self.layout_QGrid.addWidget(Indicator(1).layout_group,0,2,1,2)
        self.layout_QGrid.addWidget(Indicator(2).layout_group,0,4,1,2) 
        self.layout_QGrid.addWidget(Indicator(3).layout_group,0,6,1,2)
        
        self.layout_QGrid.addWidget(Barchart().layout_group,1,0,1,4)
        self.layout_QGrid.addWidget(Linechart().layout_group,1,4,1,4)
        
        self.layout_QV_group.setLayout(self.layout_QGrid)