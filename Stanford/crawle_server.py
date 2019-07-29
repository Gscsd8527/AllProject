import requests
from lxml import etree
import re
import pymongo
import json
import uuid

myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = myclient['Stanford']  # 数据库
mycol = mydb['Stanford_data']  # 表


BASE_URL = 'http://snap.stanford.edu/data/'

DATA_JSON = {
    'Name': '',
    'Type': '',
    'Nodes': '',
    'Edges': '',
    'Communities': '',
    'Description': '',
    'Temporal Edges': '',
    'Static Edges': '',
    'Number of items': '',
    'url': '',
}


def parseUrl(url, json_data):
    datasetInformation = ''
    datasetStatistic = {}
    citation = ''
    file = {}
    dataFormat = {}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            html_str = html.replace('\n', '').replace('\r', '')
            try:
                #  Dataset information
                # re_compile = re.compile('<div id="right-column">(.*?)<table id="datatab"')
                re_compile = re.compile('<div id="right-column">.*?</h3>.*?(.*?)<table id="datatab"')
                datasetInformation_text = re.findall(re_compile, html_str)[0]
                dataset_list = re.findall('>(.*?)<', datasetInformation_text)
                datasetInformation = ''.join(dataset_list)
            except Exception as e:
                print(e)
            # print('datasetInformation= ', datasetInformation)
            try:
                datasetStatistic_html = etree.HTML(html)
                datasetStatistic_data = datasetStatistic_html.xpath('//table[@id="datatab" and @summary="Dataset statistics"]')
                for table in datasetStatistic_data:
                    statistics_tr = table.xpath('.//tr')
                    statistics_title = statistics_tr[0].xpath('./th/text()')[0]
                    statistics_text = statistics_tr[1:]
                    temp = {}
                    for tr in statistics_text:
                        try:
                            name = tr.xpath('./td[1]/text()')
                            value = tr.xpath('./td[2]/text()')
                            if len(name):
                                name = name[0]
                            if len(value):
                                value = value[0]
                            temp[name] = value
                        except:
                            pass
                    datasetStatistic[statistics_title] = temp
            except Exception as e:
                print('==', e)
            # print('datasetStatistic = ', datasetStatistic)
            try:
                re_citation = re.compile('<h3>Source.*?</h3>.*?(<ul>.*?</ul>)')
                citation_text = re.findall(re_citation, html_str)
                if len(citation_text):
                    citation_html = etree.HTML(citation_text[0])
                    citation_data = citation_html.xpath('//ul/li')
                    for li in citation_data:
                        li_list = []
                        li_text = li.xpath('./text()')
                        li_list.extend(li_text)
                        try:
                            li_a_text = li.xpath('./a/text()')[0]
                            li_a_url = li.xpath('./a/@href')[0]
                            li_a = li_a_text + '(' + li_a_url + ')'
                            li_list.insert(1, li_a)
                        except:
                            pass
                        citation_str = ''.join(li_list)
                        citation += citation_str
                        # 如果有多个的话，方便区分
                        if len(citation_data) > 1:
                            citation += '***'
            except Exception as e:
                print(e)
            # print('citation= ', citation)
            try:
                file_html = etree.HTML(html)
                file_data = file_html.xpath('//table[@id="datatab" and @summary="Table of datasets"]')
                for table in file_data:
                    table_data = table.xpath('.//tr')[1:]
                    for tr in table_data:
                        fileName = tr.xpath('./td[1]/a/text()')[0]
                        filePath = 'http://snap.stanford.edu/data/' + tr.xpath('./td[1]/a/@href')[0]
                        fileDescription = tr.xpath('./td[2]/text()')
                        file[fileName] = {
                            'filePath': filePath,
                            'fileDescription': fileDescription
                        }
            except Exception as e:
                pass
            # print('file= ', file)

            try:
                re_dataformat = re.compile('Data format.*?(<ul>.*?</ul>)')
                dataformat_data = re.findall(re_dataformat, html_str)
                if len(dataformat_data):
                    dataformat_html = etree.HTML(dataformat_data[0])
                    dataformat_li = dataformat_html.xpath('//ul/li')
                    for li in dataformat_li:
                        try:
                            try:
                                name = li.xpath('./b/text()')[0].strip(' ')
                                value = li.xpath('./text()')[0].strip(' ')
                                dataFormat[name] = value
                            except:
                                name = li.xpath('./tt/text()')[0].strip(' ')
                                value = li.xpath('./text()')[0].strip(' ')
                                dataFormat[name] = value
                        except Exception as e:
                            print(e)
                # else:
                #     print('没有这个字段')
            except Exception as e:
                print(e)
            # print('dataFormat= ', dataFormat)
        else:
            print('错误码为： ', response.status_code)
    except Exception as e:
        print(e)
    datasetStatistic = json.dumps(datasetStatistic)
    file = json.dumps(file)
    dataFormat = json.dumps(dataFormat)
    json_data['datasetInformation'] = datasetInformation
    json_data['datasetStatistic'] = datasetStatistic
    json_data['citation'] = citation
    json_data['file'] = file
    json_data['dataFormat'] = dataFormat
    return json_data




