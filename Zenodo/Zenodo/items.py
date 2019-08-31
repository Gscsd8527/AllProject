# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZenodoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    # keyWord = scrapy.Field()
    key = scrapy.Field()
    creators = scrapy.Field()
    description = scrapy.Field()
    update_time = scrapy.Field()
    access_right = scrapy.Field()
    create_time = scrapy.Field()
    id = scrapy.Field()
    version = scrapy.Field()
    resource_type = scrapy.Field()
    file_url = scrapy.Field()
    publication_date = scrapy.Field()
    url = scrapy.Field()
    doi = scrapy.Field()
    communities = scrapy.Field()
    license = scrapy.Field()
    source_data = scrapy.Field()
    spiderDateTime = scrapy.Field()

