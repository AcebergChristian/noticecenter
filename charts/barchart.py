import enum
import numbers
import random
import sys
from tokenize import Number
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
from charts.data import ToCharts


class Barchart(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_group = QGroupBox()
        self.layout_QH = QHBoxLayout()
        self.layout_QH.setContentsMargins(0, 0, 0, 0)

        self.initUI()

    def createdata(self, arg):
        # 创建条状图组
        barseries = QBarSeries()
        barset = QBarSet("通知类别")
        set0 = []
        for item in arg["val"]:
            set0.append(item)
        
        barset.append(set0)
        barset.setColor(QColor("#4c81ff"))

        barseries.append(barset)

        return barseries

    def createaxis_x(self):
        axis_xarr = []
        for item in self.data["barchart"]["axis_x"]:
            axis_xarr.append(item)
        return axis_xarr

    # 生成图表
    def initUI(self):

        tocharts = ToCharts()
        # 不同数据
        
        ddappnum = tocharts.getdatasql("select count(id) from noticeapp where noticetype='钉钉通知' and is_deleted=0")[0][0]
        ddgzappnum = tocharts.getdatasql("select count(id) from noticeapp where noticetype='钉钉工作通知' and is_deleted=0")[0][0]
        mesappnum = tocharts.getdatasql("select count(id) from noticeapp where noticetype='短信通知' and is_deleted=0")[0][0]
        
        self.data = {
            "barchart": {
                "axis_x":  [tup[0] for tup in tocharts.getdatasql("select distinct(noticetype) from noticeapp where is_deleted=0")],
                "val": [ddappnum,ddgzappnum, mesappnum]
            }
        }

        barseries = self.createdata(self.data["barchart"])

        # 创建图表
        chart = QChart()
        chart.setTitle('各类型数据')
        chart.addSeries(barseries)
        chart.setAnimationOptions(QChart.SeriesAnimations)  # 设置成动画显示

        # 设置X轴  名称
        axis_x = QBarCategoryAxis()
        axis_x.append(self.createaxis_x())
        chart.addAxis(axis_x, Qt.AlignBottom)
        barseries.attachAxis(axis_x)

        # 设置Y轴 数值
        axis_y = QValueAxis()
        axis_y.setLabelFormat('%d')     # 以整型显示刻度
        maxval = max(self.data["barchart"]["val"])+20
        axis_y.setRange(0, maxval)
        axis_y.setTickCount(7)
        chart.addAxis(axis_y, Qt.AlignLeft)
        barseries.attachAxis(axis_y)

        chart.legend().setVisible(True)       # 显示图例，默认为显示
        chart.legend().setAlignment(Qt.AlignBottom)  # 在底部显示图例信息

        # 将柱状图添加到图表展示窗口中
        chartView = QChartView(chart)
        chartView.setStyleSheet("background:#ffffff;padding:0,0,0,0;")

        self.layout_QH.addWidget(chartView)
        self.layout_group.setLayout(self.layout_QH)

