# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from MasterSpider.settings import REDIS_HOST, REDIS_PORT
import redis
redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1, decode_responses=True)
class MasterspiderPipeline(object):
    def process_item(self, item, spider):
        # redis_db.set('Master',item['url'])
        redis_db.lpush('MasterSpider:start_urls',item['url'])
        return item
