import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import pymongo
from loguru import logger


myclient = pymongo.MongoClient('mongodb://*********:27017/')
mydb = myclient['dataset']  # 数据库
mycol = mydb['gbif']  # 表


class Gbif:
    def __init__(self):
        self.url = 'https://www.gbif.org/api/dataset/search?facet=type&facet=publishing_org&facet=hosting_org&facet=publishing_country&facet=project_id&facet=license&locale=en&offset={offset}'
        self.count = 54976  # 总量
        self.page_num = 20  # 一页的数量
        self.pages = self.get_pages()


    def get_pages(self):
        """
        获取页数
        :return:
        """
        pages = self.count // self.page_num
        ys = self.count % self.page_num
        if ys > 0:
            pages += 1
        print(pages)
        return pages


    def get_works(self):
        works = [self.url.format(offset=page*self.page_num) for page in range(self.pages)]
        return works


    def request(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            data_json = json.loads(text)
            results = data_json['results']
            return results
        else:
            print('错误响应码为： ', response.status_code)


def main():
    """
    https://www.gbif.org/dataset/search
    :return:
    """
    gbif = Gbif()
    works = gbif.get_works()
    pool = ThreadPoolExecutor(max_workers=10)

    jobs = []
    for work in works:
        p = pool.submit(gbif.request, work)  # 异步提交任务
        jobs.append(p)
    for _ in as_completed(jobs):
        for result in _.result():
            logger.info(result['title'])
            # mycol.insert_one(result)


if __name__ == '__main__':
    main()