# 将json字符转换成我们需要的key和能插入数据库中的值
def tranJson(data_json):
    json_data = {}
    for k, v in data_json.items():
        if k == 'Name':
            json_data['name'] = v
        elif k == 'Type':
            json_data['type'] = v
        elif k == 'Nodes':
            json_data['nodeCount'] = v
        elif k == 'Edges':
            json_data['edgeCount'] = v
        elif k == 'Communities':
            json_data['communityCount'] = v
        elif k == 'Description':
            json_data['description'] = v
        elif k == 'Temporal Edges':
            json_data['temporalEdgeCount'] = v
        elif k == 'Static Edges':
            json_data['staticEdgeCount'] = v
        elif k == 'Number of items':
            json_data['numberOfItem'] = v
        elif k == 'url':
            json_data['source'] = v
        else:
            print('未转化的 {}， {}'.format(k, v))
    # print(json_data)
    return json_data

def getUrl():
    url = 'http://snap.stanford.edu/data/index.html'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            html_data = etree.HTML(html)
            data = html_data.xpath('//div[@id="right-column"]')[0]
            datasetTypes = data.xpath('./h3/text()')
            tables = data.xpath('./table[@id="datatab2"]')
            CountData = zip(datasetTypes, tables)
            for dt in CountData:
                try:
                    # 1. 数据集表头
                    datasetType = dt[0]
                    print('datasetType= ', datasetType)
                    table = dt[1]
                    trs = table.xpath('./tr')
                    titles = trs[0]
                    sets = trs[1:]
                    titles_th = titles.xpath('./th')
                    # 获取表头字段数据
                    names = []
                    for th in titles_th:
                        try:
                            name = th.xpath('./text()')
                            if not len(name):
                                name = th.xpath('./a/text()')[0]
                            else:
                                name = name[0]
                            names.append(name)
                        except Exception as e:
                            print(e)
                    # 将表头全部放到一个列表中去，并增加url这个字段
                    names.append('url')
                    print('names=', names)
                    # 数据
                    for set in sets:
                        values = []
                        try:
                            set_name_url = set.xpath('./td')[0]
                            set_th = set.xpath('./td')[1:]
                            set_name = set_name_url.xpath('./a/text()')[0]
                            values.append(set_name)
                            set_url = set_name_url.xpath('./a/@href')[0]
                            source_url = BASE_URL + set_url
                            for th in set_th:
                                set_value = th.xpath('./text()')
                                # 有些字段为空
                                if not len(set_value):
                                    set_value = ' '
                                else:
                                    set_value = set_value[0]
                                values.append(set_value)
                            values.append(source_url)
                            a = zip(names, values)
                            for i in a:
                                DATA_JSON[i[0]] = i[1]
                            # print(DATA_JSON)
                            json_data = tranJson(DATA_JSON)
                            uid = uuid.uuid1()
                            suid = str(uid).replace('-', '')
                            # 1. 成果唯一标识
                            datasetId = suid
                            json_data['datasetId'] = datasetId
                            json_data['doi'] = ''
                            json_data['handle'] = ''
                            json_data['datasetType'] = datasetType
                            parse_url = json_data['source']
                            Data = parseUrl(parse_url, json_data)
                            print(Data)
                            mycol.insert_one(json_data)
                        except Exception as e:
                            print('===========', e)
                except Exception as e:
                    print('e= ', e)
                print('**************************')

        else:
            print('响应码为： {}'.format(response.status_code))
    except Exception as e:
        print(e)

def main():
    getUrl()

if __name__ == '__main__':
    main()
