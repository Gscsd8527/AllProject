import requests
from lxml import etree

# url = 'http://www.ip3366.net/free/?stype=1&page=1'
# response = requests.get(url)
# # print(response.text)
# text = response.text
# data_html = etree.HTML(text)
# data_xpath = data_html.xpath('//tbody/tr')
# for tr in data_xpath:
#     ip = tr.xpath('./td[1]/text()')[0]
#     port = tr.xpath('./td[2]/text()')[0]
#     http = tr.xpath('./td[4]/text()')[0]
#     print(http, ip, port)


url = 'https://www.kuaidaili.com/free/inha/1/'
response = requests.get(url)
# print(response.text)
text = response.text
data_html = etree.HTML(text)
data_xpath = data_html.xpath('//tbody/tr')
for tr in data_xpath:
    ip = tr.xpath('./td[1]/text()')[0]
    port = tr.xpath('./td[2]/text()')[0]
    http = tr.xpath('./td[4]/text()')[0]
    print(http, ip, port)