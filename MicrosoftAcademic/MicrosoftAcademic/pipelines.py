# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
import json
import codecs

class MicrosoftacademicPipeline(object):
    # def __init__(self):
    #     # 链接数据库
    #     client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
    #     self.db = client[settings['MONGO_DB']]  # 获得数据库的句柄
    #     self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄
    #     # 数据库登录需要帐号密码的话
    #     # self.db.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])
    #
    # def process_item(self, item, spider):
    #     postItem = dict(item)  # 把item转化成字典形式
    #     self.coll.insert(postItem)  # 向数据库插入一条记录
    #     # return item  # 会在控制台输出原item数据，可以选择不写

    # def process_item(self, item, spider):
    #     print('item= ', item)
    #     data_josn = json.dumps(item, ensure_ascii=False)
    #     with open('data.txt', 'a+', encoding='utf-8') as f:
    #         f.write(data_josn)
    #         f.write('\n')

    def __init__(self):
        self.file = codecs.open('spiderdata.json', 'a+', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

