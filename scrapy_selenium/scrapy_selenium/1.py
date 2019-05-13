# -*- coding: utf-8 -*-
# @Time    : 2018/12/10 0010 20:12
# @Author  : huangtao
# @Site    : 
# @File    : 1.py
# @Software: PyCharm
# @Blog    :https://blog.csdn.net/Programmer_huangtao
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from scrapy.conf import settings
import pymongo
class XiaoMiQuanPipeLines(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]

        client = pymongo.MongoClient(host=host, port=port)

        mydb = client[dbname]

        self.post = mydb[sheetname]

    def process_item(self, item):
        url = item['file_url']
        name = item['name']

        result = self.post.aggregate(
        [
        {"$group": {"_id": {"url": url, "name": name}}}
        ]
        )
        if result:
            pass
        else:

            self.post.insert({"url": url, "name": name})
        return item


class DownLoadPipelines(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename', '')

    def get_media_requests(self, item, info):
        file_url = item['file_url']
        meta = {'filename': item['name']}
        yield Request(url=file_url, meta=meta)