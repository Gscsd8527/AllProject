import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
import redis
import json

pool = redis.ConnectionPool(host='*********', port=6378, db=13, decode_responses=True)
r = redis.Redis(connection_pool=pool)


class Gbif:
    def __init__(self):
        self.base_url = 'https://www.gbif.org/api/dataset/'

    def get_works(self):
        keys = r.lrange('gbif', 0, -1)
        logger.info(f'总共有 {len(keys)} 个')
        works = [self.base_url + _ for _ in keys]
        return works

    def request(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            return text
        else:
            print('错误响应码为： ', response.status_code)
            return ''


def main():
    """
    详细页抓取
    :return:
    """
    gbif = Gbif()
    works = gbif.get_works()
    pool = ThreadPoolExecutor(max_workers=20)

    jobs = []
    for work in works:
        p = pool.submit(gbif.request, work)  # 异步提交任务
        jobs.append(p)
    index = 1
    for _ in as_completed(jobs):
        print('***', index)
        data = _.result()
        try:
            if len(data) != 0 or data is not None:
                key = json.loads(data)['key']
                r.lpush('gbif_data', data)
                r.lrem('gbif', 0, key)
        except:
            pass
        index += 1


if __name__ == '__main__':
    main()
