# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MicrosoftacademicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    datasetInformation = scrapy.Field()
    date = scrapy.Field()
    authors = scrapy.Field()
    tags = scrapy.Field()
    citations = scrapy.Field()
    related_pages = scrapy.Field()
    id = scrapy.Field()
    reference_dict = scrapy.Field()
    references_num = scrapy.Field()
    cited_num = scrapy.Field()
    cited_jsondata = scrapy.Field()
    related_jsondata = scrapy.Field()
    references_jsondata = scrapy.Field()


