spider_rule_list =[
    {
        'urls': ['http://www.ip3366.net/free/?stype=1&page={}'.format(i) for i in range(1, 6)],
        'type': 'xpath',
        'node': '//tbody/tr',
        'target': {'ip': './td[1]/text()', 'port': './td[2]/text()', 'http': './td[4]/text()'},
    },
    {
        'urls': ['https://www.kuaidaili.com/free/inha/{}/'.format(j) for j in range(1, 6)],
        'type': 'xpath',
        'node': '//tbody/tr',
        'target': {'ip': './td[1]/text()', 'port': './td[2]/text()', 'http': './td[4]/text()'},
    },
]
REDIS_HOST = '127.0.0.1'  #  redis的IP
REDIS_PORT = 6379  #  redis 的端口号
REDIS_DB = 3  # 数据库
REDIS_SCORE = 100  # 分数
IP_MIN = 100  # 最小IP数

THREAD_NUM = 20  # 线程数

CRAWLE_URL = 'https://www.baidu.com/?tn=06074089_18_pg&ch=6'  # 抓取的url

SELLP_TIME = 10  # 休眠秒数