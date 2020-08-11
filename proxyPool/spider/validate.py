import requests
import json
import redis
import random
from loguru import logger
import threading
from .config import *


class ProxyPoolValidate:
    """
    代理池 IP 验证
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, max_connections=10)
        self.Redis = redis.Redis(connection_pool=self.pool, decode_responses=True)
        self.Redis_db = 'proxyPool'


    def _get_proxy_pool_sum(self):
        """
        获取IP代理池数量
        """
        ip_sum = self.Redis.zcard(self.Redis_db)
        return ip_sum


    def _get_ip(self):
        """
        获取IP
        """
        logger.info('获取IP')
        ip_list = self.Redis.zrange(self.Redis_db, 0, -1, desc=False)
        return ip_list


    def _random_ip(self):
        """
        随机 生成一个IP， 用于代理IP抓取
        """
        try:
            random_ip = random.choice(self.Redis.zrange(self.Redis_db, 0, -1, desc=False))
        except:
            random_ip = None
        if random_ip:
            return random_ip


    def _insert_ip(self, http, ip, port):
        """
        插入IP
        """
        logger.info('插入IP')
        http_href = f'{http}://{ip}:{port}'
        http_url = {http: http_href}
        http_json = json.dumps(http_url)
        temp_json = {http_json: REDIS_SCORE}
        self.Redis.zadd(self.Redis_db, temp_json)


    def _check_proxies(self, ip_url):
        """
        校验 代理 IP
        """
        logger.info('校验IP')
        proxies = json.loads(ip_url)
        try:
            response = requests.get(CRAWLE_URL, proxies=proxies, timeout=1)
            if response.ok:
                logger.info('{}  可用'.format(proxies))
            else:
                logger.info('{}  无用'.format(proxies))
                self._delete_proxies(ip_url=ip_url)
        except Exception as e:
            logger.error('E:  '+ str(e))
            logger.info('{}  无用'.format(proxies))
            self._delete_proxies(ip_url=ip_url)


    def _delete_proxies(self, ip_url):
        """
        删除失效IP
        """
        logger.info('删除失效IP')
        self.Redis.zrem(self.Redis_db, ip_url)


    def _thread_check_proxies(self, ip_list):
        """
        调用线程 校验 ip
        """
        logger.info('开启线程调用IP')
        nums = len(ip_list)
        cs = nums // THREAD_NUM
        sy = nums % THREAD_NUM
        if sy > 0:
            cs += 1
        for i in range(cs):
            if i == cs+1:
                thread_list = ip_list[i*THREAD_NUM:]
            else:
                thread_list = ip_list[i * THREAD_NUM: (i + 1) * THREAD_NUM]
            threads = [threading.Thread(target=self._check_proxies, args=(ips,)) for ips in thread_list]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()


def main():
    ProxyPoolValidate()._get_ip()


if __name__ == '__main__':
    main()



