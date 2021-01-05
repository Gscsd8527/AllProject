import requests
from lxml.html import etree
import pymongo


myclient = pymongo.MongoClient('mongodb://*********:27017/')
mydb = myclient['dataset']  # 数据库
mycol = mydb['cxidb']  # 表


class Cxidb:
    def __init__(self):
        self.url = 'https://www.cxidb.org/id-{id}.html'
        self.base_url = 'https://cxidb.org/'
        self.count = 177

    def request(self):
        for html_id in range(1, self.count + 1):
            print(f'这是第  {html_id} 页')
            url = self.url.format(id=html_id)
            response = requests.get(url)
            if response.status_code == 200:
                text = response.text
                html_xpath = etree.HTML(text)
                body = html_xpath.xpath('//table[@class="entry"]')[0]
                fields = body.xpath('./tr[not(@direction)]/th/text()')  # 不带任何属性的tr标签
                fields = [_.replace('\n', '').replace('\t', '').strip() for _ in fields if _.replace('\n', '').replace('\t', '').strip() != '']
                trs = body.xpath('./tr')
                key = fields[0]
                tr_index = 0
                data_list = []
                for tr in trs:
                    try:
                        filed = tr.xpath('./th/text()')[0].strip()
                        if filed in fields:
                            key = filed
                        if key == 'Data Files':
                            other_tr = trs[tr_index+1:]  # 如果 key 为  Data Files 话，把剩下的 tr标签全部取出来单独处理
                            files = [self.base_url + _.xpath('.//a/@href')[0] for _ in other_tr if len(_.xpath('.//a/@href'))]
                            data_list.append([key, 'files', files])
                            break
                    except:
                        pass
                    try:
                        k = tr.xpath('./td[1]/text()')[0].strip(':')
                        try:
                            v = tr.xpath('./td[2]/text()')[0].strip(':')
                        except:
                            v = tr.xpath('./td/a/@href')[0].strip(':')
                        data_list.append([key, k, v])
                    except:
                        pass
                    tr_index += 1
                keys = list(set([k_[0] for k_ in data_list]))
                data_json = {_: {} for _ in keys}
                for data in data_list:
                    data_json[data[0]].update({data[1]: data[2]})
                print(data_json)
                # mycol.insert_one(data_json)
            else:
                print(f'错误响应码为 {response.status_code}')


def main():
    """
    https://www.cxidb.org/browse.html
    :return:
    """
    cxidb = Cxidb()
    cxidb.request()


if __name__ == '__main__':
    main()
