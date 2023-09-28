from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import math
import pymysql
import time
import json
import croniter
from croniter import CroniterBadCronError


class Appmanag(QWidget):

    def __init__(self):
        super().__init__()

        # UI
        self.scrolllayout = QScrollArea()
        self.gridframe = QFrame()
        self.layout_QGrid = QGridLayout()
        self.layout_QGrid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # 实例化 Createapp
        self.createapp = Createapp()

        self.layout_QGrid.addWidget(self.createapp, 0, 0, 1, 1)
        # 点击self.createapp
        self.createapp.mousePressEvent = self.on_createapp

        # 初始化 从数据库里拿出数据渲染apps
        self.creategrid()

        # 实例化 SubmitDialog
        self.submitialog = SubmitDialog()

        self.gridframe.setLayout(self.layout_QGrid)

        self.scrolllayout.setWidget(self.gridframe)

    def getdata(self):
        self.db = pymysql.connect(host="localhost",
                                  user="root",
                                  password="12345678",
                                  database="mysql",
                                  charset='utf8mb4')

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

        # SQL 插入语句
        sql = "select id,title, noticetype from noticeapp where is_deleted = 0"
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交执行
            self.db.commit()
            # 获取数据
            col = ["id", "title", "noticetype"]
            data = []
            for item in self.cursor.fetchall():
                res = {}
                for jndex, jtem in enumerate(item):
                    res[col[jndex]] = jtem
                data.append(res)

            # 关闭游标连接
            self.cursor.close()
            # 关闭数据库连接
            self.db.close()

            return data

        except:
            # 发生错误时回滚
            self.db.rollback()
            # 关闭数据库连接
            self.db.close()

    def creategrid(self):

        # 从数据库获取数据
        data = self.getdata() if self.getdata() else []
        data_len = len(data) if data else 0

        # 获取真实位置的list
        ijlist = []
        for i in range(0, math.ceil(data_len/4+0.1)):
            for j in range(0, 4):
                ijlist.append([i, j])
        ijlist.pop(0)

        for index, item in enumerate(data):
            self.everyapp = Everyapp(
                self, item["id"], item["title"], item["noticetype"])
            self.layout_QGrid.addWidget(
                self.everyapp, ijlist[index][0], ijlist[index][1], 1, 1)

    def updategrid(self):

        # 从数据库获取数据
        data = self.getdata()
        data_len = len(data)

        # 清空布局以重新渲染数据
        for i in reversed(range(1, self.layout_QGrid.count())):
            widget = self.layout_QGrid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # 获取真实位置的list
        ijlist = []
        for i in range(0, math.ceil(data_len/4+0.1)):
            for j in range(0, 4):
                ijlist.append([i, j])
        ijlist.pop(0)

        for index, item in enumerate(data):
            self.everyapp = Everyapp(
                self, item["id"], item["title"], item["noticetype"])
            self.layout_QGrid.addWidget(
                self.everyapp, ijlist[index][0], ijlist[index][1], 1, 1)

        # 渲染数据后，重新布局
        self.gridframe.adjustSize()  # 重新计算QFrame的大小以适应新的内容
        self.scrolllayout.setWidgetResizable(True)
        # self.scrolllayout.updateGeometry()
        # print(self.layout_QGrid.)

    def on_createapp(self, event):
        self.submitialog.exec()
        self.submitialog.apps_updated.connect(self.updategrid())


