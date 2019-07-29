# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from MicrosoftAcademic.items import MicrosoftacademicItem
import logging

class MicrosoftSpider(scrapy.Spider):
    name = 'microsoft'
    allowed_domains = ['https://academic.microsoft.com']
    start_urls = ['http://https://academic.microsoft.com/']

    def __init__(self):
        # self.KeyWord = ["Psychology", "Political science", "Mathematics", "Environmental science", "Computer science",
        #                 "Medicine", "Biology", "History", "Physics", "Geology", "Engineering", "Philosophy", "Art",
        #                 "Sociology", "Business", "Economics", "Chemistry", "Materials science", "Geography"]
        self.KeyWord = ["Visual modularity", ]
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            # 'Referer': 'https://academic.microsoft.com/search?q=Medicine&f=&orderBy=0&skip=0&take=10',
            'X-Requested-With': 'Fetch',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        self.url = 'https://academic.microsoft.com/api/search'
        self.data = {
            "query": '',
            "queryExpression": "",
            "filters": [],
            "orderBy": 0,
            "skip": 0,
            "sortAscending": 'true',
            "take": 10,
            "includeCitationContexts": 'false'
        }
    def start_requests(self):
        for key in self.KeyWord:
            referer = 'https://academic.microsoft.com/search?q=Medicine&f=&orderBy=0&skip=0&take=10'
            self.headers['Referer'] = referer
            data = self.data
            data['query'] = key
            print('url= ', self.url)
            yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=json.dumps(data), meta={'key': key}, callback=self.FirstParse, dont_filter=True)

    def FirstParse(self, response):
        # print('++++++++++++parse++++++++++++++++')
        body = response.body
        key = response.meta['key']
        json_data = json.loads(body)
        data_list = json_data['pr']
        # 翻页数量
        Nums = json_data['t']
        print('Nums= ', Nums)
        pages = Nums // 10
        pages_ys = Nums % 10
        if pages_ys > 0:
            pages += 1
        # for num in range(pages):
        for num in range(3):
            print('num的值= ', num)
            if num == 0:
                print('data_list= ', data_list)
                for dt in data_list:
                    paper = dt['paper']
                    # 名称
                    name = paper['dn']
                    # 时间
                    date = paper['v']['publishedDate']
                    # 作者
                    # authors = [author['dn'] for author in paper['a']]
                    author_information = {}
                    author_index = 1
                    for information in paper['a']:
                        author_name = information['dn']
                        author_sources = information['i']
                        temp_list = []
                        temp_dict = {}
                        for author in author_sources:
                            author_source = ''
                            try:
                                author_source = author['dn']
                            except Exception as e:
                                pass
                            temp_list.append(author_source)
                        temp_dict[str(author_index)] = {
                            'author_name': author_name,
                            'author_source': temp_list
                        }
                        author_index += 1
                        author_information.update(temp_dict)

                    # 标签
                    tags = [tag['dn'] for tag in paper['fos']]
                    # 引文数量
                    citations = paper['eccnt']
                    # 关联关系页数
                    related_pages = paper['et']
                    # name_id
                    name_id = paper['id']
                    # 数据集介绍
                    datasetInformation = ''
                    try:
                        datasetInformation = paper['d']
                    except:
                        pass

                    page_dict = {
                        'name': name,
                        'datasetInformation': datasetInformation,
                        'date': date,
                        'authors': author_information,
                        'tags': tags,
                        'citations': citations,
                        'related_pages': related_pages,
                        'id': name_id
                    }
            # else:
            #     pass
            #         print('page_dict= ', page_dict)
                    reference_url = 'https://academic.microsoft.com/api/entity/{}?entityType=2'.format(page_dict['id'])
                    reference_headers = self.headers.copy()
                    reference_headers.pop('Content-Type')
                    reference_headers['Referer'] = 'https://academic.microsoft.com/paper/{}/reference'.format(page_dict['id'])
                    meta = {
                        'page_dict': page_dict
                    }
                    yield scrapy.Request(reference_url, method='GET', headers=reference_headers, meta=meta, callback=self.ReferenceParse, dont_filter=True)
            else:
                referer = 'https://academic.microsoft.com/search?q=Medicine&f=&orderBy=0&skip={}&take=10'.format(num*10)
                self.headers['Referer'] = referer
                data = self.data.copy()
                data['query'] = key
                yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=json.dumps(data), callback=self.TwoParse, dont_filter=True)

    def TwoParse(self, response):
        body = response.body
        json_data = json.loads(body)
        data_list = json_data['pr']
        for dt in data_list:
            paper = dt['paper']
            # 名称
            name = paper['dn']
            # 时间
            date = paper['v']['publishedDate']
            # 作者
            # authors = [author['dn'] for author in paper['a']]
            author_information = {}
            author_index = 1
            for information in paper['a']:
                author_name = information['dn']
                author_sources = information['i']
                temp_list = []
                temp_dict = {}
                for author in author_sources:
                    author_source = ''
                    try:
                        author_source = author['dn']
                    except Exception as e:
                        pass
                    temp_list.append(author_source)
                temp_dict[str(author_index)] = {
                    'author_name': author_name,
                    'author_source': temp_list
                }
                author_index += 1
                author_information.update(temp_dict)

            # 标签
            tags = [tag['dn'] for tag in paper['fos']]
            # 引文数量
            citations = paper['eccnt']
            # 关联关系页数
            related_pages = paper['et']
            # name_id
            name_id = paper['id']
            # 数据集介绍
            datasetInformation = ''
            try:
                datasetInformation = paper['d']
            except:
                pass
            page_dict = {
                'name': name,
                'datasetInformation': datasetInformation,
                'date': date,
                'authors': author_information,
                'tags': tags,
                'citations': citations,
                'related_pages': related_pages,
                'id': name_id
            }
            reference_url = 'https://academic.microsoft.com/api/entity/{}?entityType=2'.format(page_dict['id'])
            reference_headers = self.headers.copy()
            reference_headers.pop('Content-Type')
            reference_headers['Referer'] = 'https://academic.microsoft.com/paper/{}/reference'.format(page_dict['id'])
            meta = {
                'page_dict': page_dict
            }
            yield scrapy.Request(reference_url, method='GET', headers=reference_headers, meta=meta,
                                 callback=self.ReferenceParse, dont_filter=True)

    def ReferenceParse(self, responses):
        """
        有的论文有下载的文件，需要将他们保存下来,
        其中包含了两个需要的值：
                文件：
                下一次请求的queryExpression的值
        :param responses:
        :return:
        """
        # print('===========ReferenceParse============')
        reference_data = responses.body
        page_dict = responses.meta['page_dict']
        reference_jsondata = json.loads(reference_data)

        reference_dict = getReference(reference_jsondata)
        page_dict['reference_dict'] = reference_dict

        # 关联的 PaperExpression 的值
        relatedPaperExpression = reference_jsondata['relatedPaperExpression']

        data = self.data
        temp_dict = {
            'includeCitationContexts': 'true',
            'parentEntityId': page_dict['id'],
            'query': page_dict['name'],
            # 'queryExpression': queryExpression,
        }
        data.update(temp_dict)
        headers = self.headers
        headers['Referer'] = 'https://academic.microsoft.com/paper/{}/citedby/search?q={}&qe=RId%3D{}&f=&orderBy=0'.format(
            page_dict['id'], page_dict['name'], page_dict['id'])

        # 有reference的话那么queryExpression的值是paperReferencesExpression
        # 没有的话那么queryExpression的值是entityExpression
        try:
            queryExpression = reference_jsondata['paperReferencesExpression']
            is_references = 1
        except:
            # queryExpression = reference_jsondata['entityExpression']
            queryExpression = 'RId=' + str(page_dict['id'])
            is_references = 0
            # print('except queryExpression=', queryExpression)
        temp_dict['queryExpression'] = queryExpression
        data.update(temp_dict)
        meta = {
            'page_dict': page_dict,
            'is_references': is_references,
            'data': data.copy(),  # 这个地方一定要加copy,不然的话会被后面的值给跟新掉
            'relatedPaperExpression': relatedPaperExpression
        }
        yield scrapy.Request(self.url, method='POST', headers=headers, body=json.dumps(data), meta=meta, callback=self.ParseIsHaveReferences, dont_filter=True)

    def ParseIsHaveReferences(self, responses):
        """
        解析包含references的论文
        :param response:
        :return:
        """
        # print('**********PageParse************')
        page_dict = responses.meta['page_dict']
        is_references = responses.meta['is_references']
        data = responses.meta['data']
        relatedPaperExpression = responses.meta['relatedPaperExpression']

        page_data = responses.body
        json_data = json.loads(page_data)

        request_data = data.copy()
        # print('PAGE_DICT= ', page_dict)
        microsoft_datajson = page_dict.copy()
        # 判断是否有references
        references_jsondata = {}
        references_num = 0
        if is_references:
            # print('包含references===========')
            references_num = json_data['t']
            page_dict['references_num'] = references_num
            # print('references_num= ', references_num)
            # for i in range(references_num):
            references_jsondata = getReferencesData(references_num, page_dict, self.headers, self.url, request_data)

            # for i in range(1, 3):
            #     if i == 1:
            #         references_json = parsePaperContent(1, json_data)
            #         print('references= ', references_json)
            #         references_jsondata.update(references_json)
            #     else:
            #         skip = (i - 1) * 10
            #         request_data['skip'] = skip
            #         headers = self.headers
            #         headers['Referer'] = 'https://academic.microsoft.com/paper/{}/reference/search?q={}&qe={}&f=&orderBy=0&skip={}&take=10'.format(page_dict['id'], page_dict['name'], data['queryExpression'], skip)
            #         temp_references_dict = parseNextPage(self.url, headers, request_data, i)
            #         references_jsondata.update(temp_references_dict)

            # print('references_jsondata= ', references_jsondata)

            # 将references的data的queryExpression更换掉，方便后面获取cited和related
            request_data['queryExpression'] = 'RId=' + str(page_dict['id'])

        cited_num = int(json_data['t'])
        # print('cited_num=', cited_num)
        # 循环得到cited
        # cited_data = data.copy()
        # for i in range(cited_num):
        cited_jsondata = getCitedByData(cited_num, page_dict, self.headers, self.url, request_data)
        # print('cited_jsondata= ', cited_jsondata)
        # for i in range(1, 4):
        #     if i == 1:
        #         try:
        #             cited_json = parsePaperContent(1, json_data)
        #             print('cited_json= ', cited_json)
        #             cited_jsondata.update(cited_json)
        #         except Exception as e:
        #             print('cited = ', e)
        #     if i != 1:
        #         skip = (i-1) * 10
        #         cited_data['skip'] = skip
        #         headers = self.headers
        #         headers['Referer'] = 'https://academic.microsoft.com/paper/{}/citedby/search?q={}&qe=RId%3D{}&f=&orderBy=0&skip={}&take=10'.format(page_dict['id'], page_dict['name'], page_dict['id'], skip)
        #         temp_cited_dict = parseNextPage(self.url, headers, cited_data, i)
        #         cited_jsondata.update(temp_cited_dict)
        # print('cited_jsondata= ', cited_jsondata)

        # 循环得到related, 这个值是页数
        related_pages = int(page_dict['related_pages'])
        # related_data = data.copy()
        related_jsondata = getRelatedData(related_pages, request_data, page_dict, self.headers, self.url, relatedPaperExpression)
        # print('related_jsondata= ', related_jsondata)
        # print('related_pages= ', related_pages, type(related_pages))
        # for i in range(1, related_pages+1):
        #     skip = (i-1) * 10
        #     related_data['skip'] = skip
        #     related_data['queryExpression'] = relatedPaperExpression
        #     headers = self.headers
        #     headers['Referer'] = 'https://academic.microsoft.com/paper/{}/related/search?q={}&qe={}&f=&orderBy=0&skip={}&take=10'.format(page_dict['id'], page_dict['name'], relatedPaperExpression, skip)
        #     temp_related_dict = parseNextPage(self.url, headers, related_data, i)
        #     related_jsondata.update(temp_related_dict)
        # print('related_jsondata= ', related_jsondata)
        temp_dict = {
            'references_num': references_num,
            'cited_num': cited_num,
            'references_jsondata': references_jsondata,
            'cited_jsondata': cited_jsondata,
            'related_jsondata': related_jsondata,
        }
        microsoft_datajson.update(temp_dict.copy())
        # print('microsoft_datajson= ', microsoft_datajson)
        items = MicrosoftacademicItem()
        for k, v in microsoft_datajson.items():
            items[k] = v
        yield items



