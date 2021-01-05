import requests
from lxml import etree
import json
from loguru import logger
import pymongo
import threading
import copy


myclient = pymongo.MongoClient('mongodb://*********:27017/')
mydb = myclient['dataset']  # 数据库
mycol = mydb['pangaea']  # 表

THREAD_NUM = 20
Lock = threading.Lock()


class Pangaea:
    def __init__(self):
        self.base_url = 'https://www.pangaea.de/'
        self.topics = ['Chemistry', 'Lithosphere', 'Oceans', 'Biological Classification', 'Atmosphere', 'Paleontology',
                       'Ecology', 'Biosphere', 'Land Surface', 'Geophysics', 'Cryosphere', 'Lakes & Rivers',
                       'Human Dimensions', 'Fisheries', 'Agriculture']
        self.topic_year_url = 'https://www.pangaea.de/advanced/search.php?facets=pubyear%23256&count=0&t={topic}'

        self.index_page = 'https://www.pangaea.de/advanced/search.php?facets=default&t={topic}&f.pubyear[]={year}'
        self.next_page = 'https://www.pangaea.de/advanced/search.php?facets=default&t={topic}&offset={page}&f.pubyear[]={year}'
        self.urls = self.get_all_url()


    def get_all_url(self):
        """
        获取所有url
        :return:
        """
        urls = []
        for topic in self.topics:
            year_list = self.get_year(topic)
            for year_num in year_list:
                year = year_num['year']
                nums = year_num['nums']
                pages = self.get_pages(nums)
                for page in range(pages):
                    logger.info(f'关键词为{topic}, year为{year}, page为{page}')
                    if page == 0:
                        url = self.index_page.format(topic=topic, year=year)
                    else:
                        url = self.next_page.format(topic=topic, page=page*10, year=year)
                    temp_list = {
                        'url': url,
                        'page': page,
                        'year': year,
                    }
                    urls.append(copy.deepcopy(temp_list))
        return urls


    def request(self, data):
        """
        请求链接
        :param url:
        :return:
        """
        url = data['url']
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            data_json = json.loads(text)
            results = data_json['results']
            for result in results:
                temp_dict = {
                    **result,
                    **data
                }
                Lock.acquire()
                mycol.insert_one(temp_dict)
                Lock.release()
        else:
            logger.info(f'错误响应码为 {response.status_code}')


    def get_topic(self):
        """
        获取topic
        :return:
        """
        response = requests.get(self.base_url)
        if response.status_code == 200:
            text = response.text
            html_xpath = etree.HTML(text)
            topic_list = html_xpath.xpath('//div[@class="topics-kachel-wrapper col-lg-4 col-md-4 col-sm-4 col-xs-8"]//a/text()')
            print(topic_list)
            topic_list = ['Chemistry', 'Lithosphere', 'Oceans', 'Biological Classification', 'Atmosphere', 'Paleontology', 'Ecology', 'Biosphere', 'Land Surface', 'Geophysics', 'Cryosphere', 'Lakes & Rivers', 'Human Dimensions', 'Fisheries', 'Agriculture']
        else:
            logger.info(f'错误响应码为 {response.status_code}')


    def get_year(self, topic):
        """
        获取topic的年份数据
        :param topic:
        :return:
        """
        response = requests.get(self.topic_year_url.format(topic=topic))
        if response.status_code == 200:
            text = response.text
            json_data = json.loads(text)
            year_list_data = json_data['facets'][0]['buckets']
            year_list = [{'year': _['value'], 'nums': _['count']} for _ in year_list_data]
            return year_list
        else:
            logger.info(f'错误响应码为 {response.status_code}')


    @staticmethod
    def get_pages(nums):
        """
        获取页数
        :param nums:
        :return:
        """
        if nums > 10000:
            nums = 10000

        pages = nums // 10
        ys = nums % 10
        if ys > 0:
            pages += 1
        return pages



def start_thread(urls, pangaea):
    nums = len(urls)
    x = nums // THREAD_NUM
    ys = nums % THREAD_NUM
    if ys > 0:
        x += 1
    for i in range(x):
        print('循环第  {}   次， 共有   {}   次'.format(i, x))
        if i == x + 1:
            works = urls[i * THREAD_NUM:]
        else:
            works = urls[i * THREAD_NUM:(i + 1) * THREAD_NUM]
        print('work- ', works)
        threads = [threading.Thread(target=pangaea.request, args=(url,)) for url in works]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


def main():
    """
    https://www.pangaea.de/ 网站抓取
    :return:
    """
    pangaea = Pangaea()
    urls = pangaea.urls
    start_thread(urls, pangaea)


if __name__ == '__main__':
    main()
