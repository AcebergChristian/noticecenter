import pymysql
import time


class ToCharts:

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

    def getdatasql(self, sql):
        try:
            self.connect()

            # 使用参数化查询来避免 SQL 注入攻击

            self.cursor.execute(sql)
            self.db.commit()
            data = self.cursor.fetchall()
            return data
        
        except Exception as e:
            print("An error occurred: ", str(e))
            self.db.rollback()

        finally:
            self.disconnect()


