# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from redis import *
import datetime
class MicrosoftauthorsPipeline(object):
    def process_item(self, item, spider):
        # date = datetime.datetime.today().strftime('%Y-%m-%d')


        try:
            redis = StrictRedis(host='39.107.45.99', port=6379, db=0)
            lines = json.dumps(dict(item), ensure_ascii=False)
            redis.rpush('data', lines)
        except:
            # with open(date + 'Authors.json', 'a+', encoding="utf-8") as f:
            lines = json.dumps(dict(item), ensure_ascii=False)
            # with open('ComputerAuthors.json', 'a+', encoding="utf-8") as f:
            # with open('BiologyTpoic.json', 'a+', encoding="utf-8") as f:
            # with open('PhysicsTpoic.json', 'a+', encoding="utf-8") as f:
            # with open('ChemistryTpoic.json', 'a+', encoding="utf-8") as f:
            with open('MaterialsScienceTpoic.json', 'a+', encoding="utf-8") as f:
                f.write(lines)
                f.write('\n')
