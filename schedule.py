from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import time
import pymysql
import requests
import json
import hmac
import hashlib
import base64
import urllib.parse


class Schedulenotice:
    def __init__(self):
        # 创建一个后台调度器
        self.scheduler = BackgroundScheduler()
    
    def getdata(self):
        self.db = pymysql.connect(host="localhost",
                    user="root",
                    password="12345678",
                    database="mysql",
                    charset='utf8')


        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()        
        
        # SQL 插入语句
        sql = f"select id, title, noticetype, noticeargs, noticemethod from noticeapp where is_deleted=0"
        col = ["id", "title", "noticetype", "noticeargs", "noticemethod"]
        data = []
        
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交执行
            self.db.commit()
            # 获取并处理数据
            for item in self.cursor.fetchall():
                getjson = {}
                for jdenx, jtem in enumerate(item):
                    getjson[ col[jdenx] ] = jtem
                data.append(getjson)
                
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


    def task(self):
        
        data = self.getdata()
        for task in data:

            cron = CronTrigger.from_crontab(task["noticemethod"])
            # 计算下次执行时间
            next_run_time = cron.get_next_fire_time(None,datetime.now())
            self.scheduler.add_job(self.my_task, args=[task["id"],task["title"],task["noticetype"],task["noticeargs"],task["noticemethod"]  ], trigger=cron, next_run_time=next_run_time)
            
            
    # 示例的任务函数，可以根据你的需求自定义
    def my_task(self,*arg):
        if arg[2] == "钉钉通知":
            replacestr = arg[3].replace('"{', '{').replace('}"', '}')
            replacestr = json.loads(replacestr)
    
            # 解析钉钉群通知
            ddtz = DDTZ(replacestr["webhook"],replacestr["secret"],replacestr["noticejson"])
            ddtz.torun()
            
            # 定时任务插入日志
            getdatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            tolog = ToLog()
            try:
                tolog.insert_sql(0,arg[1],arg[2],arg[3],arg[4],"成功","robot",getdatetime)
            except:
                tolog.insert_sql(0,arg[1],arg[2],arg[3],arg[4],"失败","robot",getdatetime)
        
        elif arg[2] == "钉钉工作通知":
            pass
        elif arg[2] == "短信通知":
            pass
        elif arg[2] == "邮箱通知":
            pass
            
    def torun(self):
        self.task()
        self.scheduler.start()
        
        try:
            # 让程序保持运行
            while True:
                pass
                #time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            # 如果需要手动停止程序，可以在这里添加停止调度器的代码
            self.scheduler.shutdown()
            

class DDTZ:
    def __init__(self, webhook, secret,argsjson):
        self.webhook = webhook
        self.secret = secret
        self.argsjson = argsjson

    def get_dding_sign(self, secret):
        timestamp = str(round(time.time() * 1000))  # 时间戳
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                             digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        return timestamp, sign

    def geturl_params(self):
        timestamp, sign = self.get_dding_sign(self.secret)

        url_params = {"access_token": self.webhook,
                      "timestamp": timestamp, "sign": sign}

        return url_params

    def getmsgdata(self):
        data = self.argsjson

        return data

    def torun(self):
        url = "https://oapi.dingtalk.com/robot/send"
        r = requests.post(url, params=self.geturl_params(),
                          json=self.getmsgdata())

        print("定时通知================>")
        print(f"您已发送了一个通知，URL为:{url},参数为{self.geturl_params()}")
        print("Response:", r.status_code, r.json())
        
        
        
class ToLog:
    
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = pymysql.connect(host="localhost",
                                  user="root",
                                  password="12345678",
                                  database="mysql",
                                  charset='utf8mb4')
        
        self.cursor = self.db.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def insert_sql(self, id, title, noticetype, noticeargs, noticemethod, logres, creater, createtime):
        try:
            self.connect()

            # 使用参数化查询来避免 SQL 注入攻击
            sql = "INSERT INTO noticelog (id, title, noticetype, noticeargs, noticemethod, logres, creater, createtime) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (id, title, noticetype, noticeargs, noticemethod, logres, creater, createtime)
            
            self.cursor.execute(sql, values)
            self.db.commit()

        except Exception as e:
            print("An error occurred: ", str(e))
            self.db.rollback()
            
        finally:
            self.disconnect()
    
    
       
Schedulenotice().torun()
