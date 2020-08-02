from .config import *
import requests
from lxml import etree
from .validate import ProxyPoolValidate, json, logger


class Crawler:
    """
    抓取 云代理  和  快代理  免费IP
    用 Redis 数据库来做存储和去重
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

    def crawl(self):
        """
        获取 代理IP 的 url 及端口
        """
        for spider_rule in spider_rule_list:
            urls = spider_rule['urls']
            node = spider_rule['node']
            target = spider_rule['target']
            self.download(urls=urls, node=node, target=target)

    def download(self, urls, node, target):
        """
        发起请求下载HTML并解析 得到 ip 地址
        :return:
        """
        for url in urls:
            random_ip = ProxyPoolValidate()._random_ip()

            response = self._trun_proxy_mode(url, random_ip)

            html = response.text
            data_html = etree.HTML(html)
            trs = data_html.xpath(node)
            for tr in trs:
                ip = tr.xpath(target['ip'])[0]
                port = tr.xpath(target['port'])[0]
                http = tr.xpath(target['http'])[0].lower()
                ProxyPoolValidate()._insert_ip(http, ip, port)
            # import time
            # time.sleep(10000)

    def _trun_proxy_mode(self, url, random_ip):
        """
        是否启用代理IP
        :return:
        """
        logger.info('使用代理IP来抓取代理IP')
        if random_ip is not None:
            try:
                response = requests.get(url, headers=self.headers, proxies=json.loads(random_ip), timeout=0.5)
                logger.info('代理有效')
            except:
                response = requests.get(url, headers=self.headers)
                logger.error('代理无效')
                ProxyPoolValidate()._delete_proxies(random_ip)
        else:
            response = requests.get(url, headers=self.headers)
        return response




def main():
    """
    获取 IP
    :return:
    """
    Crawler().crawl()

if __name__ == '__main__':
    main()