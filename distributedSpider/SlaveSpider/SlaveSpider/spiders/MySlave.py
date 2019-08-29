# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import re
from SlaveSpider.items import SlavespiderItem
class MyslaveSpider(RedisSpider):
    name = 'MySlave'
    allowed_domains = ['bj.zu.ke.com']
    redis_key = 'MasterSpider:start_urls'
    def parse(self, response):
        # headers = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'zh-CN,zh;q=0.9',
        #     'Cache-Control': 'max-age=0',
        #     'Connection': 'keep-alive',
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        # }
        print('------------------------------')
        count_data = response.xpath('//div[@class="content__list"]/div[@class="content__list--item"]')
        for data in count_data:
            company = data.xpath('.//p[@class="content__list--item--brand oneline"]/text()').extract_first()
            re_compile = re.compile(".*?([\u4E00-\u9FA5].*)")
            company = re.findall(re_compile, company)[0].strip(" ")  # 公司名
            addr_str = data.xpath('.//p[@class="content__list--item--title twoline"]/a/text()').extract_first()
            addr_str = re.findall(re_compile, addr_str)[0].strip(" ")
            rental = ''
            if '· ' in addr_str:
                addr_str = addr_str.replace('· ', '').strip(" ")
                rental = addr_str[:2]  # 整租或者合租
                addr = addr_str[2:].strip(" ")  # 房屋所在的小区
            else:
                addr = addr_str.split(' ', 1)[1].strip(" ")
            area = data.xpath('.//p[@class="content__list--item--des"]/text()').extract()
            mianji = ''  # 房屋面积
            geshi = ''  # 房屋格式 几室几厅
            for i in area:
                if "㎡" in i:
                    re_compile = re.compile('.*?([\d].*㎡)')
                    mianji = re.findall(re_compile, i)[0]
                if '室' in i:
                    re_compile = re.compile('.*?([\d].*[\u4E00-\u9FA5])')
                    geshi = re.findall(re_compile, i)[0]
            price = data.xpath('.//span[@class="content__list--item-price"]/em/text()').extract_first()  # 月租
            # info = SlavespiderItem()
            info = {}
            info['company'] = company
            info['rental'] = rental
            info['addr'] = addr
            info['mianji'] = mianji
            info['geshi'] = geshi
            info['price'] = price
            print(info)
            # yield info
