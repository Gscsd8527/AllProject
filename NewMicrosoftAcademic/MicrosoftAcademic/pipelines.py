# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime
class MicrosoftacademicPipeline(object):

    def process_item(self, item, spider):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        hour = datetime.datetime.today().strftime('%H')
        lines = json.dumps(dict(item), ensure_ascii=False)
        if '01' <= hour <= '09':
            end = '1'
        elif '09' < hour <= '18':
            end = '2'
        elif hour > '18':
            end = '3'
        else:
            end = '4'
        date_hour = date + '-' + end
        # with open('/json_data/'+date_hour + 'ReferenceData.json', 'a+', encoding="utf-8") as f:
        with open('ReferenceData.json', 'a+', encoding="utf-8") as f:
            f.write('{}\n'.format(lines))



