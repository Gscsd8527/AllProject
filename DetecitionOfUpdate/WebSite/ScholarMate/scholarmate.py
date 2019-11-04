import requests
from lxml import etree
from config import logger


def IsUpdate():
    COOKIES = {
        'locale_request_change_attr': 'zh_CN',
        'JSESSIONID': 'DA43DBC6C8FB21E83C999128CA7B6B11-n1',
        'AID': 'b9cf123a9b6bbf15ed9ca867c6bf4657',
        'OAUTH_LOGIN': 'true',
        'SYS': 'SNS',
        'Hm_lvt_bd14b57728d0fd166b45b6787a509aca': '1571037437',
        '__utma': '31316797.1308612187.1571037438.1571037438.1571037438.1',
        '__utmc': '31316797',
        '__utmz': '31316797.1571037438.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'Hm_lpvt_bd14b57728d0fd166b45b6787a509aca': '1571037983',
        '__utmb': '31316797.6.10.1571037438'
    }
    DATA = {
        'allFilterValues': {},
        'page.totalCount': -1,
        'page.pageNo': 1,
        'currentLoad': 0,
        'searchString': '论文',
    }
    url = 'https://www.scholarmate.com/pub/search/ajaxpdwhpaperlist'
    response = requests.post(url, cookies=COOKIES, data=DATA)
    num = 0
    if response.status_code == 200:
        isUpdate = 0
        text = response.text
        html_data = etree.HTML(text)
        num = html_data.xpath('//div[@class="js_listinfo"]/@smate_count')[0]
    else:
        isUpdate = 1
    return isUpdate, int(num)


def WebSiteUpdate():
    IsNumsUpdate = 0
    nums = 0
    try:
        isUpdate, nums = IsUpdate()
        logger.info('[WebSite: SxholarMate] : 网站能正常抓取，并没有更新')
    except Exception as e:
        isUpdate = 1
        logger.error('[WebSite: SxholarMate] : 发生错误， 错误原因为： ', e)
    return isUpdate, IsNumsUpdate, nums


def scholarmateUpdate():
    isUpdate, IsNumsUpdate, nums = WebSiteUpdate()
    resp_json = {
        'isUpdate': isUpdate,
        'IsNumsUpdate': IsNumsUpdate,
        'webName': '科研之友',
        'newNum': nums
    }
    return resp_json

