import requests
import requests_ftp
from loguru import logger
import os
import time
requests_ftp.monkeypatch_session()


class Pubchem:
    def __init__(self):
        self.base_url = 'ftp://ftp.ncbi.nlm.nih.gov/pubchem'
        self.session = requests.Session()
        self.file_url = set()
        self.path_url = list()
        self.path = '/mnt/findata/'


    def get_dir(self, url):
        """
        获取目录
        :return:
        """
        response = self.session.list(url)
        response.encoding = 'utf-8'
        text = response.text
        dir_list = text.split('\n')
        dir_list = [_.strip('\r').replace('./', '') for _ in dir_list if _ != '']
        dir_list = [{'file_type': _.split()[0], 'file_name': _.split()[-1], 'pg_up_url': url} for _ in dir_list]
        self.get_file_url(dir_list)


    def get_file_url(self, dir_list):
        """
        获取 文件url 及 文件路径url
        :param dir_list: dir 目录链接
        :return:
        """
        for _ in dir_list:
            file_type = _['file_type']
            if file_type[0] != 'd':
                logger.info(f'文件url： {_["pg_up_url"]}/{_["file_name"]}')
                self.file_url.add(f'{_["pg_up_url"]}/{_["file_name"]}')
                logger.info(f'{_["pg_up_url"]}/{_["file_name"]}')
                with open('file_url.txt', 'a+', encoding='utf-8') as f:
                    f.write('{}\n'.format(f'{_["pg_up_url"]}/{_["file_name"]}'))
            else:
                path_url = f'{_["pg_up_url"]}/{_["file_name"]}'
                if path_url not in self.path_url:
                    self.path_url.append(path_url)


    def get_need_url(self):
        """
        获取
        :return:
        """
        try:
            f = open('yzq.txt', 'r', encoding='utf-8')
            set1 = set(_.strip('\n') for _ in f.readlines())
        except:
            set1 = set()
        f2 = open('file_url.txt', 'r', encoding='utf-8')
        set2 = set([_.strip('\n') for _ in f2.readlines()])
        set3 = set2 - set1
        data = [{'file_url': _.strip('\n'), 'file_name': _.strip('\n').rsplit('/', 1)[-1], 'path_name': self.path + _.strip('\n').
            replace('ftp://ftp.ncbi.nlm.nih.gov/', '').replace(_.strip('\n').rsplit('/', 1)[-1], '').strip('/')} for _ in set3]
        logger.info(f'已抓取的 {len(set1)} 总的  {len(data)}')
        data = [_ for _ in data if _['file_url'] not in set1]
        return data


    def download_url(self, data):
        download_url = data['file_url']
        file_name = data['file_name']
        path_name = data['path_name']
        logger.info(f'文件夹为{path_name}   文件名字为 {file_name}  文件下载路径为 {download_url}')
        try:
            session = requests.Session()
            response = session.get(download_url, timeout=14400)
            if response.status_code == 200:
                try:
                    is_exists = os.path.exists('{}/'.format(path_name))
                    if not is_exists:
                        os.makedirs('{}/'.format(path_name))  # makedirs：创建多级目录

                    with open('{}/{}'.format(path_name, file_name), 'wb') as f:
                        f.write(response.content)

                    with open('yzq.txt', 'a+', encoding='utf-8') as yzq:
                        yzq.write('{}\n'.format(download_url))
                except Exception as e:
                    logger.info(f'发生异常 {e}')
            else:
                logger.info(f'错误响应码为{response.status_code}')
        except Exception as e:
            logger.info(f'请求发送异常： {str(e)}')


def main():
    """
    ftp://ftp.ncbi.nlm.nih.gov/pubchem  文件下载
    :return:
    """
    pubchem = Pubchem()
    # pubchem.get_dir(pubchem.base_url)
    # print(pubchem.file_url)
    # print(pubchem.path_url)
    # while len(pubchem.path_url):
    #     logger.info(f'path_url 还有 {len(pubchem.path_url)}')
    #     spider_path = pubchem.path_url.pop()
    #     logger.info(f'抛出的路径为 {spider_path}')
    #     pubchem.get_dir(spider_path)

    while True:
        try:
            # 下载一会就回拒绝连接
            no_download = pubchem.get_need_url()
            for download in no_download:
                pubchem.download_url(download)
        except Exception as e:
            logger.info(f'e = {e}')
            logger.info('发生异常，休眠一分钟重新启动')
            time.sleep(60)


if __name__ == '__main__':
    main()
