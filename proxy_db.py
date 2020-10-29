import re
import pymysql
from proxy_dbError import PoolEmptyError
from proxy_setting import *
from random import choice

class MysqlClient(object):
    def __init__(self, host=HOST, port=MYSQL_PORT, username=MYSQL_USERNAME, password=MYSQL_PASSWORD, sqlname=SQL_NAME):
        # 注意此处参数名为user而非username
        self.db = pymysql.connect(host=host, port=port, user=username, password=password, db=sqlname)
        self.cursor = self.db.cursor()

    def addIP(self, ip, score=INITIAL_SCORE):
        # pymysql.err.ProgrammingError: (1064,
        # "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version "
        # "for the right syntax to use near '' at line 1")
        sql_addIP = "INSERT INTO PROXY (IP,SCORE) VALUES ('%s', %s)" % (ip,score)
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', ip):
            print("IP格式有误，", ip, "丢弃")
            return
        if not self.exists(ip):
            # 一般 utf-8 编码下，一个汉字符占用 3 个字节；数字属于汉字，和汉字占用一样字节。
            # 一般 gbk 编码下，一个汉字字符占用 2 个字节；
            # 定义ip字段为varchar(15)报pymysql.err.DataError: (1406, "Data too long for column 'ip' at row 1")
            self.cursor.execute(sql_addIP)
            self.db.commit()

    def decreaseScore(self, ip):
        sql_getScore = "SELECT * FROM PROXY WHERE IP='%s'" % (ip)
        self.cursor.execute(sql_getScore)
        score = self.cursor.fetchone()[1]
        if score and score > MIN_SCORE:
            print('代理', ip, '当前分数', score, '减1')
            sql_changeScore = "UPDATE PROXY SET SCORE = %s WHERE IP = '%s'" % (score - 1, ip)
        else:
            print('代理', ip, '当前分数', score, '移除')
            sql_changeScore = "DELETE FROM PROXY WHERE IP = %s" % (ip)
        self.cursor.execute(sql_changeScore)
        self.db.commit()

    def maxScore(self, ip):
        print('代理', ip, '可用，设为', MAX_SCORE)
        sql_maxScore = "UPDATE PROXY SET SCORE = %s WHERE IP = '%s'" % (MAX_SCORE, ip)
        self.cursor.execute(sql_maxScore)
        self.db.commit()

    def randomIP(self):
        # 先从满分中随机选一个
        sql_max = "SELECT * FROM PROXY WHERE SCORE=%s" % (MAX_SCORE)
        if self.cursor.execute(sql_max):
            results = self.cursor.fetchall()
            return choice(results)[0]
        # 没有满分则随机选一个
        else:
            sql_all = "SELECT * FROM PROXY WHERE SCORE BETWEEN %s AND %s" % (MIN_SCORE, MAX_SCORE)
            if self.cursor.execute(sql_all):
                results = self.cursor.fetchall()
                return choice(results)[0]
            else:
                raise PoolEmptyError

    # 判断是否存在
    def exists(self, ip):
        sql_exists = "SELECT 1 FROM PROXY WHERE IP='%s' limit 1" % ip
        return self.cursor.execute(sql_exists)

    # 获取数量
    def count(self):
        sql_count = "SELECT * FROM PROXY"
        return self.cursor.execute(sql_count)

    # 获取全部
    def all(self):
        self.count()
        return self.cursor.fetchall()

    # 批量获取
    def batch(self, start, stop):
        sql_batch = "SELECT * FROM PROXY LIMIT %s, %s" % (start, stop - start)
        self.cursor.execute(sql_batch)
        return self.cursor.fetchall()

