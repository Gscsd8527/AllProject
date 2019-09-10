# -*- coding: utf-8 -*-
import scrapy
import json

class AuthorsidSpider(scrapy.Spider):
    name = 'authorsId'
    allowed_domains = ['https://academic.microsoft.com']
    start_urls = ['https://academic.microsoft.com/']

    def __init__(self):
        self.url = 'https://academic.microsoft.com/api/analytics/authors/topauthors?topicId={}&take=100&filter=1&dateRange=1'
        self.referer_url = 'https://academic.microsoft.com/authors/'
        self.headers = {
            'Accept': 'application/json',
            # 'Content-Type': 'application/json; charset=utf-8',
            'X-Requested-With': 'Fetch',
        }
        self.AuthorsId = self.getTopicHie()

    def start_requests(self):
        print('=========authorsId=========')
        for author in self.AuthorsId:
            # print('author= ', author)
            author_idlist = author['id_list']
            referer_url = self.getReferer(author_idlist)
            headers = self.headers.copy()
            headers['Referer'] = referer_url
            url = self.url.format(author_idlist[-1])
            # print('---', url)
            # print('===', referer_url)
            yield scrapy.Request(url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """
        解析响应的数据，直接往pipelines中抛数据
        :param response:
        :return:
        """
        body = response.body
        data_json = json.loads(body)
        for data in data_json:
            yield data

    @staticmethod
    def getTopicHie():
        """
        从文件中获取层级结构关系
        :return:
        """
        AuthorsId = []
        f = open('BiologyAuthors.json', 'r', encoding='utf-8')
        data = f.read()
        data_list = data.split('\n')
        for dt in data_list:
            if len(dt):
                data_json = json.loads(dt)
                AuthorsId.append(data_json)
        return AuthorsId

    @staticmethod
    def getReferer(id_list):
        referer_url = 'https://academic.microsoft.com/authors/'
        ids = [str(i) for i in id_list]
        id_len = len(ids)
        referer = ''
        if id_len == 1:
            referer = referer_url + ids[0]
        elif id_len > 1:
            id_str = ','.join(ids)
            id_new_str = id_str.strip(',')
            referer = referer_url + id_new_str
        return referer
