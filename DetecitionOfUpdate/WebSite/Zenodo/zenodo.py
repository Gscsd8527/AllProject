import requests
import json
from config import logger
import datetime

def getFirstData():
    nums = 0
    headers = {
        'Accept': 'application/vnd.zenodo.v1+json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    # 查询这两个关键词的字段的个数
    key_list = ['computer science', 'computer information']
    for key in key_list:
        logger.info('[WebSite: Zenodo] : 当前关键词为  {}'.format(key))
        init_url = 'https://zenodo.org/api/records/?page=1&size=20&q={}&access_right=open&access_right=embargoed&type=dataset'.format(
            key)
        headers[
            'Referer'] = 'https://zenodo.org/search?page=1&size=20&q={}&access_right=open&access_right=embargoed'.format(
            key)
        response = requests.get(init_url, headers=headers)
        if response.status_code == 200:
            text = response.text
            data_json = json.loads(text)
            total = data_json['hits']['total']
            nums += int(total)

    f = open('webSite/Zenodo/ZenodoNums.json', 'r', encoding='utf-8')
    data = f.read()
    data_list = data.split('\n')
    lastData = json.loads(data_list[-2])
    lastNums = lastData['nums']
    IsNumsUpdate = 0
    if nums > lastNums:
        IsNumsUpdate = 1
        logger.info('[WebSite: Zenodo]: 网站数据量已更新')
    nums_json = {
        'time': str(datetime.datetime.now()),
        'nums': nums
    }
    data_json = json.dumps(nums_json, ensure_ascii=False)
    with open('webSite/Zenodo/ZenodoNums.json', 'a+', encoding='utf-8') as f:
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
        IsNumsUpdate, lastNums, nums = getFirstData()
        isUpdate = 0
        logger.info('[WebSite: Zenodo] : 网站能正常抓取，并没有更新')
    except Exception as e:
        isUpdate = 1
        logger.error('[WebSite: Zenodo] : 发生错误， 错误原因为： {}'.format(e))
    return isUpdate, IsNumsUpdate, lastNums, nums

def ZenodoUpdate():
    isUpdate, IsNumsUpdate, lastNums, nums = WebSiteUpdate()
    resp_json = {
        'isUpdate': isUpdate,
        'IsNumsUpdate': IsNumsUpdate,
        'webName': 'Zenodo',
        'lastNum': lastNums,
        'newNum': nums
    }
    return resp_json