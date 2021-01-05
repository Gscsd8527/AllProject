import requests
import json
from loguru import logger
import redis
from concurrent.futures import ThreadPoolExecutor, as_completed

pool = redis.ConnectionPool(host='*********', port=6378, db=13, decode_responses=True)
r = redis.Redis(connection_pool=pool)


class Nomad:
    def __init__(self):
        self.url = 'https://nomad-lab.eu/prod/rae/api/repo/?page=1&per_page=10&order_by=upload_time&order=-1&domain=dft&owner=public&statistics=atoms&exclude=atoms,only_atoms,dft.files,dft.quantities,dft.optimade,dft.labels,dft.geometries'
        self.type_url = 'https://nomad-lab.eu/prod/rae/api/repo/?page={page}&per_page=10&order_by=upload_time&order=-1&domain=dft&owner=public&atoms={atoms}&statistics=atoms&exclude=atoms,only_atoms,dft.files,dft.quantities,dft.optimade,dft.labels,dft.geometries'
        self.type_url_order_by = 'https://nomad-lab.eu/prod/rae/api/repo/?page={page}&per_page=10&order_by=upload_time&order=1&domain=dft&owner=public&atoms={atoms}&statistics=atoms&exclude=atoms,only_atoms,dft.files,dft.quantities,dft.optimade,dft.labels,dft.geometries'
        self.page_num = 10  # 一页的数量


    def get_all_type(self):
        """
        获取所有类型
        将所有类型导入到redis中
        :return:
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            text = response.text
            json_data = json.loads(text)
            atoms = json_data['statistics']['atoms']
            data_list = [{'key': k, 'pages': self.get_pages(atoms[k]['code_runs'])} for k in atoms.keys()]
            for data in data_list:
                key = data['key']
                pages = data['pages']
                for page in range(1, pages+1):
                    url = self.type_url.format(page=page, atoms=key)
                    print('顺序', url)
                    r.lpush('nomad', url)
                # 改变了order_by，倒序，网站没有，我自己猜的
                for page in range(1, pages+1):
                    url = self.type_url_order_by.format(page=page, atoms=key)
                    print('倒序', url)
                    # r.lpush('nomad', url)
        else:
            logger.info(f'错误响应码为： {response.status_code}')


    def get_pages(self, nums):
        """
        获取页数
        :return:
        """
        pages = nums // self.page_num
        ys = nums % self.page_num
        if ys > 0:
            pages += 1
        # 最多1000页
        if pages > 1000:
            pages = 1000
        return pages


    def get_works(self):
        keys = r.lrange('nomad', 0, -1)
        logger.info(f'总共有 {len(keys)} 个')
        works = keys
        return works


    def request(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
        else:
            print('错误响应码为： ', response.status_code)
            text = ''
        return {'text': text, 'url': url}


    def start_thread(self, works):
        pool = ThreadPoolExecutor(max_workers=20)
        jobs = []
        for work in works:
            p = pool.submit(self.request, work)  # 异步提交任务
            jobs.append(p)
        index = 1
        for _ in as_completed(jobs):
            print('***', index)
            data = _.result()
            try:
                text = data['text']
                url = data['url']
                if len(text) != 0 or text is not None:
                    r.lpush('nomad_data', text)
                    r.lrem('nomad', 0, url)
            except:
                pass
            index += 1


def main():
    """
    https://nomad-lab.eu/prod/rae/gui/search
    :return:
    """
    nomad = Nomad()
    # 第一步： 获取url
    # nomad.get_all_type()

    # 第二步： 执行多线程
    works = nomad.get_works()
    nomad.start_thread(works=works)



if __name__ == '__main__':
    main()
