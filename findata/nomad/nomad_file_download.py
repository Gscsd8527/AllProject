import requests
import pymongo
import json
from loguru import logger
import os
import time
import re
import copy


myclient = pymongo.MongoClient('mongodb://*********:27017/')
mydb = myclient['dataset']  # 数据库
mycol = mydb['nomad_data']  # 表


class NomadFileDownload:
    def __init__(self):
        self.path = '/mnt/findata/nomad'
        self.base_url = 'https://nomad-lab.eu/prod/rae/api/raw/'


    def download_url(self, data):
        download_url = data['file_url']
        file_name = data['file_name']
        path_name = data['path_name']
        logger.info(f'文件夹为{path_name}   文件名字为 {file_name}  文件下载路径为 {download_url}   ')
        try:
            response = requests.get(download_url, timeout=14400)
            if response.status_code == 200:
                try:
                    isExists = os.path.exists('{}/{}/'.format(self.path, path_name))
                    if not isExists:
                        os.makedirs('{}/{}/'.format(self.path, path_name))  #  makedirs：创建多级目录

                    with open('{}/{}/{}'.format(self.path, path_name, file_name), 'wb') as f:
                        f.write(response.content)

                    with open('yzq.txt', 'a+', encoding='utf-8') as yzq:
                        yzq.write('{}\n'.format(file_name))
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
        calc_id_set = set()
        try:
            f = open('yzq.txt', 'r', encoding='utf-8')
            set1 = set(_.strip('\n') for _ in f.readlines())
        except:
            set1 = set()
        calc_id_set = calc_id_set & set1
        no_download = []
        data = mycol.find({}, {'files', 'calc_id', 'upload_id'})[:100000]
        for dt in data:
            calc_id = dt['calc_id']
            files = dt['files']
            upload_id = dt['upload_id']
            if calc_id not in calc_id_set:
                for file in files:
                    temp_dict = {
                        'file_url': self.base_url + upload_id + '/' + file,
                        'file_name': file.split('/')[-1],
                        'path_name': calc_id
                    }
                    no_download.append(copy.deepcopy(temp_dict))
                calc_id_set.add(calc_id)
        logger.info(f'未下载的url还有{len(no_download)}')
        return no_download


def main():
    """
    nomad 文件下载
    :return:
    """
    while True:
        try:
            # 下载一会就回拒绝连接
            nomad = NomadFileDownload()
            no_download = nomad.get_no_download_file()
            for download in no_download:
                nomad.download_url(download)
        except Exception as e:
            logger.info(f'e = {e}')
            logger.info('发生异常，休眠一分钟重新启动')
            time.sleep(60)


if __name__ == '__main__':
    main()
