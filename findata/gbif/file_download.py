import requests
import pymongo
import json
from loguru import logger
import os
import time
import re


myclient = pymongo.MongoClient('mongodb://*********:27017/')
mydb = myclient['dataset']  # 数据库
mycol = mydb['gbif_data']  # 表


class GbifFileDownload:
    def __init__(self):
        self.path = '/mnt/findata/gbif'

    def download_url(self, data):
        download_url = data['url']
        file_name = data['file_name']
        path_name = data['key']
        logger.info(f'文件下载路径为 {download_url}   文件夹为{path_name}， 文件名字为 {file_name}')
        try:
            response = requests.get(download_url, timeout=14400)
            if response.status_code == 200:
                try:
                    isExists = os.path.exists('{}/{}/{}'.format(self.path, path_name, file_name))
                    if not isExists:
                        os.makedirs('{}/{}/'.format(self.path, path_name))
                    with open('{}/{}/{}'.format(self.path, path_name, file_name), 'wb') as f:
                        f.write(response.content)
                        data_string = json.dumps(data, ensure_ascii=False)
                        with open('yzq.json', 'a+', encoding='utf-8') as yzq:
                            yzq.write('{}\n'.format(data_string))
                except Exception as e:
                    logger.info(f'发生异常 {e}')

            else:
                logger.info(f'错误响应码为{response.status_code}')
        except Exception as e:
            logger.info(f'请求发送异常： {str(e)}')


    def get_no_download_file(self):
        """
        获取未下载的url
        :return:
        """
        data = mycol.find({}, {'key', 'endpoints'})
        data1 = []
        for dt in data:
            endpoints = dt['endpoints']
            if len(endpoints):
                for _ in endpoints[:1]:
                    url = _['url']
                    if '.zip' in url:
                        file_name = url.rsplit('/', 1)[-1]
                    elif 'r=' in url:
                        file_name = re.findall('r=(.*)', url)[0] + '.zip'
                    elif 'download' in url and 'document_id' in url:
                        file_name = re.findall('document_id=(.*)', url)[0] + '.zip'
                    else:
                        file_name = ''
                    if file_name:
                        data1.append({'key': dt['key'], 'url': url, 'file_name': file_name})
        try:
            f = open('yzq.json', 'r', encoding='utf-8')
            data2 = [json.loads(_.strip('\n')) for _ in f.readlines()]
        except:
            data2 = []

        no_download = []
        for dt in data1:
            if dt not in data2:
                no_download.append(dt)
        logger.info(f'未下载的url还有{len(no_download)}')
        return no_download


def main():
    """
    gbif 文件下载
    :return:
    """
    while True:
        try:
            # 下载一会就回拒绝连接
            gbif = GbifFileDownload()
            no_download = gbif.get_no_download_file()
            for download in no_download:
                gbif.download_url(download)
        except Exception as e:
            logger.info(f'e = {e}')
            logger.info('发生异常，休眠一分钟重新启动')
            time.sleep(60)


if __name__ == '__main__':
    main()
