# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import copy

class AuthorsSpider(scrapy.Spider):
    name = 'yield_authors'
    allowed_domains = ['https://academic.microsoft.com']
    start_urls = ['http://https://academic.microsoft.com/']

    # AuthorsSet = set()

    def __init__(self):
        self.next_url = 'https://academic.microsoft.com/api/analytics/topics/hierarchy?topicPath='
        self.referer_url = 'https://academic.microsoft.com/authors/'
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'X-Requested-With': 'Fetch',
        }
    def start_requests(self):
        url = 'https://academic.microsoft.com/api/analytics/topics/hierarchy?topicPath='
        headers = self.headers.copy()
        headers['Referer'] = 'https://academic.microsoft.com/home'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            text = response.text
            data_json = json.loads(text)
            data_list = data_json['ct']
            for data in data_list[:1]:
                init_name = data['n']
                init_id = data['id']
                print('init_name= ', init_name)
                print('init_id= ', init_id)
                request_url = self.GenerateUrl(self.next_url, init_id)
                referer = self.GenerateRefererUrl(self.referer_url, init_id)
                headers = self.headers.copy()
                headers['Referer'] = referer
                meta = {
                    'data': data.copy(),
                    'initFiled': init_name,
                    'id': init_id
                }
                yield scrapy.Request(request_url, headers=headers, meta=meta, callback=self.NextRequestOne, dont_filter=True)

    def NextRequestOne(self, response):
        """
        第一层数据
        :param response:
        :return:
        """
        body = response.body
        resp_data = response.meta['data']
        data = copy.deepcopy(resp_data)
        initFiled = response.meta['initFiled']
        init_id = response.meta['id']
        data_json = json.loads(body)
        data_list = data_json['ct']
        for dt in data_list:
            first_id = dt['id']
            first_name = dt['n']
            print('第一层字段 ', first_name)
            dt.update({'next': ''})
            data.update({'next': copy.deepcopy(dt)})
            data_first = {
                initFiled: copy.deepcopy(data)
            }
            request_url = self.GenerateUrl(self.next_url, init_id, first_id)
            referer = self.GenerateRefererUrl(self.referer_url, init_id, first_id)
            headers = self.headers.copy()
            headers['Referer'] = referer
            meta = {
                'data': copy.deepcopy(data_first),
                'id': [init_id, first_id],
                'initFiled': initFiled,
                'oneFiled': first_name,
            }
            # yield scrapy.Request(request_url, headers=headers, meta=meta, callback=self.NextRequestTwo, dont_filter=True)
            yield scrapy.Request(request_url, headers=headers, meta=meta, callback=self.NextRequest, dont_filter=True)

    def NextRequest(self, response):
        print(response.meta)
        """
        下一层数据
        :param response:
        :return:
        """
        body = response.body
        resp_data = response.meta['data']
        data = resp_data.copy()
        id_lst = response.meta['id']
        initFiled = response.meta['initFiled']
        data_json = json.loads(body)
        data_list = data_json['ct']
        if len(data_list):
            for dt in data_list:
                next_id = dt['id']
                id_list = copy.deepcopy(id_lst)
                id_list.append(next_id)
                dt.update({'next': ''})
                data_update = copy.deepcopy(data)
                # data_update[initFiled]['next']['next'] = copy.deepcopy(dt)
                if len(id_list) == 3:
                    data_update[initFiled]['next']['next'] = copy.deepcopy(dt)
                elif len(id_list) == 4:
                    data_update[initFiled]['next']['next']['next'] = copy.deepcopy(dt)
                elif len(id_list) == 5:
                    data_update[initFiled]['next']['next']['next']['next'] = copy.deepcopy(dt)
                elif len(id_list) == 6:
                    data_update[initFiled]['next']['next']['next']['next']['next'] = copy.deepcopy(dt)
                elif len(id_list) == 7:
                    data_update[initFiled]['next']['next']['next']['next']['next']['next'] = copy.deepcopy(dt)
                elif len(id_list) == 8:
                    data_update[initFiled]['next']['next']['next']['next']['next']['next']['next'] = copy.deepcopy(dt)

                request_url = self.GenerateUrl(self.next_url, *id_list)
                referer = self.GenerateRefererUrl(self.referer_url, *id_list)
                headers = self.headers.copy()
                headers['Referer'] = referer
                meta = {
                    'data': data_update.copy(),
                    'id': id_list,
                    'initFiled': initFiled,
                }
                # yield scrapy.Request(request_url, headers=headers, meta=meta, callback=self.NextRequestThree, dont_filter=True)
                # if request_url not in self.AuthorsSet:
                # self.AuthorsSet.add(request_url)
                # yield scrapy.Request(request_url, headers=headers, meta=meta, callback=self.NextRequestThree, dont_filter=True)
                yield scrapy.Request(request_url, headers=headers, meta=meta, callback=self.NextRequest, dont_filter=True)
        else:
            items_data = copy.deepcopy(data)
            # items_data.update({'id_list': id_lst})
            items_data.update({'id_list': copy.deepcopy(id_lst)})
            yield items_data


    @staticmethod
    def GenerateUrl(init_url, *ids):
        """
        通过传过来的Id值生成请求的URL
        :param init_url:
        :param ids:
        :return:
        """
        ids = [str(i) for i in ids]
        id_len = len(ids)
        url = ''
        if id_len == 1:
            url = init_url + ids[0]
        elif id_len > 1:
            id_str = ','.join(ids)
            id_new_str = id_str.strip(',')
            url = init_url + id_new_str
        return url

    @staticmethod
    def GenerateRefererUrl(referer_url, *ids):
        """
        生成header头中referer
        :param referer_url:
        :param ids:
        :return:
        """
        ids = [str(i) for i in ids]
        id_len = len(ids)
        referer = ''
        if id_len == 1:
            referer = referer_url + ids[0]
        elif id_len > 1:
            id_str = ','.join(ids)
            id_new_str = id_str.strip(',')
            referer = referer_url + id_new_str
        return referer

