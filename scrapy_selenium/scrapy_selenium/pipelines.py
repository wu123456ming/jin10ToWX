# -*- coding: utf-8 -*-
# from redis import Redis
# import pandas as pd
import logging
import re
import time

import pymongo
# from pymysql import connect

from scrapy.exceptions import DropItem
from scrapy.conf import settings
class MongoPipeline(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler("log2.txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.logger.addHandler(console)



        self.parseFileDir = r"C:\Users\wuming\AppData\Roaming\MetaQuotes\Terminal\F884183C9F0A36329B7B3B945F18FF84\MQL4\Files"
        self.parseFileDir2 = r"C:\Users\wuming\AppData\Roaming\MetaQuotes\Terminal\2010C2441A263399B34F537D91A53AC9\MQL4\Files"



    def open_spider(self,spider):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        self.client = pymongo.MongoClient(host=host, port=port)
        tdb = self.client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
    def process_item(self, item, spider):
        if not self.post.find_one({'date_id': item['date_id']}):
            wenzi = item['wenzi_text']
            self.dealWenzi(wenzi)
            self.post.insert(item)
            return item
    def close_spider(self,spider):
        self.client.close()

    def dealWenzi(self, wenzi):


        symbol = ""
        # listStr = symbol.split("，")
        # if len(listStr)  == 0 :
        #     return
        #
        # wenzi = listStr[0]
        print("wenzi==============================>",wenzi)
        if wenzi.__contains__("黄金")  or wenzi.__contains__("国际金"):
            symbol = "GOLD"
        elif wenzi.__contains__("WTI"):
            symbol = "WTI"
        else:
            searchObj = re.search(r'([A-Z]{3}/[A-Z]{3})', wenzi)
            if searchObj:
                symbol = searchObj.group(1).replace("/","")
        if symbol != "":
            action = 0
            if wenzi.__contains__("由涨转跌"):
                action = -1
            elif wenzi.__contains__("由跌转涨"):
                action = 1
            elif wenzi.__contains__("收复日内跌幅") or wenzi.__contains__("收复跌幅"):
                action = 1
            elif wenzi.__contains__("抹平"):
                action = -1
            elif wenzi.__contains__("下挫") or wenzi.__contains__("跌")  or wenzi.__contains__("下行"):
                action = -1
            elif wenzi.__contains__("涨") or wenzi.__contains__("上行")or wenzi.__contains__("升"):
                action = 1

            if action != 0 :
                self.writeFile(symbol,action)


    def writeFile(self, symbol, action):
        resultFile = self.parseFileDir + "\\" + symbol+ "_RESULT.csv"
        resultFile2 = self.parseFileDir + "\\" + symbol+ "_RESULT.csv"
        self.writeFile2(resultFile,action)
        self.writeFile2(resultFile2, action)
        pass

    def writeFile2(self,path, action):
        print("writeFile:", path.split("\\")[-1])
        try:
            with open(path, mode='w+') as file:
                file.write(str(action))
            if str(action) != "0":
                with open("log.txt", mode='a') as file:
                    file.write(
                        str(time.localtime(time.time())) + "=====>" + path.split("\\")[-1] + "====>" + str(
                            action) + "\r\n")
        except Exception as  e:
            self.logger.info(e)
            with open("log.txt", mode='a') as file:
                file.write(
                    str(time.localtime(time.time())) + "=====>" + path.split("\\")[-1] + "====>" + str(e) + "\r\n")
            pass

# import pymysql
# import redis
# import pandas
# import json
# redis_db = redis.Redis(host='127.0.0.1',port=6379,db=1) # 连接本地redis，db数据库默认连接到0号库，写的是索引值
# redis_data_dict = ''  # key的名字，里面的内容随便写，这里的key相当于字典名称，而不是key值。为了后面引用而建的
#
# class MysqlRemovePipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect(host="localhost",port=3306,user='root',password='123456',db='jinshishujuku',charset='utf8') # 连接mysql
#         self.cursor = self.conn.cursor()  # 建立游标
#         # print(redis_db)
#         redis_db.flushdb('date_id')  # 清空当前数据库中的所有 key，为了后面将mysql数据库中的数据全部保存进去
#         # print(redis_db)
#         if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mysql数据并临时保存在redis中
#             sql = 'select date_id from jinshi'  # 查询表中的现有数据
#             df = pandas.read_sql(sql,self.conn)  # 读取mysql中的数据
#              # print(df)
#             for date_id in df['date_id'].get_values():
#                 redis_db.hset(redis_data_dict,date_id,0) # 把每个url写入field中，value值随便设，我设置的0  key field value 三者的关系
#
#     def process_item(self,item,spider):
#         """
#         比较爬取的数据在数据库中是否存在，不存在则插入数据库
#         :param item: 爬取到的数据
#         :param spider: /
#         """
#         if redis_db.hexists(redis_data_dict,item['date_id']): # 比较的是redis_data_dict里面的field
#             print("数据库已经存在该条数据，不再继续追加")
#         else:
#             self.do_insert(item)
#
#     def do_insert(self, item):
#         insert_sql = """
#                 insert into jinshi VALUES(0,%s,%s,%s,%s,%s,%s)
#                             """
#         args = [item['date_id'], item['date'], item['wenzi_text'], item['gengduo_url'],item['wenzi_href_url'], item['photo_url']]
#         self.cursor.execute(insert_sql,args)
#         self.conn.commit()  # 提交操作，提交了才真正保存到数据库中
#         return item
#
#     def close_spider(self,spider):
#         self.cursor.close()  # 关闭游标
#         self.conn.close()    # 关闭连接