import random
import sys
import math
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import tablewid.data as static


# 表格组件
class Tablewid(QWidget):
     
    def __init__(self):
        super().__init__()
        
        
        self.getcolumnData = static.data["tablewid"]["columndata"]
        self.filterdata = [] #获取列字段
        self.getData = static.data["tablewid"]["data"]
        
        self.tablewid_group = QGroupBox("")
        self.tablewid_group.setStyleSheet("background:rgb(255,255,255)")
        self.tablewid_groupQV = QVBoxLayout()
        
        #创建筛选区域 
        self.createfilter(static.data["tablewid"]["columndata"])
        
        #记录当前页数
        self.currentpage = 1
        #self.get_gotobtntext = 1
        self.createtable(self.getData,self.getcolumnData)
        self.createtablepagebar()
        
        self.tablewid_group.setLayout(self.tablewid_groupQV)

    # 创建筛选
    def createfilter(self, arg):

        # 右侧 筛选条件
        self.filter_group = QGroupBox("")
        self.filter_group.setStyleSheet("border-radius:4px;color:#ffffff")
        self.filter_group.setFixedHeight(150)

        self.filter_layoutQV = QVBoxLayout()
        
        self.filter_scroll_QH = QHBoxLayout()
        self.filter_scroll_QH.setSpacing(20)
        
        self.filter_scroll = QScrollArea()
        self.filter_scroll_frame = QFrame()
      
        self.btn_layoutQH = QHBoxLayout()
        
        self.filter_scroll_QH.addLayout(self.creategrid(arg))
        self.filter_scroll_frame.setLayout(self.filter_scroll_QH)
        self.filter_scroll.setWidget(self.filter_scroll_frame)
        self.filter_layoutQV.addWidget(self.filter_scroll)
        
        self.filter_confirm = filterbtn("查询")
        self.filter_reset = filterbtn("重置")
        self.btn_layoutQH.addWidget(self.filter_confirm)
        self.btn_layoutQH.addWidget(self.filter_reset)
        self.btn_layoutQH.setContentsMargins(0,10,0,0)

        
        self.filter_layoutQV.addLayout(self.btn_layoutQH)
        self.filter_group.setLayout(self.filter_layoutQV)
        
        self.tablewid_groupQV.addWidget(self.filter_group)
        
    def creategrid(self,arg):
        
        widgets_pic_len  = len(arg)
        layout_grid = QGridLayout()
        for i in range(0, widgets_pic_len, 3):
            for j in range(i, min(i + 3, widgets_pic_len)):
                layout_grid.addLayout(self.createfiled(arg[j]),int(i/3),j%3,1,1)
                
        return layout_grid
        
    def createfiled(self, arg):
        filter_layoutForm = QFormLayout()

        label = QLabel(arg)
        label.setStyleSheet("color:#333333")
        label.setFixedWidth(60)
        QLine = QLineEdit()
        QLine.setFixedSize(150, 22)
        QLine.setStyleSheet("color:#333333;border:1px solid #e1e1e1")
        filter_layoutForm.addRow(label, QLine)

        return filter_layoutForm
    
        
        
    # 创建表格
    def createtable(self,arg1,arg2):
        #默认表格
        self.tableWidget = QTableWidget(10, 8)
        self.tableWidget.setFixedHeight(300)
        self.tableWidget.setHorizontalHeaderLabels(arg2)
        
        self.tableWidget.setStyleSheet(
            "QTableWidget::item { color:#333333;font-size:8px;border:0px solid rgb(255,255,11)}  QTableView::item:selected { background-color: rgba(81,93,128,0.3);  }")
        self.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section { color:#333333;font-weight:500;font-size:12px; }")
        self.tableWidget.verticalHeader().setStyleSheet(
            "QHeaderView::section { color:#333333;font-weight:500;font-size:12px; }")
        self.tableWidget.horizontalScrollBar().setStyleSheet(
            "QScrollBar:horizontal { background: rgb(208,209,210); height: 12px;  }")
        self.tableWidget.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical {  background: rgb(208,209,210); width: 12px;  }")
        
        #默认表格的数据
        for index, item in enumerate(arg1):
            for yndex,itemfiled in enumerate(arg2):
                self.tableWidget.setItem(index, yndex, QTableWidgetItem(item[itemfiled]))
                
        self.tablewid_groupQV.addWidget(self.tableWidget)
        
        
    #更新表格和数据,用于翻页时
    def updatetabledata(self,arg1,arg2):

        #清理表格数据 重新生成列和行
        self.tableWidget.clear()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(len(arg2)+2)
        
        #更新表格表头
        self.tableWidget.setHorizontalHeaderLabels(arg2)
        
        #更新表格数据
        for row, item in enumerate(arg1):  # 使用enumerate创建新的行索引
            for col, itemfield in enumerate(arg2):
                self.tableWidget.setItem(row, col, QTableWidgetItem(item[itemfield]))
        
        # print(self.Ace_getcolumnData)


    # 生成点击页数槽函数
    def btnclickfunc_decorator(self, flag):
        if flag == "next":
            def btnclickfunc():
                self.currentpage = self.currentpage+1 if self.currentpage<math.ceil(len(self.getData) / 10) else math.ceil(len(self.getData) / 10) 
                self.gather_frame_QV_tablewid_pagebarformlabel.setText(str(self.currentpage))
                self.updatetabledata(self.somepagedata(self.currentpage),self.getcolumnData)
        elif flag == "pre":
            def btnclickfunc():
                self.currentpage = self.currentpage-1 if self.currentpage>1 else 1
                self.gather_frame_QV_tablewid_pagebarformlabel.setText(str(self.currentpage))
                self.updatetabledata(self.somepagedata(self.currentpage),self.getcolumnData)
        elif flag == "fir":
            def btnclickfunc():
                self.currentpage = 1
                self.gather_frame_QV_tablewid_pagebarformlabel.setText(str(self.currentpage))
                self.updatetabledata(self.somepagedata(1),self.getcolumnData)
        elif flag == "lst":
            def btnclickfunc():
                self.currentpage = math.ceil(len(self.getData) / 10)
                self.gather_frame_QV_tablewid_pagebarformlabel.setText(str(self.currentpage))
                self.updatetabledata(self.somepagedata(self.currentpage),self.getcolumnData)
        elif flag == "goto":
            def btnclickfunc():
                gotopage = self.gather_frame_QV_tablewid_pagebarformlabel.text()
                gotopage = int(gotopage) if gotopage != "" else 1
                self.currentpage = gotopage
                self.updatetabledata(self.somepagedata(gotopage),self.getcolumnData)
        else:
            def btnclickfunc():
                self.updatetabledata(self.somepagedata(self.currentpage),self.getcolumnData)
        return btnclickfunc

    # 生成失焦获取 edit的文字槽函数
    def blurgettext(self):
        get_gotobtntext = self.gather_frame_QV_tablewid_pagebarformlabel.text()
        print("Text changed:", get_gotobtntext)
    

    def createtablepagebar(self):
        pagebar_QH = QHBoxLayout()

        firstpbtn = Pagebtn("首页")
        btnclick_funcnfir = self.btnclickfunc_decorator("fir")
        firstpbtn.clicked.connect(btnclick_funcnfir)
        
        lastpbtn = Pagebtn("尾页")
        btnclick_funcnlst = self.btnclickfunc_decorator("lst")
        lastpbtn.clicked.connect(btnclick_funcnlst)
        
        prebtn = Pagebtn("<")
        btnclick_funcnpre = self.btnclickfunc_decorator("pre")
        prebtn.clicked.connect(btnclick_funcnpre)
        
        nextbtn = Pagebtn(">")
        btnclick_funcnnext = self.btnclickfunc_decorator("next")
        nextbtn.clicked.connect(btnclick_funcnnext)
        
        #跳转页 input
        self.gather_frame_QV_tablewid_pagebarformlabel = QLineEdit()
        self.gather_frame_QV_tablewid_pagebarformlabel.setFixedSize(40, 26)
        self.gather_frame_QV_tablewid_pagebarformlabel.setStyleSheet("background:rgb(229,230,235);color:#333333")
        gotobtn = Pagebtn("跳转")
        btnclick_funcngoto = self.btnclickfunc_decorator("goto")
        gotobtn.clicked.connect(btnclick_funcngoto)

        pagebar_QH.addStretch()
        pagebar_QH.addWidget(firstpbtn)
        pagebar_QH.addWidget(prebtn)
        pagebar_QH.addWidget(self.gather_frame_QV_tablewid_pagebarformlabel)
        pagebar_QH.addWidget(gotobtn)
        pagebar_QH.addWidget(nextbtn)
        pagebar_QH.addWidget(lastpbtn)
        
        self.tablewid_groupQV.addLayout(pagebar_QH)
    

    # 根据点击的数字，展示某一页数据
    def somepagedata(self, arg):
        res = []
        for index, item in enumerate(self.getData):
            if 10*arg-10 <= index <= 10*arg-1:
                res.append(item)
        #print(res)
        return res
    

# 分页按钮的类
class Pagebtn(QPushButton):
    def __init__(self, arg):
        super().__init__()

        self.setText(arg)
        self.setFixedSize(26, 26)
        self.setStyleSheet(
            "font-size:10px;background-color:rgb(86,100,154);color:#ffffff;border-radius:2px;")

    def enterEvent(self, event):
        self.setStyleSheet(
            "font-size:10px;background-color:rgba(86,100,154,0.6);color:#ffffff;border-radius:2px;")

    def leaveEvent(self, event):
        self.setStyleSheet(
            "font-size:10px;background-color:rgba(86,100,154,1);color:#ffffff;border-radius:2px;")

# 搜索和btnBar 的按钮的类
class filterbtn(QPushButton):
    def __init__(self, arg):
        super().__init__()

        self.setText(arg)
        self.setFixedSize(52, 26)
        self.setStyleSheet(
            "background-color:rgb(86,100,154);color:#ffffff;border-radius:2px;")

    def enterEvent(self, event):
        self.setStyleSheet(
            "background-color:rgba(86,100,154,0.6);color:#ffffff;border-radius:2px;")

    def leaveEvent(self, event):
        self.setStyleSheet(
            "background-color:rgba(86,100,154,1);color:#ffffff;border-radius:2px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pass