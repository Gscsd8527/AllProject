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
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 3
REDIS_SCORE = 100
IP_MIN = 100

