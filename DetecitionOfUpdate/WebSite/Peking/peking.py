import requests
from lxml import etree
import re
from config import logger


def IsUpdate():
    url = 'https://opendata.pku.edu.cn/dataverse.xhtml?q=&types=datasets&sort=dateSort&order=desc&page=1'
    isUpdate, num = 0, 0
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            try:
                text = response.content
                html_data = etree.HTML(text)
                data = html_data.xpath('//span[@class="facetTypeDataset"]/text()')[0]
                num = re.findall('\((.*?)\)', data)[0]
            except:
                pass
        else:
            isUpdate = 1
        if isinstance(num, str):
            num = int(num.strip())
        return isUpdate, num
    except:
        pass


def WebSiteUpdate():
    """
    检测网站是否更新，通过原有的抓取数据手段来判断
    :return:
    """
    IsNumsUpdate = 0
    nums = 0
    try:
        isUpdate, nums = IsUpdate()
        logger.info('[WebSite: Peking] : 网站能正常抓取，并没有更新')
    except Exception as e:
        isUpdate = 1
        logger.error('[WebSite: Peking] : 发生错误， 错误原因为： ', e)
    return isUpdate, IsNumsUpdate, nums


def PekingUpdate():
    isUpdate, IsNumsUpdate, nums = WebSiteUpdate()
    resp_json = {
        'isUpdate': isUpdate,
        'IsNumsUpdate': IsNumsUpdate,
        'webName': '北大开放平台',
        'newNum': nums
    }
    return resp_json