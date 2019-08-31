# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import datetime
from Zenodo.items import ZenodoItem
class ZenodoSpider(scrapy.Spider):
    name = 'zenodo_dataset'
    allowed_domains = ['zenodo.org']
    start_urls = ['http://zenodo.org/']

    def start_requests(self):
        headers = {
            'Accept': 'application/vnd.zenodo.v1+json',
        }
        init_url = 'https://zenodo.org/api/records/?page=1&size=20'
        headers['Referer'] = 'https://zenodo.org/search?page=1&size=20'
        response = requests.get(init_url, headers=headers)
        if response.status_code == 200:
            text = response.text
            data_json = json.loads(text)
            # 关键词 type
            typeAndNumsData = data_json['aggregations']['type']['buckets']
            Type = 'type'
            # print(typeAndNumsData)
            for item in typeAndNumsData:
                if item['key'] == 'dataset':
                    key = item['key']
                    count = item['doc_count']
                    k_v = {'key': key, 'count': count}
                    # print('k_v = ', k_v)
                    pages = getPageNums(count)
                    # print('总共有  {}   页'.format(pages))
                    # pages = 2
                    for page in range(500, pages+1):
                        url = 'https://zenodo.org/api/records/?page={}&size=20&{}={}'.format(page, Type, key)
                        if page == 1:
                            Referer = 'https://zenodo.org/search?page=1&size=20'
                        else:
                            Referer = 'https://zenodo.org/search?page={}&size=20&{}={}'.format(page-1, Type, key)
                        yield scrapy.Request(url, headers={'Referer': Referer}, callback=self.parse, dont_filter=False)
                # getDatasetData(key, count)
                
    def parse(self, response):
        text = response.body
        data = json.loads(text)
        print('json_data = ', data)
        items = data['hits']['hits']
        spiderDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in items:
            source_data = item
            name = item['metadata']['title']
            creators = item['metadata']['creators']
            description = item['metadata']['description']
            update_time = item['updated']
            access_right = item['metadata']['access_right']
            create_time = item['created']
            id = item['id']
            url = item['links']['html']
            version = item['revision']
            resource_type = item['metadata']['resource_type']['type']
            file_url = {}
            try:
                files = item['files']
                index = 1
                for file in files:
                    file_name = file['key']
                    file_size = file['size']
                    download_url = file['links']['self']
                    temp_dict = {
                        'file_name': file_name,
                        'file_size': file_size,
                        'download_url': download_url
                    }
                    file_url[str(index)] = temp_dict
                    index += 1
            except:
                pass
            publication_date = item['metadata']['publication_date']
            doi = item['metadata']['doi']
            communities = ''
            try:
                communities = item['metadata']['communities']['id']
            except:
                pass
            license = ''
            try:
                license = item['metadata']['license']['id']
            except:
                pass
            data_json = {
                'name': name,
                'creators': creators,
                'description': description,
                'update_time': update_time,
                'access_right': access_right,
                'create_time': create_time,
                'id': id,
                'version': version,
                'resource_type': resource_type,
                'file_url': file_url,
                'publication_date': publication_date,
                'url': url,
                'doi': doi,
                'communities': communities,
                'license': license,
                'source_data': source_data,
                'spiderDateTime': spiderDateTime,
            }
            items_dict = ZenodoItem()
            for k, v in data_json.items():
                items_dict[k] = v
            yield items_dict
            



def getPageNums(counts):
    """
    通过关键字的个数来判断页数
    :return:
    """
    pages = counts // 20
    pages_ys = counts % 20
    if pages_ys > 1:
        pages += 1
    return pages