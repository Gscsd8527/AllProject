import requests
import re
import pandas as pd
from lxml import etree
from loguru import logger
import json


class Academician:
    def __init__(self):
        # self.url = 'http://www.casad.cas.cn/ysxx2017/ysmdyjj/qtysmd_124280/'
        self.url = 'http://casad.cas.cn/ysxx2017/ygysmd/'
        self.re_compile = re.compile('(http://casad.cas.cn/sourcedb_ad_cas.*?html)')
        self.file_path = './file/'
        self.df_name_id = self.get_name_id()

    def get_acade_url(self):
        """
        获取url链接
        :return:
        """
        print('获取url链接')
        response = requests.get(self.url)
        if response.status_code == 200:
            text = response.text
            url_list = re.findall(self.re_compile, text)
            for url in url_list:
                print('url = ', url)
                self.get_acade_detailed_info(url)
        else:
            logger.info(f'错误响应码为{response.status_code}')


    def get_acade_detailed_info(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            text = response.text
            html = etree.HTML(text)
            name = html.xpath('//div[@class="contentBar"]//div[@class="title"]/h1/text()')[0]

            particulars = html.xpath('//div[@class="contentTest"]//p[@align="justify"]/text()')
            particulars = ''.join(particulars).strip()
            if particulars == '':
                particulars_xpath = html.xpath('//div[@class="contentTest"]')[0]
                particulars_string = etree.tostring(particulars_xpath, encoding='utf-8').decode('utf-8')
                particulars_list = re.findall('>(.*?)<', particulars_string)
                particulars = ''.join(particulars_list).strip()

            img_url = html.xpath('//div[@class="acadImg"]/img/@src')[0]
            img_url = url.rsplit('/', 1)[0] + img_url.strip('.')
            person_id = self.get_person_id(name)
            temp_json = {
                'person_id': person_id,
                'name': name,
                'particulars': particulars,
                'img_url': img_url,
            }
            print('name = ', name, img_url)
            temp_string = json.dumps(temp_json, ensure_ascii=False)
            with open('data.json', 'a+', encoding='utf-8') as f:
                f.write('{}\n'.format(temp_string))

            self.download_img(img_url, person_id)
        else:
            logger.info(f'错误响应码为{response.status_code}')


    def download_img(self, img_url, img_name):
        """
        下载图片
        :param img_url: 图片的url
        :param img_name: 图片名
        :return:
        """
        logger.info('获取图片')
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(self.file_path + '{}.jpg'.format(img_name), 'wb') as fd:
                # 每到128位就写入
                for chunk in response.iter_content(128):
                    fd.write(chunk)
        else:
            logger.info(f'获取图片失败： 错误响应码为{response.status_code}')


    def get_name_id(self):
        """
        获取人的id
        :return:
        """
        # df = pd.read_excel('手动采集照片.xls')
        # df = df.drop_duplicates(subset='chinese_name')

        df = pd.read_csv('已故院士.csv')
        df = df.drop_duplicates(subset='chinese_name')
        print(df)
        # df.to_excel('A.xlsx', index=False)
        return df

    def get_person_id(self, name):
        print('name= ', name)
        try:
            df = self.df_name_id[self.df_name_id['chinese_name'] == name]
            person_id = df['person_id'].values.tolist()[0]
        except:
            person_id = name
        return person_id

def main():
    """
    下载院士信息和图片
    :return:
    """
    academician = Academician()
    academician.get_acade_url()


if __name__ == '__main__':
    main()
