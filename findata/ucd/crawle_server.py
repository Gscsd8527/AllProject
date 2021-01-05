import requests
from lxml import etree
import json
import pandas as pd
import threading
from loguru import logger
import re
import copy
import random
import time

THREAD_NUM = 1
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


class Ucd:
    def __init__(self):
        self.url = 'https://digital.ucd.ie/index.php?q=&start={}&rows=10'
        self.base_url = 'https://digital.ucd.ie/view/'
        self.author_base_url = 'https://digital.ucd.ie/'
        self.pages = 24952


    def get_source_data(self):
        """
        获取原始数据
        :return:
        """
        for page in range(1, self.pages+1):
            logger.info(f'这是第 {page} 页')
            url = self.url.format(page*10 + 1)
            self.request(url, page)


    def request(self, url, page):
        headers = {'User-Agent':  random.choice(MY_USER_AGENT)}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            text = response.text
            # print(text)
            self.parse_html(text, page)
        else:
            logger.info('错误响应码为：' + str(response.status_code))


    @staticmethod
    def parse_html(text, page):
        html_xpath = etree.HTML(text)
        rows = html_xpath.xpath('//div[@class="row results-row"]/div')
        print(len(rows))
        for row in rows:
            title = row.xpath('.//h4/a/text()')[0]
            url = row.xpath('.//img/@src')[0]
            temp_dict = {
                'title': title,
                'url': url,
                'page': page,
            }
            print(temp_dict)
            temp_string = json.dumps(temp_dict, ensure_ascii=False)
            with open('data.json', 'a+', encoding='utf-8') as f:
                f.write('{}\n'.format(temp_string))


    @staticmethod
    def get_id_data():
        """
        解析id得到数据
        :return:
        """
        df = pd.read_json('data.json', encoding='utf-8', lines=True)
        urls = df['url'].values.tolist()
        dois = [i.replace('/get/', '').replace('/thumbnail', '') for i in urls if i != '']
        print('总的数量为', len(dois))
        yzq_doi = open('yzq.txt', 'r', encoding='utf-8')
        yzq_doi_list = [_.strip() for _ in yzq_doi.readlines()]
        print('已抓取的数量为', len(yzq_doi_list))
        dois = list(set(dois) - set(yzq_doi_list))
        print('未抓取的数量为', len(dois))
        return dois


    def start_thread(self, ids):
        nums = len(ids)
        x = nums // THREAD_NUM
        ys = nums % THREAD_NUM
        if ys > 0:
            x += 1
        for i in range(x):
            print('循环第  {}   次， 共有   {}   次'.format(i, x))
            if i == x + 1:
                works = ids[i * THREAD_NUM:]
            else:
                works = ids[i * THREAD_NUM:(i + 1) * THREAD_NUM]
            print('work- ', works)
            threads = [threading.Thread(target=self.request_detail, args=(doi,)) for doi in works]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()


    def request_detail(self, doi):
        url = self.base_url + doi
        headers = {'User-Agent': random.choice(MY_USER_AGENT)}
        try:
            response = requests.get(url, headers=headers)

        except:
            time.sleep(3)
            response = requests.get(url, headers=headers)

        if response.status_code == 200:
            text = response.text
            # print(text)
            self.parse_detail(text, doi, url)
        else:
            logger.info('错误响应码为：' + str(response.status_code))


    def parse_detail(self, text, doi, source_url):
        """
        解析详细页信息
        :param text:
        :return:
        """
        html_data = etree.HTML(text)
        try:
            permalink = html_data.xpath('//span[@id="permalink"]/text()')[0]
        except:
            permalink = ''
        print(text)
        body = html_data.xpath('//div[@id="data-heading"]/div[@class="panel-body"]')[0]
        try:
            title = body.xpath('.//span/h1/text()')[0]
        except:
            title = ''
        try:
            description_xpath = body.xpath('.//p[@itemprop="description"]')
            description_list = []
            for description in description_xpath:
                description_string = etree.tostring(description, encoding='utf-8').decode('utf-8')
                description_string_list = re.findall('>(.*?)<', description_string)
                description_string_list = [i for i in description_string_list if i != '']
                description_list.extend(description_string_list)
            description = ''.join(description_list)
        except:
            description = ''
        authors_list = []
        try:
            authors = body.xpath('.//ul[@class="name-list list-unstyled"]//span[@itemprop="name"]/a')

            for author in authors:
                name = author.xpath('./text()')[0]
                url = self.author_base_url + author.xpath('./@href')[0]
                temp_dict = {
                    'name': name,
                    'url': url,
                }
                authors_list.append(copy.deepcopy(temp_dict))
        except:
            pass

        data_json = {
            'permalink': permalink,
            'title': title,
            'description': description,
            'authors': authors_list,
            'doi': doi,
            'url': source_url,
        }
        Lock.acquire()
        data_string = json.dumps(data_json, ensure_ascii=False)
        with open('ucd.json', 'a+', encoding='utf-8') as f:
            f.write('{}\n'.format(data_string))
        with open('yzq.txt', 'a+', encoding='utf-8') as f:
            f.write('{}\n'.format(doi))
        Lock.release()


def main():
    """
    :return:
    """
    ucd = Ucd()
    # 获取原始数据
    # ucd.get_source_data()

    # 解析详细页
    ids = ucd.get_id_data()
    ucd.start_thread(ids)


if __name__ == '__main__':
    main()
