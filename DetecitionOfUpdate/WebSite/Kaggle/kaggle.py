import requests
import re
import json
import datetime
from config import logger

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
    return int(nums)


def WebSiteUpdate():
    """
    检测网站是否更新，通过原有的抓取数据手段来判断
    :return:
    """
    IsNumsUpdate = 0
    nums = 0
    try:
        token = getToken()
        nums = getFirstData(token)
        isUpdate = 0
        logger.info('[WebSite: Kaggle] : 网站能正常抓取，并没有更新')
    except Exception as e:
        isUpdate = 1
        logger.error('[WebSite: Kaggle] : 发生错误， 错误原因为： ', e)
    return isUpdate, IsNumsUpdate, nums


def KaggleUpdate():
    isUpdate, IsNumsUpdate, nums = WebSiteUpdate()
    resp_json = {
        'isUpdate': isUpdate,
        'IsNumsUpdate': IsNumsUpdate,
        'webName': 'Kaggle',
        'newNum': nums
    }
    return resp_json
