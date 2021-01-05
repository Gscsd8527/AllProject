import requests
import json
from loguru import logger
import datetime
from lxml import etree
from lxml.html import tostring


class ChinaAcademician:
    def __init__(self):
        self.count = 29716  # 总数
        self.pages = self.get_pages()
        self.timestemp = 1609745561123  # url中给的时间戳，但又不是时间戳
        self.url = 'https://ysg.ckcest.cn/ysgNews/api/newsList?pageSize=12&pageNum={page}&_={timestemp}'
        self.base_img = 'http://ysg.ckcest.cn/ysgOld'
        self.href_url = 'https://ysg.ckcest.cn/ysgNews/{id}.html'
        self.file_path = './file/'

    def get_list_page_data(self):
        """
        获取初始的列表页数据
        :return:
        """
        for page in range(1, self.pages + 1):
            logger.info(f'这是第 {page} 页, 总共有 {self.pages} 页')
            url = self.url.format(page=page, timestemp=self.timestemp)
            self.timestemp += 1
            response = requests.get(url)
            if response.status_code == 200:
                text = response.text
                data_json = json.loads(text)
                data_list = data_json['newsList']
                for data in data_list:
                    title = data['title']
                    logger.info(title)
                    with open('source.json', 'a+', encoding='utf-8') as f:
                        f.write('{}\n'.format(json.dumps(data, ensure_ascii=False)))
            else:
                print('错误响应码为：', response.status_code)


    def get_pages(self):
        """
        获取页数
        :return:
        """
        pages = self.count // 12
        ys = self.count % 12
        if ys > 0:
            pages += 1
        return pages


    def get_page_data(self):
        """
        解析列表页数据
        :return:
        """
        try:
            f1 = open('yzq.txt', 'r', encoding='utf-8')
            set1 = set(_.strip('\n') for _ in f1.readlines())
            f1.close()
        except:
            set1 = set()

        f = open('source.json', encoding='utf-8')
        data = [json.loads(_.strip('\n')) for _ in f.readlines()]
        data_list = []
        for dt in data:
            title = dt['title']
            try:
                img_url = self.base_img + dt['cover'].replace('\\', '/')
            except:
                img_url = ''
            url = self.href_url.format(id=dt['id'])
            try:
                source = dt['mediaName']
            except:
                source = ''

            try:
                date = datetime.datetime.fromtimestamp(int(dt['reportDate'])/1000).strftime('%Y-%m-%d %H:%M:%S')
            except:
                date = ''

            name = dt['acInfos'][0]['acInfoName']

            if url not in set1:
                data_list.append({
                    'title': title,
                    'name': name,
                    'img_url': img_url,
                    'url': url,
                    'source': source,
                    'date': date
                })
        logger.info(f'已抓取 {len(set1)}, 总的有 {len(data_list)}')
        return data_list


    def request(self, data):
        """
        详细页请求
        :param data:
        :return:
        """
        url = data['url']
        print(data)
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            html_data = etree.HTML(text)
            body_html = tostring(html_data.xpath('//div[@class="news_detail_text"]')[0], encoding="utf-8", pretty_print=True, method="html")
            body_html = body_html.decode("utf-8")
            body = html_data.xpath('string(//div[@class="news_detail_text"])').strip()
            try:
                link = html_data.xpath('//div[@class="news_detail_link"]/a/@href')[0]
            except:
                link = ''
            temp_dict = {
                **data,
                'body_html': body_html,
                'body': body,
                'link': link,
            }
            with open('data.json', 'a+', encoding='utf-8') as f:
                f.write('{}\n'.format(json.dumps(temp_dict, ensure_ascii=False)))
            with open('yzq.txt', 'a+', encoding='utf-8') as f:
                f.write('{}\n'.format(url))

        else:
            print('错误响应码为', response.status_code)


    def download_img(self):
        """
        下载图片
        :return:
        """
        try:
            f1 = open('yzq.txt', 'r', encoding='utf-8')
            set1 = set(_.strip('\n') for _ in f1.readlines())
            f1.close()
        except:
            set1 = set()

        f = open('source.json', encoding='utf-8')
        data = [json.loads(_.strip('\n')) for _ in f.readlines()]
        f.close()
        data_list = []
        for dt in data:
            try:
                img_url = self.base_img + dt['cover'].replace('\\', '/')
                img_name = img_url.replace('http://ysg.ckcest.cn/ysgOld/uploadfile/cae/newsCover/', '')
                if img_url not in set1:
                    data_list.append(
                        {
                            'img_url': img_url,
                            'img_name': img_name,
                        }
                    )
            except:
                pass

        logger.info(f'已抓取 {len(set1)}, 总的有 {len(data_list)}')
        for dt in data_list:
            img_url = dt['img_url']
            img_name = dt['img_name']
            logger.info(f'正在抓取 {img_url}')
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(self.file_path + '{}.jpg'.format(img_name), 'wb') as fd:
                    # 每到128位就写入
                    for chunk in response.iter_content(128):
                        fd.write(chunk)
                with open('img_yzq.txt', 'a+', encoding='utf-8') as f:
                    f.write('{}\n'.format(img_url))
            else:
                logger.info(f'获取图片失败： 错误响应码为{response.status_code}')


def main():
    """
    中国院士馆
    https://ysg.ckcest.cn/ysgNews/index.html
    :return:
    """
    academician = ChinaAcademician()

    # 第一步： 获取初始列表页数据
    # academician.get_list_page_data()

    # 第二步： 通过初始列表页数据，获取详细页数据
    # data_list = academician.get_page_data()
    # for data in data_list:
    #     academician.request(data)

    # 第三步: 下载图片
    # academician.download_img()


if __name__ == '__main__':
    main()
