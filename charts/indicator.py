from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
from charts.data import ToCharts


class Indicator(QWidget):
    def __init__(self, arg):
        super().__init__()

        self.arg = arg
        
        self.layout_group = QGroupBox()
        self.layout_group.setStyleSheet(
            "background:#dbdde5;border-radius:2px;")
        self.layout_group.setFixedHeight(60)
        
        self.initUI()


    def initUI(self):
        tocharts = ToCharts()
        # 不同数据
        if self.arg==0:
            allappnum = tocharts.getdatasql("select count(id) from noticeapp where is_deleted=0")[0][0]
            self.data =  {"yesterdaycn_title": "总应用",
             "yesterdaycn_val": str(allappnum),
             "yesterdaycn_rate": "+ 120.18%",
             "iconcolor": "background:rgb(66,70,126)"}
        elif self.arg==1:
            ddappnum = tocharts.getdatasql("select count(id) from noticeapp where noticetype='钉钉通知' and is_deleted=0")[0][0]
            self.data =  {"yesterdaycn_title": "钉钉通知",
             "yesterdaycn_val": str(ddappnum),
             "yesterdaycn_rate": "+ 110%",
             "iconcolor": "background:rgb(253,67,116)"}
        elif self.arg==2:
            ddgzappnum = tocharts.getdatasql("select count(id) from noticeapp where noticetype='钉钉工作通知' and is_deleted=0")[0][0]
            self.data =  {"yesterdaycn_title": "钉钉工作通知",
             "yesterdaycn_val": str(ddgzappnum),
             "yesterdaycn_rate": "- 20.68%",
             "iconcolor": "background:rgb(59,213,149)"}
        elif self.arg==3:
            mesappnum = tocharts.getdatasql("select count(id) from noticeapp where noticetype='短信通知' and is_deleted=0")[0][0]
            self.data =  {"yesterdaycn_title": "短信通知",
             "yesterdaycn_val": str(mesappnum),
             "yesterdaycn_rate": "+ 180.07%",
             "iconcolor": "background:rgb(246,109,98)"}
        
        # icon
        indicator_icon = QFrame()
        indicator_icon.setFixedSize(30, 30)
        indicator_icon.setStyleSheet(
            "background:url(charts/pic/indicator.svg) no-repeat center center;")
        indicator_icon_bg = QFrame()
        indicator_icon_bg_QH = QHBoxLayout()
        indicator_icon_bg.setFixedSize(30, 30)
        indicator_icon_bg.setStyleSheet(
            self.data["iconcolor"]+";border-radius:15px")
        indicator_icon_bg_QH.setContentsMargins(0, 0, 0, 0)
        indicator_icon_bg_QH.addWidget(indicator_icon)
        indicator_icon_bg.setLayout(indicator_icon_bg_QH)

        # 标题和值
        indicator_label_QV = QVBoxLayout()
        indicator_label1 = QLabel(self.data["yesterdaycn_title"])
        indicator_label1.setStyleSheet("color:#333333;font-size:10px;")
        indicator_label2 = QLabel(self.data["yesterdaycn_val"])
        indicator_label2.setStyleSheet("color:#333333;font-size:14px;")
        indicator_label_QV.addWidget(indicator_label1)
        indicator_label_QV.addWidget(indicator_label2)

        # 涨幅率
        indicator_updown_QV = QVBoxLayout()
        indicator_updown = QLabel(self.data["yesterdaycn_rate"])

        def judgeupdown(
            x): return "color:rgb(50,167,139);font-size:10px;" if "+" in x else "color:rgb(243,65,69);font-size:10px;"
        indicator_updown.setStyleSheet(judgeupdown(
            self.data["yesterdaycn_rate"]))
        indicator_updown_QV.addWidget(indicator_updown)
        indicator_updown_QV.addStretch()

        # 以上三个组件放到布局里
        self.layout_QH = QHBoxLayout()
    
        self.layout_QH.addWidget(indicator_icon_bg)
        self.layout_QH.addLayout(indicator_label_QV)
        self.layout_QH.addLayout(indicator_updown_QV)

        self.layout_group.setLayout(self.layout_QH)

    