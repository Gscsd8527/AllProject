# utf-8
import sys
import requests
import http.cookiejar
import re
import os
import logging
import json
import random

par_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(par_dir)


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


LOGIN_URL = "https://www.kaggle.com/account/login"

DATA_URL = "https://www.kaggle.com/nguyenhoc/plane-crash/version/1"

MY_USER_AGENT = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]

headers = {
    'User-Agent': random.choice(MY_USER_AGENT),
    "Host": "www.kaggle.com",
    "Referer": "https://www.kaggle.com/"
}

IPLIST = [
    "59.62.51.56:6888",
    "59.62.51.185:6888",
    "59.62.51.222:6888",
    "59.62.50.254:6888",
    "218.64.146.21:6888",
]

def getAgency():
    random_ip = random.choice(IPLIST)
    random_ip = 'https://' + random_ip
    # print('random_ip= ', random_ip)
    return random_ip

def getFileInformation():
    f = open('url.json', 'r', encoding='utf-8')
    data = f.read()
    data_list = data.split('\n')
    index = 510
    for dt in data_list[index:1000]:
        if len(dt):
            data_json = json.loads(dt)
            datasetId = data_json['datasetId']
            file_url = data_json['file_url']
            print('共有 {}  个文件, 正在下载第  {}  个'.format(len(data_list), index))
            logger.info('共有 {}  个文件, 正在下载第  {}  个'.format(len(data_list), index))
            file_name = re.findall('downloads/(.*?)/', file_url)[0]
            download(datasetId, file_name, file_url)
            index += 1


def download(datasetId, file_name, download_url):
    # ip = getAgency()
    # print('ip= ', ip)
    try:
        session = requests.Session()
        session.cookies = http.cookiejar.LWPCookieJar("cookie")
        try:
            session.cookies.load(ignore_discard=True)
        except IOError:
            pass
        # session.get("https://www.kaggle.com", proxies={'https': ip})
        session.get("https://www.kaggle.com")
        cookies_home = {}
        for item in session.cookies:
            cookies_home[item.name] = item.value
        user = random.choices([
            {
                "username": "Gscsd8527",
                "password": "1234567",
            },
            {
                "username": "chichi",
                "password": "c289836256",
            },
            {
                "username": "John3689",
                "password": "wobushitanzhenhua",
            },
            {
                "username": "sham123",
                "password": "1234567",
            }
        ])
        print(user[0])
        username = user[0]['username']
        password = user[0]['password']
        resp_login = session.post(LOGIN_URL, data={
            "X-XSRF-TOKEN": cookies_home["XSRF-TOKEN"],
            "__RequestVerificationToken": cookies_home["XSRF-TOKEN"],
            "username": username,
            "password": password,
            "rememberme": "true",
        }, headers=headers)
        # }, headers=headers, proxies={'https': ip})

        if resp_login.status_code == 200:
            logger.info('login active')
            print("登陆成功!!!")
        else:
            print("登陆失败!!!")
            logger.error('login error!!!')
            sys.exit(1)
        try:
            isExists = os.path.exists('E:/Kaggle/file0-1000/{}'.format(datasetId))
            # isExists = os.path.exists('/data/www/html/dataset/Kaggle/{}'.format(datasetId))
            if not isExists:
                os.makedirs('E:/Kaggle/file0-1000/{}'.format(datasetId))
            print('datasetID = ', datasetId)
            print('file_ulr = ', download_url)
            resp_data = session.get(download_url, timeout=1200)
            # resp_data = session.get(download_url, timeout=1200, proxies={'https': ip})
            if resp_data.status_code == 200:
                # os.makedirs('./files/{}'.format(datasetId))
                # os.makedirs('/data/www/html/dataset/Kaggle/{}'.format(datasetId))
                with open('E:/Kaggle/file0-1000/{}/{}'.format(datasetId, file_name), 'wb') as w:
                # with open('./files/{}/{}'.format(datasetId, file_name), 'wb') as w:
                # with open('/data/www/html/dataset/Kaggle/{}/{}'.format(datasetId, file_name), 'wb') as w:
                    w.write(resp_data.content)
                print('---------------文件下载完毕---------------')
                logger.info('---------------文件下载完毕---------------')
                import time
                print('休眠---------')
                time.sleep(random.uniform(5, 10))
                # time.sleep(10)
            else:
                os.removedirs('E:/Kaggle/file0-1000/{}'.format(datasetId))
                qs = {
                    'datasetId': datasetId,
                    'file_url': download_url
                }
                qs_json = json.dumps(qs)
                with open('queshi.json', 'a+', encoding='utf-8') as f:
                    f.write(qs_json)
                    f.write('\n')
                logger.info('请求文件链接报错：{}'.format(resp_data.status_code))
            # else:
            #     logger.info('文件已经下载过了----------')

        except Exception as e:
            logger.error('下载超时或者下载过程中报错')
            logger.error(e)
            qs = {
                'datasetId': datasetId,
                'file_url': download_url
            }
            qs_json = json.dumps(qs)
            with open('queshi.json', 'a+', encoding='utf-8') as f:
                f.write(qs_json)
                f.write('\n')

    except Exception as e:
        logger.error(e)
        # print('e= ', e)

def main():
    getFileInformation()

if __name__ == '__main__':
    main()