# 定义创建app的类
class Createapp(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setFixedSize(180, 200)
        self.setStyleSheet(
            "background-color:{};border-radius:4px;".format("rgb(255,255,255)"))
        createappQV = QVBoxLayout()
        createappQV.setAlignment(Qt.AlignCenter)

        self.createappframe = QFrame()
        self.createappframe.setStyleSheet(
            "background-color:{};border-radius:4px;".format("rgb(240,240,240)"))
        self.createappframe.setFixedSize(140, 140)
        createappframeQH = QHBoxLayout()
        createappframeadd = QLabel("+")
        createappframeadd.setStyleSheet("color:rgb(96,96,96);font-size:80px;")
        createappframeQH.addWidget(createappframeadd)
        createappframeQH.setAlignment(Qt.AlignCenter)
        self.createappframe.setLayout(createappframeQH)

        createapptitleQH = QHBoxLayout()
        createapptitleQH.setAlignment(Qt.AlignCenter)
        createapptitle = QLabel("create")
        createapptitle.setStyleSheet("color:#333333;border-radius:4px;")
        createapptitleQH.addWidget(createapptitle)

        createappQV.addWidget(self.createappframe)
        createappQV.addSpacing(4)
        createappQV.addLayout(createapptitleQH)

        self.setLayout(createappQV)

    def enterEvent(self, event):
        self.createappframe.setStyleSheet(
            "background-color:{};border-radius:4px;".format("rgb(200,200,200)"))

    def leaveEvent(self, event):
        self.createappframe.setStyleSheet(
            "background-color:{};border-radius:4px;".format("rgb(240,240,240)"))


# 已经创建好的app的类
class Everyapp(QGroupBox):
    def __init__(self, Appmanag_self, id, title, mestype):
        super().__init__()

        self.Appmanag_self = Appmanag_self
        self.id = id
        self.mestype = mestype

        self.setProperty("id", self.id)
        self.setProperty("mestype", self.mestype)

        self.setFixedSize(180, 200)
        self.setStyleSheet("border-radius:4px;")
        self.everyappQV = QVBoxLayout()
        self.everyappQV.setAlignment(Qt.AlignCenter)

        self.everyapplabel = QLabel(title)
        self.everyapplabel.setFixedSize(140, 140)
        if mestype == "钉钉通知":
            pic = "pic/ddpic.jpeg"
        elif mestype == "钉钉工作通知":
            pic = "pic/ddgzpic.jpg"
        elif mestype == "短信通知":
            pic = "pic/mespic.jpg"
        self.everyapplogo = QPixmap(pic)  # 替换为你的图像文件路径
        self.everyapplabel.setScaledContents(True)
        self.everyapplabel.setPixmap(self.everyapplogo)

        self.everyapptitleQH = QHBoxLayout()
        self.everyapptitleQH.setAlignment(Qt.AlignCenter)
        self.everyapptitle = QLabel(title)
        self.everyapptitle.setStyleSheet(
            "color:{};border-radius:4px;".format("#333333"))
        self.everyapptitleQH.addWidget(self.everyapptitle)

        self.everyappQV.addWidget(self.everyapplabel)
        self.everyappQV.addSpacing(4)
        self.everyappQV.addLayout(self.everyapptitleQH)

        self.setLayout(self.everyappQV)

    def enterEvent(self, event):
        self.setStyleSheet(
            "background-color:{};border-radius:4px;".format("rgb(226,227,227)"))

    def leaveEvent(self, event):
        self.setStyleSheet(
            "background-color:{};border-radius:4px;".format("rgb(255,255,255)"))

    def mousePressEvent(self, event):
        # 获取Appmanag 的实例化对象【唯一】
        self.dataDialog = DataDialog(self.Appmanag_self, self.id)
        self.dataDialog.exec()


class SubmitDialog(QDialog):

    apps_updated = Signal(str)  # 定义一个信号

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setWindowTitle("定时通知表单")
        self.setMinimumSize(340, 300)

        # 创建表单布局
        self.form_layoutQV = QVBoxLayout(self)

        # 添加表单标题
        self.formtitle_QH = QHBoxLayout()
        self.formtitle_label = QLabel("标题:")
        self.formtitle_label.setFixedWidth(80)
        self.formtitle_input = QLineEdit()
        self.formtitle_input.setMinimumSize(200, 24)
        self.formtitle_QH.addWidget(self.formtitle_label)
        self.formtitle_QH.addWidget(self.formtitle_input)
        self.form_layoutQV.addLayout(self.formtitle_QH)

        # 选择类型
        self.mestypeframeQH = QHBoxLayout()
        self.radio_grouplabel = QLabel("通知类型:")
        self.radio_grouplabel.setFixedWidth(80)
        self.dd_radio = QRadioButton("钉钉通知")
        self.dd_radio.setChecked(True)
        self.ddgz_radio = QRadioButton("钉钉工作通知")
        self.mes_radio = QRadioButton("短信通知")

        self.mestypeframeQH.addWidget(self.radio_grouplabel)
        self.mestypeframeQH.addWidget(self.dd_radio)
        self.mestypeframeQH.addWidget(self.ddgz_radio)
        self.mestypeframeQH.addWidget(self.mes_radio)

        self.form_layoutQV.addLayout(self.mestypeframeQH)

        self.dd_radio.clicked.connect(self.toggle_radio)
        self.ddgz_radio.clicked.connect(self.toggle_radio)
        self.mes_radio.clicked.connect(self.toggle_radio)

        # 堆叠布局
        self.stacklayout = QStackedLayout()

        # 堆叠布局下钉钉form
        self.stacklayout_ddframe = QFrame()
        self.stacklayout_ddframeQV = QVBoxLayout()
        self.stacklayout_ddframeQV.setContentsMargins(0, 0, 0, 0)

        self.stacklayout_ddQH1 = QHBoxLayout()
        self.ddframewebhook_label = QLabel("WEBHOOK:")
        self.ddframewebhook_label.setFixedWidth(80)
        self.ddframewebhook_input = QLineEdit()
        self.ddframewebhook_input.setMinimumSize(200, 24)
        self.stacklayout_ddQH1.addWidget(self.ddframewebhook_label)
        self.stacklayout_ddQH1.addWidget(self.ddframewebhook_input)

        self.stacklayout_ddQH2 = QHBoxLayout()
        self.ddframesecret_label = QLabel("加签:")
        self.ddframesecret_label.setFixedWidth(80)
        self.ddframesecret_input = QLineEdit()
        self.ddframesecret_input.setMinimumSize(200, 24)
        self.stacklayout_ddQH2.addWidget(self.ddframesecret_label)
        self.stacklayout_ddQH2.addWidget(self.ddframesecret_input)

        self.stacklayout_ddQH3 = QHBoxLayout()
        self.ddframeddjson_label = QLabel("推送内容:")
        self.ddframeddjson_label.setFixedWidth(80)
        self.ddframeddjson_input = QTextEdit()
        self.ddframeddjson_input.setMinimumSize(200, 50)
        self.stacklayout_ddQH3.addWidget(self.ddframeddjson_label)
        self.stacklayout_ddQH3.addWidget(self.ddframeddjson_input)

        self.stacklayout_ddframeQV.addLayout(self.stacklayout_ddQH1)
        self.stacklayout_ddframeQV.addLayout(self.stacklayout_ddQH2)
        self.stacklayout_ddframeQV.addLayout(self.stacklayout_ddQH3)

        self.stacklayout_ddframe.setLayout(self.stacklayout_ddframeQV)

        # 堆叠布局下钉钉工作通知ddgz  form
        self.stacklayout_ddgzframe = QFrame()
        self.stacklayout_ddgzframeQV = QVBoxLayout()
        self.stacklayout_ddgzframeQV.setContentsMargins(0, 0, 0, 0)

        self.stacklayout_ddgzQH1 = QHBoxLayout()
        self.ddgzframeappkey_label = QLabel("appKey:")
        self.ddgzframeappkey_label.setFixedWidth(80)
        self.ddgzframeappkey_input = QLineEdit()
        self.ddgzframeappkey_input.setMinimumSize(200, 24)
        self.stacklayout_ddgzQH1.addWidget(self.ddgzframeappkey_label)
        self.stacklayout_ddgzQH1.addWidget(self.ddgzframeappkey_input)

        self.stacklayout_ddgzQH2 = QHBoxLayout()
        self.ddgzframeappsecret_label = QLabel("appSecret:")
        self.ddgzframeappsecret_label.setFixedWidth(80)
        self.ddgzframeappsecret_input = QLineEdit()
        self.ddgzframeappsecret_input.setMinimumSize(200, 24)
        self.stacklayout_ddgzQH2.addWidget(self.ddgzframeappsecret_label)
        self.stacklayout_ddgzQH2.addWidget(self.ddgzframeappsecret_input)

        self.stacklayout_ddgzQH3 = QHBoxLayout()
        self.ddgzframeddjson_label = QLabel("推送内容:")
        self.ddgzframeddjson_label.setFixedWidth(80)
        self.ddgzframeddjson_input = QTextEdit()
        self.ddgzframeddjson_input.setMinimumSize(200, 50)
        self.stacklayout_ddgzQH3.addWidget(self.ddgzframeddjson_label)
        self.stacklayout_ddgzQH3.addWidget(self.ddgzframeddjson_input)

        self.stacklayout_ddgzframeQV.addLayout(self.stacklayout_ddgzQH1)
        self.stacklayout_ddgzframeQV.addLayout(self.stacklayout_ddgzQH2)
        self.stacklayout_ddgzframeQV.addLayout(self.stacklayout_ddgzQH3)

        self.stacklayout_ddgzframe.setLayout(self.stacklayout_ddgzframeQV)

        # 堆叠布局下短信form
        self.stacklayout_mesframe = QFrame()
        self.stacklayout_mesframeQV = QVBoxLayout()

        self.stacklayout_mesQH1 = QHBoxLayout()
        self.mesframearg1_label = QLabel("Arg1:")
        self.mesframearg1_label.setFixedWidth(80)
        self.mesframearg1_input = QLineEdit()
        self.mesframearg1_input.setMinimumSize(200, 24)
        self.stacklayout_mesQH1.addWidget(self.mesframearg1_label)
        self.stacklayout_mesQH1.addWidget(self.mesframearg1_input)

        self.stacklayout_mesQH2 = QHBoxLayout()
        self.mesframearg2_label = QLabel("Arg2:")
        self.mesframearg2_label.setFixedWidth(80)
        self.mesframearg2_input = QLineEdit()
        self.mesframearg2_input.setMinimumSize(200, 24)
        self.stacklayout_mesQH2.addWidget(self.mesframearg2_label)
        self.stacklayout_mesQH2.addWidget(self.mesframearg2_input)

        self.stacklayout_mesframeQV.addLayout(self.stacklayout_mesQH1)
        self.stacklayout_mesframeQV.addLayout(self.stacklayout_mesQH2)

        self.stacklayout_mesframe.setLayout(self.stacklayout_mesframeQV)

        self.stacklayout.addWidget(self.stacklayout_ddframe)
        self.stacklayout.addWidget(self.stacklayout_ddgzframe)
        self.stacklayout.addWidget(self.stacklayout_mesframe)

        self.form_layoutQV.addLayout(self.stacklayout)

        # 添加定时策略

        # self.clockmethodframe = QFrame()
        self.clockmethodframeQH = QHBoxLayout()
        # 时间策略
        self.clockmethodlabel = QLabel("定时策略:")
        self.clockmethodlabel.setFixedWidth(80)

        self.noticemethod = QLineEdit()
        self.noticemethod.setMinimumSize(200, 24)

        self.clockmethodframeQH.addWidget(self.clockmethodlabel)
        self.clockmethodframeQH.addWidget(self.noticemethod)

        self.form_layoutQV.addLayout(self.clockmethodframeQH)

        # 添加表单提交按钮
        self.buttonQH = QHBoxLayout()
        self.cancel_button = QPushButton("取消")
        self.submit_button = QPushButton("提交")
        self.buttonQH.addWidget(self.cancel_button)
        self.buttonQH.addWidget(self.submit_button)
        self.form_layoutQV.addLayout(self.buttonQH)

        # 连接表单 取消按钮的点击事件
        self.cancel_button.clicked.connect(self.on_cancel)
        # 连接表单 提交按钮的点击事件
        self.submit_button.clicked.connect(self.on_submit)

    def toggle_radio(self):
        if self.dd_radio.isChecked():
            self.stacklayout.setCurrentIndex(0)
            print("类型：钉钉通知")
        elif self.ddgz_radio.isChecked():
            self.stacklayout.setCurrentIndex(1)
            print("类型：钉钉工作通知")
        elif self.mes_radio.isChecked():
            self.stacklayout.setCurrentIndex(2)
            print("类型：短信通知")

    def on_cancel(self):
        self.accept()

    def on_submit(self):
        name = self.formtitle_input.text()
        print(f"你创建了新应用,名为{name}")

        # 获取 cron 验证结果
        is_valid, error_message = self.validate_cron_expression(
            self.noticemethod.text())

        # 判断是否有空
        if self.formtitle_input.text() == "" or self.noticemethod.text() == "":
            notice = NoticeDialog("有空值, 请检查")
            notice.exec()
        else:
            if is_valid:

                # 插入数据库
                getdatetime = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())

                if self.dd_radio.isChecked():
                    getradiotext = self.dd_radio.text()
                elif self.ddgz_radio.isChecked():
                    getradiotext = self.ddgz_radio.text()
                elif self.mes_radio.isChecked():
                    getradiotext = self.mes_radio.text()

                if self.dd_radio.isChecked():
                    noticeargs = {
                        "webhook": self.ddframewebhook_input.text(),
                        "secret": self.ddframesecret_input.text(),
                        "noticejson": self.ddframeddjson_input.toPlainText()
                    }
                elif self.ddgz_radio.isChecked():
                    noticeargs = {
                        "appkey": self.ddgzframeappkey_input.text(),
                        "appsecret": self.ddgzframeappsecret_input.text(),
                        "noticejson": self.ddgzframeddjson_input.toPlainText()
                    }
                else:
                    noticeargs = {
                        "arg1": self.mesframearg1_input.text(),
                        "arg2": self.mesframearg2_input.text()
                    }

                # 变成字符串
                noticeargs = json.dumps(noticeargs, ensure_ascii=False)
                self.insert_mysql(0, self.formtitle_input.text(), getradiotext, noticeargs, self.noticemethod.text(), getdatetime, 0)

                # 关闭对话框
                self.accept()

            else:
                invalidcron = NoticeDialog("cron表达式不合法,请修改")
                invalidcron.exec()

    # 用于校验 cron是否合法
    def validate_cron_expression(self, cron_expression):
        try:
            # 尝试创建 croniter 对象
            cron = croniter.croniter(cron_expression)
            return True, None  # cron 表达式有效
        except CroniterBadCronError as e:
            return False, str(e)  # cron 表达式无效，返回错误消息

    # 数据库
    def insert_mysql(self, id, title, noticetype, noticeargs, noticemethod, createtime, is_deleted):
        self.db = pymysql.connect(host="localhost",
                                  user="root",
                                  password="12345678",
                                  database="mysql",
                                  charset='utf8mb4')

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

        # SQL 插入语句
        sql = "insert into noticeapp(id, title, noticetype, noticeargs, noticemethod, createtime, is_deleted) \
            VALUES (%s, '%s',  '%s',  '%s', '%s' ,'%s' ,%s )" % \
            (id, title, noticetype, noticeargs,
             noticemethod, createtime, is_deleted)

        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交执行
            self.db.commit()
            # 关闭游标连接
            self.cursor.close()
            # 关闭数据库连接
            self.db.close()

        except:
            # 发生错误时回滚
            self.db.rollback()
            # 关闭数据库连接
            self.db.close()


