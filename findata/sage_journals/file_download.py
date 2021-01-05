import requests
import pymongo
import json
from loguru import logger
import os
import time
import re


myclient = pymongo.MongoClient('mongodb://*********:27017/')
mydb = myclient['dataset']  # 数据库
mycol = mydb['sage_journals_data']  # 表


class SageJournalsFileDownload:
    def __init__(self):
        self.path = '/mnt/findata/sage_journals'


    def download_url(self, data):
        download_url = data['download_url']
        file_name = data['file_name']
        logger.info(f'{file_name} 下载， 文件路径为 {download_url}')
        if 'versions' not in download_url:
            path_name = download_url.split('/')[-1]
        else:
            path_name = re.findall('articles/(\d+)/', download_url)[0]
            file_name = f'{path_name}.zip'
        logger.info(f'文件夹为{path_name}， 文件名字为 {file_name}')
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
        data1 = [{'download_url': _['download_url'], 'file_name': _['file_name']} for _ in
                 mycol.find({}, {'download_url', 'file_name'}) if _['download_url'] != '']
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
    文件下载
    :return:
    """
    while True:
        try:
            # 下载一会就回拒绝连接
            sage = SageJournalsFileDownload()
            no_download = sage.get_no_download_file()
            for download in no_download:
                sage.download_url(download)
        except Exception as e:
            logger.info(f'e = {e}')
            logger.info('发生异常，休眠一分钟重新启动')
            time.sleep(60)


if __name__ == '__main__':
    main()
