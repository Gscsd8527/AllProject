# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime
class MicrosoftauthorsPipeline(object):
    def process_item(self, item, spider):
        # date = datetime.datetime.today().strftime('%Y-%m-%d')
        lines = json.dumps(dict(item), ensure_ascii=False)
        # with open(date + 'Authors.json', 'a+', encoding="utf-8") as f:
        with open('Authors.json', 'a+', encoding="utf-8") as f:
            f.write(lines)
            f.write('\n')
        # return item