def parseNextPage(url, headers, cited_data, index):
    """
    解析下一页得到数据，其中包括references、cited by、 related的翻页
    :return:
    """
    # print('=========citedPage=========')
    response = requests.post(url, headers=headers, data=json.dumps(cited_data))
    data = ''
    if response.status_code == 200:
        text = response.text
        data_json = json.loads(text)
        data = parsePaperContent(index, data_json)
        # print('data= ', data)
    else:
        pass
        # print('cited 错误响应码为： ', response.status_code)
    return data

def getReference(reference_jsondata):
    """
    解析得到ViewPDF、Website、AdditionalLink
    :param reference_jsondata:
    :return:
    """
    reference_dict = {
        'ViewPDF': [],
        'Website': [],
        'AdditionalLink': []
    }
    try:
        reference_list = reference_jsondata['entity']['s']
        for i in reference_list:
            index = i['sourceType']
            if index == 0 or index == '0':
                reference_dict['AdditionalLink'].append(i['link'])
            if index == 1 or index == '1':
                reference_dict['Website'].append(i['link'])
            if index == 3 or index == '3':
                reference_dict['ViewPDF'].append(i['link'])
    except Exception as e:
        pass
        # print('referer= ', e)
    # print('reference_dict= ', reference_dict)
    return reference_dict

