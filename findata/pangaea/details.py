import requests
from lxml import etree
import pandas as pd
import random
from loguru import logger
import threading
import json


THREAD_NUM = 20
Lock = threading.Lock()


MY_USER_AGENT = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]


class Pangaea:
    def __init__(self):
        self.base_url = 'https://doi.pangaea.de/'


    def request(self, data):
        """
        请求详细页
        :param data: 源数据
        :return:
        """
        url = data['url']
        headers = {'User-Agent': random.choice(MY_USER_AGENT)}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            text = response.text
            html_xpath = etree.HTML(text)
            authors_list = html_xpath.xpath('//h1[@class="hanging citation"]/strong//text()')
            authors_list = [_ for _ in authors_list if _ != '']
            authors_string = ''.join(authors_list)
            authors_string = authors_string.rsplit('(')[0]
            authors_list = authors_string.split(';')
            authors = [_.strip() for _ in authors_list]

            description_list = html_xpath.xpath('//h1[@class="hanging citation"]/text()')
            description_list = [_.strip() for _ in description_list if _ != '']
            description = ''.join(description_list)
            rows = html_xpath.xpath('//div[@id="main"]//div[@class="row"]')
            temp_dict = {}
            temp_dict['authors'] = authors
            temp_dict['description'] = description
            for row in rows:
                # head = row.xpath('.//div[@class="title"]/text()')[0]
                head = row.xpath('./div[1]/div/text()')[0]
                if 'Abstract' in head:
                    abstract = row.xpath('.//div[@class="abstract"]/text()')[0]
                    temp_dict['abstract'] = abstract
                elif 'Keyword' in head:
                    keyword = row.xpath('.//div[@class="descr"]//text()')
                    keyword = [_.strip('; ').strip() for _ in keyword if _ != '\n']
                    temp_dict['keyword'] = keyword
                elif 'Related' in head:
                    related = row.xpath('.//div[@class="descr"]//text()')
                    related = [_.strip() for _ in related if _ not in ['', '\n']]
                    related = ''.join(related)
                    temp_dict['related'] = related
                elif 'Project' in head:
                    project = row.xpath('.//div[@class="descr"]//text()')
                    project = [_.strip() for _ in project if _ not in ['', '\n']]
                    project = ''.join(project)
                    temp_dict['project'] = project
                elif 'Coverage' in head:
                    coverage = row.xpath('.//div[@class="descr"]//text()')
                    coverage = [_ for _ in coverage if _ not in ['', '\n']]
                    coverage = ''.join(coverage)
                    temp_dict['coverage'] = coverage
                elif 'Event' in head:
                    event = row.xpath('.//div[@class="descr"]//text()')
                    event = [_.strip() for _ in event if _ not in ['', '\n']]
                    event = ''.join(event)
                    temp_dict['event'] = event
                elif 'Comment' in head:
                    comment = row.xpath('.//div[@class="descr"]//text()')
                    comment = [_.strip() for _ in comment if _ not in ['', '\n']]
                    comment = '\n'.join(comment)
                    temp_dict['comment'] = comment
                elif 'License' in head:
                    license = row.xpath('.//div[@class="descr"]//text()')
                    license = [_.strip() for _ in license if _ not in ['', '\n']]
                    temp_dict['license'] = license
            data_json = {
                **data,
                **temp_dict
            }
            Lock.acquire()
            # mycol_data.insert_one(data_json)
            data_sring = json.dumps(data_json, ensure_ascii='utf-8')
            with open('data.json', 'a+', encoding='utf-8') as f:
                f.write('{}\n'.format(data_sring))

            with open('yzq.txt', 'a+', encoding='utf-8') as f:
                f.write('{}\n'.format(data['doi']))

            Lock.release()
        else:
            logger.info(f'错误响应码为{response.status_code}')


    def get_all_doi(self):
        """
        获取所有doi
        :return:
        """
        yzq_doi = open('yzq.txt', 'r', encoding='utf-8')
        yzq_doi_list = [_.strip('\n') for _ in yzq_doi.readlines() if _ not in ['', '\n']]

        # 用pandas来做去重更快
        df = pd.read_json('doi.json', orient='records', lines=True)
        df = df.drop_duplicates(subset='url')
        df = df[~df['doi'].isin(yzq_doi_list)]
        logger.info(f'已抓取： {len(yzq_doi_list)}, 未抓取 {len(df)}')
        data_list = df.to_dict(orient='records')
        return data_list


def start_thread(data_list, pangaea):
    nums = len(data_list)
    x = nums // THREAD_NUM
    ys = nums % THREAD_NUM
    if ys > 0:
        x += 1
    for i in range(x):
        logger.info('循环第  {}   次， 共有   {}   次'.format(i, x))
        if i == x + 1:
            works = data_list[i * THREAD_NUM:]
        else:
            works = data_list[i * THREAD_NUM:(i + 1) * THREAD_NUM]
        threads = [threading.Thread(target=pangaea.request, args=(work,)) for work in works]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


def main():
    """
    pangaea 详细页解析
    :return:
    """
    pangaea = Pangaea()
    data_list = pangaea.get_all_doi()
    start_thread(data_list, pangaea)


if __name__ == '__main__':
    main()
