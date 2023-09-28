import pymysql


class GetLogdata:
    
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

    def getdata_sql(self):
        try:
            self.connect()

            # 使用参数化查询来避免 SQL 注入攻击
            sql = "select CONVERT(id, CHAR), title, noticetype, noticeargs, noticemethod, logres, creater, DATE_FORMAT(createtime,'%Y-%m-%d %H:%i:%s') from noticelog " 
            
            self.cursor.execute(sql)
            self.db.commit()
            col =["id", "title", "noticetype", "noticeargs", "noticemethod", "logres", "creater", "createtime"]
            data=[]
            for item in self.cursor.fetchall():
                res={}
                for jndex, jtem in enumerate(item):
                    res[col[jndex]]=jtem
                data.append(res)
                
            #print(data)
            return data

        except Exception as e:
            print("An error occurred: ", str(e))
            self.db.rollback()
            
        finally:
            self.disconnect()
            



data = {
        "tablewid": {
            "columndata":["id", "title", "noticetype", "noticeargs", "noticemethod", "logres", "creater", "createtime"],
            "data":GetLogdata().getdata_sql()
        }}
 