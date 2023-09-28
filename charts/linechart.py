import time
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
from charts.data import ToCharts


class Linechart(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_group = QGroupBox()
        self.layout_QH = QHBoxLayout()
        self.layout_QH.setContentsMargins(0, 0, 0, 0)

        self.initUI()

    def createaxis_x(self, arg):
        axis_xarr = []
        for item in arg["linechart"]["axis_x"]:
            axis_xarr.append(item)

        # 创建坐标轴
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(axis_xarr)
        self.axis_x.setTitleText("日期")
        axis_x_font = QFont()
        axis_x_font.setPointSize(8)
        self.axis_x.setLabelsFont(axis_x_font)

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)

    def createaxis_y(self, arg):

        self.axis_y = QValueAxis()
        self.axis_y.setRange(
            0, max(arg["linechart"]["all_log"])+5)
        self.axis_y.setTitleText("Y Axis")
        axis_y_font = QFont()
        axis_y_font.setPointSize(10)
        self.axis_y.setLabelsFont(axis_y_font)

        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

    def initUI(self):

        #tocharts = ToCharts()

        linechart_x = []
        for i in range(0, 7):
            getdatetime = time.strftime("%m-%d", time.localtime(time.time()-i*86400))
            linechart_x.append(getdatetime)
        linechart_x.reverse()
        
        # 折线图数据
        linechart_data = {
            "linechart": {
                "legend": [["all_log", "#4c81ff"], ["success_log", "#f081ff"], ["fail_log", "#b381ff"]],
                "axis_x": linechart_x,
                "all_log": [10, 7, 4, 3, 6, 2, 0],
                "success_log": [8, 4, 4, 3, 6, 2, 0],
                "fail_log": [2, 3, 4, 3, 6, 2, 0]
            }
        }

        self.chart = QChart()
        self.legend = self.chart.legend()

        # 创建X坐标轴
        self.createaxis_x(linechart_data)
        # 创建Y坐标轴
        self.createaxis_y(linechart_data)

        series_arr = linechart_data["linechart"]["legend"]
        for item in series_arr:
                series_cj = QLineSeries()
                series_cj_scatter = QScatterSeries()
                series_cj_scatter.setMarkerSize(5)
                series_cj.setName(item[0])

                for index, val in enumerate(linechart_data["linechart"][item[0]]):
                    series_cj.append(index, val)
                    series_cj_scatter.append(index, val)

                self.chart.addSeries(series_cj)
                self.chart.addSeries(series_cj_scatter)

                series_cj.attachAxis(self.axis_x)
                series_cj_scatter.attachAxis(self.axis_x)

                series_cj.attachAxis(self.axis_y)
                series_cj_scatter.attachAxis(self.axis_y)

                # 设置线条颜色和宽度
                pen = QPen()
                pen.setWidth(2)
                series_cj.setPen(QColor(item[1]))

        # 将散点系列从图例中移除
        markers = self.legend.markers()
        for marker in markers:
            # 判断每一个图例是否属于QScatterSeries类
            if isinstance(marker.series(), QScatterSeries):
                marker.setVisible(False)

        # 创建视图和场景
        self.view = QChartView(self.chart)

        # 设置图表标题
        self.chart.setTitle("7日数据图")

        # 将折线图添加到图表展示窗口中
        self.chartView = QChartView(self.chart)
        self.chartView.setStyleSheet("background:#ffffff;padding:0,0,0,0;")

        self.layout_QH.addWidget(self.chartView)
        self.layout_group.setLayout(self.layout_QH)
