# -*- coding: utf-8 -*-
import scrapy
import re
from MasterSpider.items import MasterspiderItem
class MymasterSpider(scrapy.Spider):
    name = 'MyMaster'
    allowed_domains = ['bj.zu.ke.com']
    start_urls = ['https://bj.zu.ke.com/zufang/rs%E5%8C%97%E4%BA%AC/']

    # def __init__(self):
    #     self.start_urls = 'https://bj.zu.ke.com/zufang/pg{}rs%E5%8C%97%E4%BA%AC/#contentList'
    #     self.pageNum = 36
    #     self.urlList = []
    #     for num in range(1, self.pageNum + 1):
    #         url = self.start_urls.format(num)
    #         self.urlList.append(url)
    def parse(self, response):
        start_urls = 'https://bj.zu.ke.com/zufang/pg{}rs%E5%8C%97%E4%BA%AC/#contentList'
        pageNum = 60
        urlList = []
        for num in range(1, pageNum + 1):
            url = start_urls.format(str(num))
            urlList.append(url)
        item = MasterspiderItem()
        for url in urlList:
            item['url'] = url
            yield item
        # item = MasterspiderItem()
        # id = 0
        # for url in self.urlList:
        #     item['id'] = id
        #     item['url'] = url
        #     yield item
        #     id += 1
    # def start_requests(self):
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    #     }
    #     for url in self.urlList:
    #         yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)
    #
    # def parse(self, response):
    #     count_data = response.xpath('//div[@class="content__list"]/div[@class="content__list--item"]')
    #     for data in count_data:
    #         company = data.xpath('.//p[@class="content__list--item--brand oneline"]/text()').extract_first()
    #         re_compile = re.compile(".*?([\u4E00-\u9FA5].*)")
    #         company = re.findall(re_compile, company)[0].strip(" ")  # 公司名
    #         addr_str = data.xpath('.//p[@class="content__list--item--title twoline"]/a/text()').extract_first()
    #         addr_str = re.findall(re_compile, addr_str)[0].strip(" ")
    #         rental = ''
    #         if '· ' in addr_str:
    #             addr_str = addr_str.replace('· ', '').strip(" ")
    #             rental = addr_str[:2]  # 整租或者合租
    #             addr = addr_str[2:].strip(" ")  # 房屋所在的小区
    #         else:
    #             addr = addr_str.split(' ', 1)[1].strip(" ")
    #         area = data.xpath('.//p[@class="content__list--item--des"]/text()').extract()
    #         mianji = ''  # 房屋面积
    #         geshi = ''  # 房屋格式 几室几厅
    #         for i in area:
    #             if "㎡" in i:
    #                 re_compile = re.compile('.*?([\d].*㎡)')
    #                 mianji = re.findall(re_compile, i)[0]
    #             if '室' in i:
    #                 re_compile = re.compile('.*?([\d].*[\u4E00-\u9FA5])')
    #                 geshi = re.findall(re_compile, i)[0]
    #         price = data.xpath('.//span[@class="content__list--item-price"]/em/text()').extract_first()  # 月租
    #         print(company, rental, addr, mianji, geshi, price)
    #         info = {}
    #         info['company'] = company
    #         info['rental'] = rental
    #         info['addr'] = addr
    #         info['mianji'] = mianji
    #         info['geshi'] = geshi
    #         info['price'] = price
    #         yield info