def parsePaperContent(parse_index, data):
    """
    解析论文的内容， 其中包括references、cited by、 related
    :return:
    """
    print('=======parseCitedContent=======')
    cited_json = {}
    try:
        papers = data['pr']
        # print('papers= ', papers)

        index = (parse_index - 1) * 10 + 1
        # if parse_index > 0:
        #     index = (parse_index-1) * 10 + 1
        # else:
        #     index = parse_index * 10 + 1
        for paper in papers:
            paper = paper['paper']
            name = paper['dn']
            # 时间
            date = paper['v']['publishedDate']
            displayName = ''
            try:
                displayName = paper['v']['displayName']
            except Exception as e:
                pass
            # 作者信息
            # authors = [author['dn'] for author in paper['a']]
            author_information = {}
            author_index = 1
            for information in paper['a']:
                author_name = information['dn']
                author_sources = information['i']
                temp_list = []
                temp_dict = {}
                for author in author_sources:
                    author_source = ''
                    try:
                        author_source = author['dn']
                    except Exception as e:
                        pass
                    temp_list.append(author_source)
                temp_dict[str(author_index)] = {
                    'author_name': author_name,
                    'author_source': temp_list
                }
                author_index += 1
                author_information.update(temp_dict)

            # 标签
            tags = [tag['dn'] for tag in paper['fos']]

            datasetInformation = ''
            try:
                datasetInformation = paper['d']
            except Exception as e:
                pass
                # print(e)
            cited_id = ''
            try:
                cited_id = paper['id']
            except:
                pass
            citations = ''
            try:
                citations = paper['eccnt']
            except:
                pass
            data_dict = {
                'name': name,
                'date': date,
                'displayName': displayName,
                'authors': author_information,
                'tags': tags,
                'datasetInformation': datasetInformation,
                'id': cited_id,
                'citations': citations
            }
            cited_json[str(index)] = data_dict
            index += 1
    except Exception as e:
        pass
    # print(cited_json)
    return cited_json


