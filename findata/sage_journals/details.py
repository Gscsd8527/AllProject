import requests
import pymongo
from lxml import etree
import threading
import re
import json


THREAD_NUM = 10
Lock = threading.Lock()


myclient = pymongo.MongoClient('mongodb://*********:27017/')
mydb = myclient['dataset']  # 数据库
mycol = mydb['sage_journals']  # 表
mycol_data = mydb['sage_journals_data']  # 表


class SageJournals:
    def request(self, dt):
        title = dt['title']
        url = dt['url']
        posted = dt['posted']
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            html = etree.HTML(text)
            try:
                try:
                    description = html.xpath('//div[@class="_3gcwy"]/div[@class="_3j15x"]//p/text()')[0]
                except:
                    description = html.xpath('//div[@class="_3zjWV"]')[0]
                    description_string = etree.tostring(description, encoding='utf-8').decode('utf-8')
                    description_string_list = re.findall('>(.*?)<', description_string)
                    description_string_list = [i for i in description_string_list if i != '']
                    description = '\n'.join(description_string_list)
            except:
                try:
                    description = html.xpath('//div[@class="_3gcwy"]')[0]
                    description_string = etree.tostring(description, encoding='utf-8').decode('utf-8')
                    description_string_list = re.findall('>(.*?)<', description_string)
                    description_string_list = [i.strip() for i in description_string_list if i != '']
                    description = '\n'.join(description_string_list)
                except:
                    description = ''
            try:
                doi = html.xpath('//div[@class="_1HwW4"]//a/@href')[0]
            except:
                doi = ''
            try:
                download_url = html.xpath('//div[@aria-orientation="horizontal"]//a/@href')[0]
            except:
                download_url = ''
            try:
                file_name = html.xpath('//div[@class="_1SY7u textSizeS"]/@title')[0]
            except:
                file_name = ''
            try:
                authors = html.xpath('//div[@class="_2o9ZF"]//div[@class="_3xNn7"]//span/@title')
                if not authors:
                    authors = html.xpath('//div[@class="_3xNn7"]//div/@title')
            except:
                authors = []
            try:
                category = html.xpath('//section[@class="wLGAQ"]//li/a/span/text()')
            except:
                category = ''
            try:
                keywords = html.xpath('//div[@class="_24MgV"]//a/span/text()')
            except:
                keywords = ''
            if not len(keywords):
                keywords = html.xpath('//div[@class="_3zOxb _3ELOV"][last()]//a/span/text()')
            try:
                license = html.xpath('//div[@class="_3eD2q"]//a/text()')
            except:
                license = ''
            data_json = {
                'title': title,
                'posted': posted,
                'description': description,
                'doi': doi,
                'authors': authors,
                'category': category,
                'keywords': keywords,
                'url': url,
                'license': license,
                'download_url': download_url,
                'file_name': file_name,
            }
            print(data_json['title'])
            mycol_data.insert_one(data_json)

        else:
            print('错误响应码为： ', response.status_code)

    @staticmethod
    def parse_html(html):
        """
        解析页面
        :param html:
        :return:
        """
        # json_string = re.findall('{ window.apolloState = ({.*}); }\(\)\);', html)[0]
        # json_string = re.findall('{ window.apolloState = ({.*?}); }\(\)\);</script><script>;', html)[0]
        json_string = re.findall('({.*?"description").*?"\$ROOT_QUERY', html)[0]
        json_string = json_string.replace(':true,', ':"true",')
        json_string = json_string.replace('null', '"null"')
        print(json_string)
        print(json.loads(json_string))
        print(eval(json_string))

    @staticmethod
    def get_all_url():
        """
        获取所有请求的url
        :return:
        """
        urls = [{'title': _['title'], 'url': _['url'], 'posted': _['timeline']['posted']} for _ in mycol.find({}, {'title', 'url', 'timeline'})]
        return urls


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
            threads = [threading.Thread(target=self.request, args=(dt,)) for dt in works]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()


def main():
    """
    4tu网站抓取
    :return:
    """
    sage_journals = SageJournals()
    data = sage_journals.get_all_url()
    sage_journals.start_thread(data)


if __name__ == '__main__':
    main()
