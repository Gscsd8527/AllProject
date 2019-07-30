import requests
import re
import pymongo
from ZhongKeYuan.Chinatech.city import getCity
from lxml import etree
import uuid
import datetime

myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = myclient['Chinatech']  # 数据库
myurls = mydb['sbj_url']  # 表
mydata = mydb['sbj_data']


Cookie = 'ASPSESSIONIDQWRSTSTA=PNMFALPDHNBIBHPGLDMFKDCF; ASPSESSIONIDQWQRQQRC=LGMNOGMAPEHMCEIILNOFAJMC'

def parseUrl(Session):
    urls = myurls.find()
    print('已抓取：  ', myurls.find({'is_read': 1}).count())
    for dt in urls:
        url = dt['url']
        is_read = dt['is_read']
        if is_read == 0:
            uid = uuid.uuid1()
            suid = str(uid).replace('-', '')
            # 1. 成果唯一标识
            datasetId = suid
            doi = ''
            handle = ''
            spiderDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_json = {
                'datasetId': datasetId,
                'doi': doi,
                'handle': handle,
                'classType': '省部级',
                'souce': url,
                'spiderDateTime': spiderDateTime
            }
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': Cookie,
                'Host': 'www.chinatech.gov.hk',
                'Referer': '',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            }
            try:
                header['Referer'] = url
                new_url = re.sub('(recordID=.*?)&', '', url)
                new_url = re.sub(r'index.asp', r'index_content.asp', new_url)
                response = Session.get(new_url, headers=header, timeout=100)
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    html = response.text
                    # print(html)
                    html = html.replace('\n', '')
                    re_complice = re.compile('<form name="form1" method="POST">.*?(<table.*?</table>)')
                    table = re.findall(re_complice, html)
                    dct = {}
                    if len(table):
                        table_str = table[0]
                        table_html = etree.HTML(table_str)
                        data = table_html.xpath('//table/tr')
                        for dt in data:
                            name = dt.xpath('./td[1]/text()')[0]
                            if name == '负责人':
                                temp_dct = {}
                                value = dt.xpath('./td[2]/text()')
                                values = [i.replace('\r', '').strip(' ') for i in value]
                                for i in values:
                                    dt = i.split(':')
                                    v_name = dt[0].strip(' ')
                                    v_value = dt[1].strip(' ')
                                    temp_dct[v_name] = v_value
                                    value = temp_dct
                            else:
                                value = dt.xpath('./td[2]/text()')[0]
                            dct[name] = value
                            data_json.update(dct)
                    try:
                        if dct != {}:
                            print('data_json = ', data_json)
                            mydata.insert_one(data_json)
                            # col.insert_one(data_json)
                            myurls.update_one(
                                {'url': url},
                                {
                                    '$set': {
                                        'is_read': 1
                                    }
                                }
                            )
                            # print('未读的URL还有： ', myurls.find({'is_read': 0}).count())
                        else:
                            print('dct 为空')
                    except Exception as e:
                        print('insert= ', e)
                else:
                    print('响应码为： ', response.status_code)

            except Exception as e:
                print(e)

def firstRequest(Session, province_id, city_id):
    url = 'https://www.chinatech.gov.hk/gb/search/query.asp'
    arg = {
        '中科院': 1,
        '省部共建': 2,
        '企业': 3,
        '行业': 4,
        '市级': 5,
        '国家级': 6,
        '民营': 7,
        '省部级': 8,
        '高校': 9,
        '其他': 10
    }
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': Cookie,
        'Host': 'www.chinatech.gov.hk',
        'Origin': 'https://www.chinatech.gov.hk',
        # 'Referer': 'https://www.chinatech.gov.hk/gb/search/index_content.asp?act=',
        'Referer': 'https://www.chinatech.gov.hk/gb/search/index_content.asp?act=chgpro',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    data = {
        'act': 'chgpro',
        'reset': '',
        'province': province_id,
        'city': city_id,
        'institution': '',
        'srchmtd': '1',
        'subjectarea': '-1',
        'insttype': arg['省部级'],
        'free': '',
        'record': '50'
    }
    response = Session.post(url, data=data, headers=header)
    if response.status_code == 200:
        headers = response.headers
        headers_dict = {}
        for k, v in headers.items():
            headers_dict[k] = v
        print(headers_dict)
    else:
        print('错误响应码为; ', response.status_code)

def getUrl(Session):
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': Cookie,
        'Host': 'www.chinatech.gov.hk',
        'Referer': '',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    for i in range(1, 11):
        print('第  {}   页'.format(i))
        url = 'https://www.chinatech.gov.hk/gb/search/resultlist_content.asp?page={}&pagesize=50'.format(i)
        HEADERS['Referer'] = url
        response = Session.get(url, headers=HEADERS, timeout=100)
        response.encoding = 'utf-8'
        html = response.text
        html = html.replace('\n', '')
        re_compile = re.compile('<a href="(../result/index\.asp.*?)"')
        urls = re.findall(re_compile, html)
        Urls = [i.replace('..', 'https://www.chinatech.gov.hk/gb') for i in urls]
        for url in Urls:
            print('url= ', url)
            if not myurls.find({'url': url}).count():
                data_json = {
                    'url': url,
                    'is_read': 0
                }
                try:
                    myurls.insert_one(data_json)
                except Exception as e:
                    print('插入错误： ', e)
                parseUrl(Session)
            else:
                print('该url已经存在数据库中了')


def main():
    Data = getCity()
    for dt in Data:
        Session = requests.session()
        province_name = dt[0]
        province_id = dt[1]
        city_id = dt[2]
        print(province_name, province_id, city_id)
        firstRequest(Session, province_id, city_id)
        getUrl(Session)
        print('=======================================================')


if __name__ == '__main__':
    main()

