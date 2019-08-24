import requests
import re
import json
import datetime
from crawle_server import logger
Session = requests.session()


HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def getToken():
    headers = HEADERS.copy()
    headers['upgrade-insecure-requests'] = '1'
    url = 'https://www.kaggle.com/datasets'
    response = Session.get(url, headers=headers)
    token = ''
    if response.status_code == 200:
        text = response.text
        token = re.findall("antiForgeryToken: '(.*?)',", text)[0]
    else:
        print('错误响应码为： ', response.status_code)
    return token

def getFirstData(token):
    data = {
        "page": 1,
        "group": "public",
        "size": "all",
        "fileType": "all",
        "license": "all",
        "viewed": "all",
        "categoryIds": [],
        "search": "",
        "sortBy": "hottest",
        "userId": None,
        "organizationId": None,
        "maintainerOrganizationId": None,
        "minSize": None,
        "maxSize": None,
        "isUserQuery": 'false'
    }
    url = 'https://www.kaggle.com/requests/SearchDatasetsRequest'
    headers = HEADERS.copy()
    temp_headers = {
        '__requestverificationtoken': token,
        'accept': 'application/json',
        'content-type': 'application/json',
        'Referer': 'https://www.kaggle.com/datasets',
        'x-xsrf-token': token
    }
    headers.update(temp_headers)
    response = Session.post(url, data=json.dumps(data), headers=headers)
    text = response.text
    data_json = json.loads(text)
    items = data_json['result']['items']
    nums = data_json['result']['totalResults']

    f = open('webSite/KaggleNums.json', 'r', encoding='utf-8')
    data = f.read()
    data_list = data.split('\n')
    lastData = json.loads(data_list[-2])
    lastNums = lastData['nums']
    IsNumsUpdate = 0
    if nums > lastNums:
        IsNumsUpdate = 1
        logger.info('[WebSite: Kaggle]: 网站数据量已更新')

    nums_json = {
        'time': str(datetime.datetime.now()),
        'nums': nums
    }
    data_json = json.dumps(nums_json, ensure_ascii=False)
    with open('webSite/KaggleNums.json', 'a+', encoding='utf-8') as f:
        f.write(data_json)
        f.write('\n')
    return IsNumsUpdate, lastNums, nums


def WebSiteUpdate():
    """
    检测网站是否更新，通过原有的抓取数据手段来判断
    :return:
    """
    IsNumsUpdate = 0
    lastNums, nums = 0, 0
    try:
        token = getToken()
        IsNumsUpdate, lastNums, nums = getFirstData(token)
        isUpdate = 0
        logger.info('[WebSite: Kaggle] : 网站能正常抓取，并没有更新')
    except Exception as e:
        isUpdate = 1
        logger.error('[WebSite: Kaggle] : 发生错误， 错误原因为： ', e)
    return isUpdate, IsNumsUpdate, lastNums, nums



def KaggleUpdate():
    isUpdate, IsNumsUpdate, lastNums, nums = WebSiteUpdate()
    resp_json = {
        'isUpdate': isUpdate,
        'IsNumsUpdate': IsNumsUpdate,
        'webName': 'Kaggle',
        'lastNum': lastNums,
        'newNum': nums
    }
    return resp_json
