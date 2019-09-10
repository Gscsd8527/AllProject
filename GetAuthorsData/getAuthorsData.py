import json
import requests
import uuid
import random
import threading
Lock = threading.Lock()

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

class Authors(object):
    AuthorsSet = []
    def __init__(self):
        self.url = 'https://academic.microsoft.com/api/entity/author/{}?paperId=undefined'
        self.referer_url = 'https://academic.microsoft.com/author/{}/publication/search?q={}&qe=Composite(AA.AuId={})&f=&orderBy=0'
        # self.AuthorsData = self.getAuthorsData()

    # def Request(self):
    #     for author in self.AuthorsData:
    #         author_id = author['id']
    #         author_name = author['name']
    #         try:
    #             if author_id not in self.AuthorsSet:
    #                 self.AuthorsSet.append(author_id)
    #                 url = self.url.format(author_id)
    #                 referer = self.referer_url.format(author_id, author_name, author_id)
    #                 headers = self.getHeaders()
    #                 headers['Referer'] = referer
    #                 response = requests.get(url, headers=headers)
    #                 if response.status_code == 200:
    #                     text = response.text
    #                     data_json = json.loads(text)
    #                     self.parseData(data_json, author, self.url)
    #                 else:
    #                     print('错误响应码为： ', response.status_code)
    #         except Exception as e:
    #             print('e= ', e)

    def ThreadRequest(self, author):
        author_id = author['id']
        author_name = author['name']
        try:
            if author_id not in self.AuthorsSet:
                self.AuthorsSet.append(author_id)
                url = self.url.format(author_id)
                referer = self.referer_url.format(author_id, author_name.encode('utf-8'), author_id)
                headers = self.getHeaders()
                headers['Referer'] = referer
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    text = response.text
                    data_json = json.loads(text)
                    self.parseData(data_json, author, self.url)
                else:
                    print('错误响应码为： ', response.status_code)
            else:
                print('数据重复-----')
        except Exception as e:
            print('e= ', e)

    @staticmethod
    def parseData(data_json, init_data, url):
        name = data_json['entity']['dn']
        id = data_json['entity']['id']
        description = data_json['entity']['d']
        organization = {}
        try:
            organization_name = data_json['entity']['ci']['dn']
            organization_id = data_json['entity']['ci']['id']
            lat = data_json['entity']['ci']['lat']
            lon = data_json['entity']['ci']['lon']
            organization = {
                'organization_name': organization_name,
                'organization_id': organization_id,
                'lat': lat,
                'lon': lon,
            }
        except:
            pass
        author_img = ''
        try:
            author_img = data_json['entity']['iurl']
        except:
            pass
        author_fiurl = ''
        try:
            author_fiurl = data_json['entity']['fiurl']
        except:
            pass

        publications = data_json['entity']['pc']
        citations = data_json['entity']['eccnt']
        tags = [i['id'] for i in data_json['entity']['t']]
        reference_list = []
        try:
            reference_list = data_json['entity']['w']
        except:
            pass
        uid = uuid.uuid1()
        suid = str(uid).replace('-', '')
        author_data = {
            'datasetId': suid,
            'name': name,
            'id': id,
            'description': description,
            'organization': organization,
            'author_img': author_img,
            'author_fiurl': author_fiurl,
            'publications': publications,
            'citations': citations,
            'tags': tags,
            'reference_list': reference_list,
            'url': url,
            'init_data': init_data,
            'data_json': data_json,
        }
        # print(author_data)
        data_string = json.dumps(author_data)
        Lock.acquire()
        with open('AuthorsJson.json', 'a+', encoding='utf-8') as f:
            f.write(data_string)
            f.write('\n')
        Lock.release()


    @staticmethod
    def getHeaders():
        headers = {
            'Accept': 'application/json',
            'X-Requested-With': 'Fetch',
            'User-Agent': random.choice(MY_USER_AGENT),
        }
        return headers


    @staticmethod
    def getAuthorsData():
        AuthorsId = []
        f = open('BiologyAuthorsID.json', 'r', encoding='utf-8')
        # f = open('aa.json', 'r', encoding='utf-8')
        data = f.read()
        data_list = data.split('\n')
        for dt in data_list:
            if len(dt):
                data_json = json.loads(dt)
                AuthorsId.append(data_json)
        return AuthorsId

def start_thread():
    authors = Authors()
    AuthorsId = authors.getAuthorsData()[200:]
    nums = len(AuthorsId)
    # 循环次数
    x = nums // THREAD_NUM
    # 剩余量
    y = nums % THREAD_NUM
    xs = x + 2
    for i in range(xs):
        print('循环第  {}  次， 共有  {}  次'.format(i, xs-2))
        print('****************')
        if i == x + 1:
            AuthorsData = AuthorsId[i * THREAD_NUM:]
        else:
            AuthorsData = AuthorsId[i * THREAD_NUM: (i + 1) * THREAD_NUM]
        threads = [threading.Thread(target=authors.ThreadRequest, args=(author,)) for author in AuthorsData]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print('*******---********')

def main():
    start_thread()
    # authors.Request()

if __name__ == '__main__':
    THREAD_NUM = 10
    main()
