from .crawler import Crawler
from .validate import ProxyPoolValidate, IP_MIN, logger
import time
from .config import SELLP_TIME

class Scheduler:
    """
    调度
    """
    def _scheduler(self):
        while True:
            ip_sum = ProxyPoolValidate()._get_proxy_pool_sum()
            logger.info(f'现有IP {ip_sum}  个')
            if ip_sum < IP_MIN:
                logger.info(f'低于最小IP数 {IP_MIN}')
                Crawler().crawl()
            ip_list = ProxyPoolValidate()._get_ip()
            ProxyPoolValidate()._thread_check_proxies(ip_list)
            logger.info('休眠10秒')
            time.sleep(SELLP_TIME)

