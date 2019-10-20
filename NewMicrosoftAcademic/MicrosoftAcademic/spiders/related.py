# -*- coding: utf-8 -*-
import scrapy
import json
import copy




class MicrosoftSpider(scrapy.Spider):
    name = 'related'
    allowed_domains = ['https://academic.microsoft.com']
    start_urls = ['http://https://academic.microsoft.com/']

    def __init__(self):
        self.url = 'https://academic.microsoft.com/api/search'
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            # 'Referer': 'https://academic.microsoft.com/search?q=Medicine&f=&orderBy=0&skip=0&take=10',
            'X-Requested-With': 'Fetch',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
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
    @staticmethod
    def getPaperNameId():
        f1 = open('paperIdData1.json', 'r', encoding='utf-8')
        j1 = set()
        while 1:
            try:
                data1 = json.loads(f1.readline().strip())
                # print('data1=', data1)
                j1.add('{}tanzhenhua{}tanzhenhua{}'.format(data1['name'], data1['id'], data1["relatedPaperExpression"]))
            except:
                break
        f1.close()
        print('j1=', len(j1))
        f2 = open('related.json', 'r', encoding='utf-8')
        j2 = set()
        while 1:
            try:
                data2 = json.loads(f2.readline().strip())
                # print('data2= ', data2)
                j2.add('{}tanzhenhua{}tanzhenhua{}'.format(data2['name'], data2['id'], data2["relatedPaperExpression"]))
            except:
                break
        f2.close()
        print('j2=', len(j2))
        countSet = j1 - j2
        print('countSet= ', len(countSet))
        return countSet

    def start_requests(self):
        PaperID = self.getPaperNameId()
        print('===================RELATED===========================', len(PaperID))
        for paper in PaperID:
            paper_list = paper.split('tanzhenhua')
            print('paper_list=', paper_list)
            paper_dict = {
                'name': paper_list[0],
                'id': paper_list[1],
                'relatedPaperExpression': paper_list[2],
            }
            paper_name = paper_dict['name']
            paper_id = paper_dict['id']
            relatedPaperExpression = paper_dict['relatedPaperExpression']
            if relatedPaperExpression != '':
                reference_data = copy.deepcopy(self.data)
                reference_data['query'] = paper_name
                reference_data['queryExpression'] = relatedPaperExpression
                reference_headers = copy.deepcopy(self.headers)
                meta = {
                    'init_data': paper_dict,
                    'type': 'Related',
                    'paper_name': paper_name,
                }
                yield scrapy.Request(self.url, method='POST', headers=reference_headers, meta=meta, body=json.dumps(reference_data), callback=self.ParseReferenceData, dont_filter=True)

    def ParseReferenceData(self, response):
        """
        抓取references的论文
        :param response:
        :return:
        """
        body = response.body
        init_data = response.meta['init_data']
        type = response.meta['type']
        paper_name = response.meta['paper_name']
        if response.status == 200:
            referer_data = {
                'name': init_data['name'],
                'id': init_data['id'],
                'relatedPaperExpression': init_data['relatedPaperExpression']
            }
            referer_string = json.dumps(referer_data, ensure_ascii=False)
            with open('related.json', 'a+', encoding='utf-8') as f:
                f.write('{}\n'.format(referer_string))
            data_json = json.loads(body)
            data_list = data_json['pr']
            Nums = data_json['t']
            print('related paper_name: {}, Nums: {}'.format(paper_name, Nums))
            pages = Nums // 10
            pages_ys = Nums % 10
            if pages_ys > 0:
                pages += 1
            print('related paper_name: {}, pages: {}'.format(paper_name, pages))
            # retlate 默认只有两页，既20个， 其实可以把 + 1 去掉
            # for num in range(pages + 1):
            for num in range(pages):
                if num == 0:
                    papers_list = self.ParsePaperData(data_list, init_data, type, num)
                    for sig_paper in papers_list:
                        yield sig_paper
                else:
                    next_headers = copy.deepcopy(self.headers)
                    next_headers['Referer'] = 'https://academic.microsoft.com/paper/{}/related/search?q={}&qe={}&f=&orderBy=0&skip={}&take=10'.format(init_data['id'], init_data['name'], init_data['relatedPaperExpression'], num*10)
                    next_data = copy.deepcopy(self.data)
                    next_data['query'] = paper_name
                    next_data['skip'] = num * 10
                    next_data['queryExpression'] = init_data['relatedPaperExpression']
                    meta = {
                        'init_data': init_data,
                        'type': type,
                        'num': num,
                    }
                    yield scrapy.Request(url=self.url, method='POST', headers=next_headers, body=json.dumps(next_data), meta=meta,
                                          callback=self.PargeTurning, dont_filter=True)

    def PargeTurning(self, response):
        """
        翻页
        :param response:
        :return:
        """

        body = response.body
        init_data = response.meta['init_data']
        type = response.meta['type']
        num = response.meta['num']
        print('related 这是 {} 第 {} 页'.format(init_data['name'], num))
        data_json = json.loads(body)
        data_list = data_json['pr']
        papers_list = self.ParsePaperData(data_list, init_data, type, num)
        for sig_paper in papers_list:
            yield sig_paper


    @staticmethod
    def ParsePaperData(papers, init_data, type, num):
        papers_list = []
        for sing_paper in papers:
            paper = sing_paper['paper']
            # 名称
            name = paper['dn']
            id = paper['id']
            # 数据集介绍
            datasetInformation = paper['d']
            # 时间
            date = paper['v']['publishedDate']
            displayName = ''
            try:
                displayName = paper['v']['displayName']
            except:
                pass
            # 作者
            author_information = []
            for information in paper['a']:
                au_name = information['dn']
                au_id = information['id']
                org_sources = information['i']
                temp_list = []
                for organ in org_sources:
                    author_source = {}
                    try:
                        author_source['organization_name'] = organ['dn']
                        author_source['organization_id'] = organ['id']
                        author_source['lat'] = organ['lat']
                        author_source['lon'] = organ['lon']
                    except Exception as e:
                        pass
                    temp_list.append(copy.deepcopy(author_source))
                    temp_dict = {
                        'author_name': au_name,
                        'author_id': au_id,
                        'author_source': copy.deepcopy(temp_list)
                    }
                    author_information.append(copy.deepcopy(temp_dict))
            # 标签
            tags = [{'name': tag['dn'], 'id': tag['id']} for tag in paper['fos']]
            # 引文数量
            citations = paper['eccnt']
            # 关联关系页数
            related_pages = paper['et']

            reference_dict = {}
            try:
                reference_dict = getRefererLink(paper['s'])
            except:
                pass

            paper_data = {
                'init_data': init_data,
                'type': type,
                'num': num+1,
                'name': name,
                'id': id,
                'datasetInformation': datasetInformation,
                'date': date,
                'displayName': displayName,
                'authors': author_information,
                'tags': tags,
                'citations': citations,
                'related_pages': related_pages,
                'reference_dict': reference_dict,
                'source_data': sing_paper,
            }
            papers_list.append(paper_data)
        return papers_list


def getRefererLink(reference_list):
    reference_dict = {
        'ViewPDF': [],
        'Website': [],
        'AdditionalLink': []
    }
    for i in reference_list:
        index = i['sourceType']
        if index == 0 or index == '0':
            reference_dict['AdditionalLink'].append(i['link'])
        if index == 1 or index == '1':
            reference_dict['Website'].append(i['link'])
        if index == 3 or index == '3':
            reference_dict['ViewPDF'].append(i['link'])
    return reference_dict