class DataDialog(QDialog):

    delapps_updated = Signal(str)  # 定义一个信号

    def __init__(self, Appmanag_self, appid):
        super().__init__()

        self.Appmanag_self = Appmanag_self
        self.appid = appid

        data = self.getdata_mysql(self.appid)[0]

        # 尝试解析noticeargs中的noticejson
        data["noticeargs"] = data["noticeargs"].replace(" ", "").replace(
            '"{', "{").replace('}"', "}")
        data["noticeargs"] = json.loads(data["noticeargs"])
        try:
            data["noticeargs"]["noticejson"] = json.dumps(
                data["noticeargs"]["noticejson"], ensure_ascii=False)
            self.initdialog(data)
        except:
            self.initdialog(data)

    def initdialog(self, data):
        self.setWindowTitle("数据详情")
        self.setMinimumSize(340, 300)

        # 创建表单布局
        self.form_layoutQV = QVBoxLayout(self)

        # 添加表单标题
        self.formtitle_QH = QHBoxLayout()
        self.formtitle_label = QLabel("标题:")
        self.formtitle_label.setFixedWidth(80)
        self.formtitle_input = QLineEdit()
        self.formtitle_input.setText(data["title"])  # 根据sql查出来数据 渲染
        self.formtitle_input.setReadOnly(True)
        self.formtitle_input.setMinimumSize(200, 24)
        self.formtitle_QH.addWidget(self.formtitle_label)
        self.formtitle_QH.addWidget(self.formtitle_input)
        self.form_layoutQV.addLayout(self.formtitle_QH)

        # 选择类型
        self.mestypeframeQH = QHBoxLayout()
        self.radio_grouplabel = QLabel("通知类型:")
        self.radio_grouplabel.setFixedWidth(80)

        self.dd_radio = QRadioButton("钉钉通知")
        self.ddgz_radio = QRadioButton("钉钉工作通知")
        self.mes_radio = QRadioButton("短信通知")

        if data["noticetype"] == "钉钉通知":
            self.dd_radio.setChecked(True)

            self.dd_radio.setDisabled(True)  # 设置为不可用状态
            self.ddgz_radio.setDisabled(True)  # 设置为不可用状态
            self.mes_radio.setDisabled(True)  # 设置为不可用状态
        elif data["noticetype"] == "钉钉工作通知":
            self.ddgz_radio.setChecked(True)

            self.dd_radio.setDisabled(True)  # 设置为不可用状态
            self.ddgz_radio.setDisabled(True)  # 设置为不可用状态
            self.mes_radio.setDisabled(True)  # 设置为不可用状态
        elif data["noticetype"] == "短信通知":
            self.mes_radio.setChecked(True)

            self.dd_radio.setDisabled(True)  # 设置为不可用状态
            self.ddgz_radio.setDisabled(True)  # 设置为不可用状态
            self.mes_radio.setDisabled(True)  # 设置为不可用状态

        self.mestypeframeQH.addWidget(self.radio_grouplabel)
        self.mestypeframeQH.addWidget(self.dd_radio)
        self.mestypeframeQH.addWidget(self.ddgz_radio)
        self.mestypeframeQH.addWidget(self.mes_radio)

        self.form_layoutQV.addLayout(self.mestypeframeQH)

        # 堆叠布局
        self.stacklayout = QStackedLayout()
        self.stacklayout_frame = QFrame()
        if data["noticetype"] == "钉钉通知":
            self.stacklayout.setCurrentIndex(0)
            # 堆叠布局下钉钉form
            self.stacklayout_ddframe = QFrame()
            self.stacklayout_ddframeQV = QVBoxLayout()
            self.stacklayout_ddframeQV.setContentsMargins(0, 0, 0, 0)

            self.stacklayout_ddQH1 = QHBoxLayout()
            self.ddframewebhook_label = QLabel("WEBHOOK:")
            self.ddframewebhook_label.setFixedWidth(80)
            self.ddframewebhook_input = QLineEdit()
            self.ddframewebhook_input.setText(
                data["noticeargs"]["webhook"])  # 根据sql查出来数据 渲染
            self.ddframewebhook_input.setReadOnly(True)
            self.ddframewebhook_input.setMinimumSize(200, 24)
            self.stacklayout_ddQH1.addWidget(self.ddframewebhook_label)
            self.stacklayout_ddQH1.addWidget(self.ddframewebhook_input)

            self.stacklayout_ddQH2 = QHBoxLayout()
            self.ddframesecret_label = QLabel("加签:")
            self.ddframesecret_label.setFixedWidth(80)
            self.ddframesecret_input = QLineEdit()
            self.ddframesecret_input.setText(
                data["noticeargs"]["secret"])  # 根据sql查出来数据 渲染
            self.ddframesecret_input.setReadOnly(True)
            self.ddframesecret_input.setMinimumSize(200, 24)
            self.stacklayout_ddQH2.addWidget(self.ddframesecret_label)
            self.stacklayout_ddQH2.addWidget(self.ddframesecret_input)

            self.stacklayout_ddQH3 = QHBoxLayout()
            self.ddframeddjson_label = QLabel("推送内容:")
            self.ddframeddjson_label.setFixedWidth(80)
            self.ddframeddjson_input = QTextEdit()
            self.ddframeddjson_input.setPlainText(
                data["noticeargs"]["noticejson"])  # 根据sql查出来数据 渲染
            self.ddframeddjson_input.setReadOnly(True)
            self.ddframeddjson_input.setMinimumSize(200, 50)
            self.stacklayout_ddQH3.addWidget(self.ddframeddjson_label)
            self.stacklayout_ddQH3.addWidget(self.ddframeddjson_input)

            self.stacklayout_ddframeQV.addLayout(self.stacklayout_ddQH1)
            self.stacklayout_ddframeQV.addLayout(self.stacklayout_ddQH2)
            self.stacklayout_ddframeQV.addLayout(self.stacklayout_ddQH3)

            self.stacklayout_frame.setLayout(self.stacklayout_ddframeQV)

        elif data["noticetype"] == "钉钉工作通知":
            self.stacklayout.setCurrentIndex(1)
            # 堆叠布局下钉钉form
            self.stacklayout_ddgzframe = QFrame()
            self.stacklayout_ddgzframeQV = QVBoxLayout()
            self.stacklayout_ddgzframeQV.setContentsMargins(0, 0, 0, 0)

            self.stacklayout_ddgzQH1 = QHBoxLayout()
            self.ddgzframeappkey_label = QLabel("appKey:")
            self.ddgzframeappkey_label.setFixedWidth(80)
            self.ddgzframeappkey_input = QLineEdit()
            self.ddgzframeappkey_input.setText(
                data["noticeargs"]["appkey"])  # 根据sql查出来数据 渲染
            self.ddgzframeappkey_input.setReadOnly(True)
            self.ddgzframeappkey_input.setMinimumSize(200, 24)
            self.stacklayout_ddgzQH1.addWidget(self.ddgzframeappkey_label)
            self.stacklayout_ddgzQH1.addWidget(self.ddgzframeappkey_input)

            self.stacklayout_ddgzQH2 = QHBoxLayout()
            self.ddgzframeappsecret_label = QLabel("appSecret:")
            self.ddgzframeappsecret_label.setFixedWidth(80)
            self.ddgzframeappsecret_input = QLineEdit()
            self.ddgzframeappsecret_input.setText(
                data["noticeargs"]["appsecret"])  # 根据sql查出来数据 渲染
            self.ddgzframeappsecret_input.setReadOnly(True)
            self.ddgzframeappsecret_input.setMinimumSize(200, 24)
            self.stacklayout_ddgzQH2.addWidget(self.ddgzframeappsecret_label)
            self.stacklayout_ddgzQH2.addWidget(self.ddgzframeappsecret_input)

            self.stacklayout_ddgzQH3 = QHBoxLayout()
            self.ddgzframeddjson_label = QLabel("推送内容:")
            self.ddgzframeddjson_label.setFixedWidth(80)
            self.ddgzframeddjson_input = QTextEdit()
            self.ddgzframeddjson_input.setPlainText(
                data["noticeargs"]["noticejson"])  # 根据sql查出来数据 渲染
            self.ddgzframeddjson_input.setReadOnly(True)
            self.ddgzframeddjson_input.setMinimumSize(200, 50)
            self.stacklayout_ddgzQH3.addWidget(self.ddgzframeddjson_label)
            self.stacklayout_ddgzQH3.addWidget(self.ddgzframeddjson_input)

            self.stacklayout_ddgzframeQV.addLayout(self.stacklayout_ddgzQH1)
            self.stacklayout_ddgzframeQV.addLayout(self.stacklayout_ddgzQH2)
            self.stacklayout_ddgzframeQV.addLayout(self.stacklayout_ddgzQH3)

            self.stacklayout_frame.setLayout(self.stacklayout_ddgzframeQV)

        elif data["noticetype"] == "短信通知":
            self.stacklayout.setCurrentIndex(2)
            # 堆叠布局下短信form
            self.stacklayout_mesframeQV = QVBoxLayout()

            self.stacklayout_mesQH1 = QHBoxLayout()
            self.mesframearg1_label = QLabel("Arg1:")
            self.mesframearg1_label.setFixedWidth(80)
            self.mesframearg1_input = QLineEdit()
            self.mesframearg1_input.setText(
                data["noticeargs"]["arg1"])  # 根据sql查出来数据 渲染
            self.mesframearg1_input.setReadOnly(True)
            self.mesframearg1_input.setMinimumSize(200, 24)
            self.stacklayout_mesQH1.addWidget(self.mesframearg1_label)
            self.stacklayout_mesQH1.addWidget(self.mesframearg1_input)

            self.stacklayout_mesQH2 = QHBoxLayout()
            self.mesframearg2_label = QLabel("Arg2:")
            self.mesframearg2_label.setFixedWidth(80)
            self.mesframearg2_input = QLineEdit()
            self.mesframearg2_input.setText(
                data["noticeargs"]["arg2"])  # 根据sql查出来数据 渲染
            self.mesframearg2_input.setReadOnly(True)
            self.mesframearg2_input.setMinimumSize(200, 24)
            self.stacklayout_mesQH2.addWidget(self.mesframearg2_label)
            self.stacklayout_mesQH2.addWidget(self.mesframearg2_input)

            self.stacklayout_mesframeQV.addLayout(self.stacklayout_mesQH1)
            self.stacklayout_mesframeQV.addLayout(self.stacklayout_mesQH2)

            self.stacklayout_frame.setLayout(self.stacklayout_mesframeQV)

        self.stacklayout.addWidget(self.stacklayout_frame)
        self.form_layoutQV.addLayout(self.stacklayout)

        # 添加定时策略
        self.clockmethodframeQH = QHBoxLayout()
        # 时间策略
        self.clockmethodlabel = QLabel("定时策略:")
        self.clockmethodlabel.setFixedWidth(80)

        self.timemethod = QLineEdit()
        self.timemethod.setText(data["noticemethod"])  # 根据sql查出来数据 渲染
        self.timemethod.setReadOnly(True)
        self.timemethod.setMinimumSize(200, 24)

        self.clockmethodframeQH.addWidget(self.clockmethodlabel)
        self.clockmethodframeQH.addWidget(self.timemethod)

        self.form_layoutQV.addLayout(self.clockmethodframeQH)

        # 添加创建时间
        self.createtimeframeQH = QHBoxLayout()
        # 时间策略
        self.createtimelabel = QLabel("创建时间:")
        self.createtimelabel.setFixedWidth(80)

        self.createtimetext = QLabel(data["createtime"])

        self.createtimeframeQH.addWidget(self.createtimelabel)
        self.createtimeframeQH.addWidget(self.createtimetext)

        self.form_layoutQV.addLayout(self.createtimeframeQH)

        # 添加表单提交按钮
        self.buttonQH = QHBoxLayout()
        self.del_button = QPushButton("删除")
        self.close_button = QPushButton("关闭")
        self.buttonQH.addWidget(self.del_button)
        self.buttonQH.addStretch()
        self.buttonQH.addWidget(self.close_button)
        self.form_layoutQV.addLayout(self.buttonQH)

        # 连接表单 关闭按钮的点击事件
        self.del_button.clicked.connect(self.del_def)
        self.close_button.clicked.connect(self.close_def)

    def toggle_radio(self):
        if self.dd_radio.isChecked():
            self.stacklayout.setCurrentIndex(0)
            print("类型：钉钉通知")
        elif self.mes_radio.isChecked():
            self.stacklayout.setCurrentIndex(1)
            print("类型：短信通知")

    def close_def(self):
        # 关闭对话框
        self.accept()

    def del_def(self, event):
        self.deldata_mysql(self.appid)
        self.delapps_updated.connect(self.Appmanag_self.updategrid())
        # 关闭对话框
        self.accept()

    def getdata_mysql(self, appid):
        self.db = pymysql.connect(host="localhost",
                                  user="root",
                                  password="12345678",
                                  database="mysql",
                                  charset='utf8mb4')

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

        # SQL 插入语句
        sql = f"select id,title, noticetype, noticeargs, noticemethod,DATE_FORMAT(createtime,'%Y-%m-%d %H:%i:%s') from noticeapp where id = {appid}"

        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交执行
            self.db.commit()
            # 获取 处理数据
            col = ["id", "title", "noticetype",
                   "noticeargs", "noticemethod", "createtime"]
            data = []
            for item in self.cursor.fetchall():
                res = {}
                for jndex, jtem in enumerate(item):
                    res[col[jndex]] = jtem
                data.append(res)

            # 关闭游标连接
            self.cursor.close()
            # 关闭数据库连接
            self.db.close()

            return data

        except:
            # 发生错误时回滚
            self.db.rollback()
            # 关闭数据库连接
            self.db.close()

    def deldata_mysql(self, appid):
        self.db = pymysql.connect(host="localhost",
                                  user="root",
                                  password="12345678",
                                  database="mysql",
                                  charset='utf8mb4')

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

        # SQL 插入语句
        sql = f"UPDATE noticeapp SET is_deleted = 1 where id = {appid}"

        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交执行
            self.db.commit()
            # 获取数据
            data = self.cursor.fetchall()
            # 关闭游标连接
            self.cursor.close()
            # 关闭数据库连接
            self.db.close()

            return data

        except:
            # 发生错误时回滚
            self.db.rollback()
            # 关闭数据库连接
            self.db.close()


class NoticeDialog(QDialog):
    def __init__(self, arg):
        super().__init__()
        self.setWindowTitle("提示表单")

        layoutQV = QVBoxLayout()

        label_layoutQH = QHBoxLayout()
        label = QLabel(arg)
        label_layoutQH.addWidget(label)

        btn_layoutQH = QHBoxLayout()
        btn = QPushButton("关闭")
        btn.clicked.connect(self.closedialog)
        btn_layoutQH.addWidget(btn)

        layoutQV.addLayout(label_layoutQH)
        layoutQV.addLayout(btn_layoutQH)

        self.setLayout(layoutQV)

    def closedialog(self):
        self.accept()



