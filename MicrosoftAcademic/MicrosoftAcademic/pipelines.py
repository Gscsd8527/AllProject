# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import json
import datetime
class MicrosoftacademicPipeline(object):
    def __init__(self):
        # 链接数据库
        client = pymongo.MongoClient(host='127.0.0.1')
        self.db = client['Microsoft']  # 获得数据库的句柄
        self.coll = self.db['key_dataset']  # 获得collection的句柄
        # 数据库登录需要帐号密码的话
        # self.db.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])
    #
    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        self.coll.insert(postItem)  # 向数据库插入一条记录

    # def process_item(self, item, spider):
    #     self.date = datetime.datetime.today().strftime('%Y-%m-%d')
    #     # date = datetime.datetime.today().strftime('%Y-%m-%d')
    #     lines = json.dumps(dict(item), ensure_ascii=False)
    #     # with open(date + 'spiderdata2600_3000.json', 'a+', encoding="utf-8") as f:
    #     with open('KeyData.json', 'a+', encoding="utf-8") as f:
    #         f.write(lines)
    #         f.write('\n')