def getReferencesData(references_num, page_dict, headers, url, request_data):
    """
    获取references的数据
    :return:
    """
    references_jsondata = {}
    # 将个数转换成页数
    references_nums = references_num // 10
    references_nums_ys = references_num % 10
    if references_nums_ys > 0:
        references_nums += 1

    for i in range(1, references_nums):
    # for i in range(1, 3):
        skip = (i - 1) * 10
        request_data['skip'] = skip
        headers[
            'Referer'] = 'https://academic.microsoft.com/paper/{}/reference/search?q={}&qe={}&f=&orderBy=0&skip={}&take=10'.format(
            page_dict['id'], page_dict['name'], request_data['queryExpression'], skip)
        temp_references_dict = parseNextPage(url, headers, request_data, i)
        references_jsondata.update(temp_references_dict)
    return references_jsondata


def getCitedByData(cited_num, page_dict, headers, url, cited_data):
    """
    得到cited by 的数据
    :return:
    """
    cited_jsondata = {}

    cited_nums = cited_num // 10
    cited_nums_ys = cited_num % 10
    if cited_nums_ys > 0:
        cited_nums += 1

    for i in range(cited_nums):
    # for i in range(1, 4):
        skip = (i - 1) * 10
        cited_data['skip'] = skip
        headers[
            'Referer'] = 'https://academic.microsoft.com/paper/{}/citedby/search?q={}&qe=RId%3D{}&f=&orderBy=0&skip={}&take=10'.format(
            page_dict['id'], page_dict['name'], page_dict['id'], skip)
        temp_cited_dict = parseNextPage(url, headers, cited_data, i)
        cited_jsondata.update(temp_cited_dict)
    return cited_jsondata


def getRelatedData(related_pages, related_data, page_dict, headers, url, relatedPaperExpression):
    """
    获取related的数据
    :return:
    """
    related_jsondata = {}
    for i in range(1, related_pages + 1):
        skip = (i - 1) * 10
        related_data['skip'] = skip
        related_data['queryExpression'] = relatedPaperExpression
        # headers = self.headers
        headers[
            'Referer'] = 'https://academic.microsoft.com/paper/{}/related/search?q={}&qe={}&f=&orderBy=0&skip={}&take=10'.format(
            page_dict['id'], page_dict['name'], relatedPaperExpression, skip)
        temp_related_dict = parseNextPage(url, headers, related_data, i)
        related_jsondata.update(temp_related_dict)
    return related_jsondata