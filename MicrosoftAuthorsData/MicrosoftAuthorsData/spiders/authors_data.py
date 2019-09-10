# -*- coding: utf-8 -*-
import scrapy
import json
import uuid

class AuthorsDataSpider(scrapy.Spider):
    name = 'authors_data'
    allowed_domains = ['https://academic.microsoft.com']
    start_urls = ['http://https://academic.microsoft.com/']
    AuthorsSet = []
    def __init__(self):
        self.url = 'https://academic.microsoft.com/api/entity/author/{}?paperId=undefined'
        self.referer_url = 'https://academic.microsoft.com/author/{}/publication/search?q={}&qe=Composite(AA.AuId={})&f=&orderBy=0'
        self.headers = {
            'Accept': 'application/json',
            # 'Referer': 'https://academic.microsoft.com/authors/',
            'X-Requested-With': 'Fetch',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        self.AuthorsData = self.getAuthorsData()
    def start_requests(self):
        for author in self.AuthorsData:
            author_id = author['id']
            author_name = author['name']
            if author_id not in self.AuthorsSet:
                self.AuthorsSet.append(author_id)
                url = self.url.format(author_id)
                referer = self.referer_url.format(author_id, author_name, author_id)
                headers = self.headers.copy()
                headers['Referer'] = referer
                yield scrapy.Request(url, headers=headers, meta={'init': author, 'url': self.url}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        body = response.body
        init_data = response.meta['init']
        url = response.meta['url']
        data_json = json.loads(body)
        name = data_json['entity']['dn']
        id = data_json['entity']['id']
        description = data_json['entity']['d']
        organization = {}
        try:
            organization_name = data_json['entity']['ci']['dn']
            organization_id = data_json['entity']['ci']['id']
            lat = data_json['entity']['ci']['lat']
            lon = data_json['entity']['ci']['lon']
            organization = {
                'organization_name': organization_name,
                'organization_id': organization_id,
                'lat': lat,
                'lon': lon,
            }
        except:
            pass
        author_img = ''
        try:
            author_img = data_json['entity']['iurl']
        except:
            pass
        author_fiurl = ''
        try:
            author_fiurl = data_json['entity']['fiurl']
        except:
            pass

        publications = data_json['entity']['pc']
        citations = data_json['entity']['eccnt']
        tags = [i['id'] for i in data_json['entity']['t']]
        reference_list = []
        try:
            reference_list = data_json['entity']['w']
        except:
            pass
        uid = uuid.uuid1()
        suid = str(uid).replace('-', '')
        author_data = {
            'datasetId': suid,
            'name': name,
            'id': id,
            'description': description,
            'organization': organization,
            'author_img': author_img,
            'author_fiurl': author_fiurl,
            'publications': publications,
            'citations': citations,
            'tags': tags,
            'reference_list': reference_list,
            'url': url,
            'init_data': init_data,
            'data_json': data_json,
        }
        yield author_data

    @staticmethod
    def getAuthorsData():
        AuthorsId = []
        f = open('BiologyAuthorsID.json', 'r', encoding='utf-8')
        # f = open('aa.json', 'r', encoding='utf-8')
        data = f.read()
        data_list = data.split('\n')
        for dt in data_list:
            if len(dt):
                data_json = json.loads(dt)
                AuthorsId.append(data_json)
        return AuthorsId
