# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime
from redis import *
class MicrosoftacademicPipeline(object):

    # def process_item(self, item, spider):
    #     date = datetime.datetime.today().strftime('%Y-%m-%d')
    #     hour = datetime.datetime.today().strftime('%H')
    #     lines = json.dumps(dict(item), ensure_ascii=False)
    #     if '01' <= hour <= '06':
    #         end = '1'
    #     elif '06' < hour <= '12':
    #         end = '2'
    #     elif '12' < hour <= '18':
    #         end = '3'
    #     elif hour > '18':
    #         end = '4'
    #     else:
    #         end = '5'
    #     date_hour = date + '-' + end
    #     # with open('/json_data/' + date_hour + 'ReferenceData.json', 'a+', encoding="utf-8") as f:
    #     # with open('ReferenceData.json', 'a+', encoding="utf-8") as f:
    #     # with open('CitedByData.json', 'a+', encoding="utf-8") as f:
    #     # with open('CitedByData2.json', 'a+', encoding="utf-8") as f:
    #     # with open('CitedByData3.json', 'a+', encoding="utf-8") as f:
    #     with open('RelatedData.json', 'a+', encoding="utf-8") as f:
    #         f.write('{}\n'.format(lines))

    # def __init__(self):
    #     import pymongo
    #     # 链接数据库
    #     client = pymongo.MongoClient(host='127.0.0.1')
    #     self.db = client['Microsoft']  # 获得数据库的句柄
    #     self.coll = self.db['references2']  # 获得collection的句柄
    #     # 数据库登录需要帐号密码的话
    #     # self.db.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])
    # #
    # def process_item(self, item, spider):
    #     postItem = dict(item)  # 把item转化成字典形式
    #     self.coll.insert(postItem)  # 向数据库插入一条记录

    def process_item(self, item, spider):
        try:
            redis = StrictRedis(host='39.107.45.99', port=6379, db=2)
            lines = json.dumps(dict(item), ensure_ascii=False)
            redis.rpush('data', lines)
        except:
            self.date = datetime.datetime.today().strftime('%Y-%m-%d')
            date = datetime.datetime.today().strftime('%Y-%m-%d')
            lines = json.dumps(dict(item), ensure_ascii=False)
            # with open(date + 'spiderdata.json', 'a+', encoding="utf-8") as f:
            with open('/json_data/' + date + 'KeyData.json', 'a+', encoding="utf-8") as f:
                f.write('{}\n'.format(lines))
