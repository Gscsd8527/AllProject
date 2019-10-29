import requests
from lxml import etree
import re
from config import logger


def IsUpdate():
    url = 'https://dataverse.harvard.edu/dataverse/harvard?q=&fq0=subject_ss%3A%22Computer+and+Information+Science%22&types=datasets&sort=dateSort&order=desc&page=1'
    response = requests.get(url)
    num = 0
    if response.status_code == 200:
        isUpdate = 0
        try:
            text = response.content
            html_data = etree.HTML(text)
            data = html_data.xpath('//span[@class="facetTypeDataset"]/text()')[0]
            num = re.findall('\((.*?)\)', data)[0]
        except:
            pass
    else:
        isUpdate = 1
    return isUpdate, int(num.strip())


def WebSiteUpdate():
    """
    检测网站是否更新，通过原有的抓取数据手段来判断
    :return:
    """
    IsNumsUpdate = 0
    nums = 0
    try:
        isUpdate, nums = IsUpdate()
        logger.info('[WebSite: Harvard] : 网站能正常抓取，并没有更新')
    except Exception as e:
        isUpdate = 1
        logger.error('[WebSite: Harvard] : 发生错误， 错误原因为： ', e)
    return isUpdate, IsNumsUpdate, nums


def HarvardUpdate():
    isUpdate, IsNumsUpdate, nums = WebSiteUpdate()
    resp_json = {
        'isUpdate': isUpdate,
        'IsNumsUpdate': IsNumsUpdate,
        'webName': 'Harvard',
        'newNum': nums
    }
    return resp_json