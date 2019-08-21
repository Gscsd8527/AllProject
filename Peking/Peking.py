from lxml import etree
import time
import uuid
from selenium import webdriver
import pymongo
import datetime
import json


# 远程数据库
myclient = pymongo.MongoClient('mongodb://****:27017/')
mydb = myclient['DataSet']  # 数据库
myurl = mydb['Peking_url']  # 存放数据表
mycol = mydb['Peking_dataset']

BASE_URL = 'http://opendata.pku.edu.cn'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}


# 引用规则和格式
def getCitationPolicy(html_data):
    citationPolicy = ''
    try:
        citationPolicy_list = html_data.xpath('//span[@class="citation-select"]//text()')
        citationPolicy_new_list = [i.strip(' ').replace('\n', '') for i in citationPolicy_list]
        citationPolicy = ''.join(citationPolicy_new_list)
    except Exception as e:
        print('citationPolicy error= ', e)
    return citationPolicy

# 获取元数据
def getMetaData(driver):
    print('========点击元数据========')
    MetaData = {}
    # 点击元数据
    html = ''
    try:
        try:
            # 将页面拉到底部
            js = "var q=document.documentElement.scrollTop=400"
            driver.execute_script(js)
            driver.find_element_by_xpath('//*[@id="datasetForm:tabView"]/ul/li[2]').click()
        except:
            # 将页面拉到底部
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            driver.find_element_by_xpath('//*[@id="datasetForm:tabView"]/ul/li[2]').click()
        time.sleep(5)
        html = driver.find_element_by_xpath('//div[@id="datasetForm:tabView:metadataMapTab"]/div[@class="panel-group"]').get_attribute('outerHTML')
        # print(html)
        html_data = etree.HTML(html)
        groups = html_data.xpath('.//div[@class="panel panel-default"]')
        gp = 1
        for group in groups:
            name = group.xpath('./div[@class="panel-heading text-info"]/text()')[0].strip('\n').replace('\xa0', '').strip(' ')
            form_groups = group.xpath('.//div[@class="form-group"]')
            gp += 1
            data_dict = {}
            for form_group in form_groups:
                try:
                    filed_name = form_group.xpath('./label/text()')[0].replace('\n', '').strip(' ').replace(r'\n', '')
                    filed_value_list = form_group.xpath('./div[@class="col-sm-9"]//text()')
                    if len(filed_value_list) == 1:
                        filed_value = filed_value_list[0].replace('\n', '').strip(' ')
                    elif len(filed_value_list) > 1:
                        filed_value = [i.replace('\n', '').strip(' ') for i in filed_value_list]
                    else:
                        filed_value = ''
                    data_dict[filed_name] = filed_value
                except Exception as e:
                    pass
            MetaData[name] = data_dict
        # 数据集持久标识
    except Exception as e:
        print('--e', e)
    return MetaData, html

# 获取许可和条款
def getLicenseTerms(driver):
    print('========获取许可和条款========')
    LicenseTerms = {}
    html = ''
    try:
        try:
            # 将页面拉到底部
            js = "var q=document.documentElement.scrollTop=450"
            driver.execute_script(js)
            driver.find_element_by_xpath('//*[@id="datasetForm:tabView"]/ul/li[3]').click()
        except:
            # 将页面拉到底部
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            driver.find_element_by_xpath('//*[@id="datasetForm:tabView"]/ul/li[3]').click()
        time.sleep(3)
        html = driver.find_element_by_xpath('//*[@id="datasetForm:tabView:termsTab"]/div[@class="panel-group"]').get_attribute('outerHTML')
        html_data = etree.HTML(html)
        groups = html_data.xpath('.//div[@class="panel panel-default"]')
        for group in groups:
            name = group.xpath('./div[@class="panel-heading text-info"]/text()')[0].replace('\n', '').replace('\xa0', '').strip(' ')
            form_groups = group.xpath('.//div[@class="form-group"]')
            data_dict = {}
            for form_group in form_groups:
                try:
                    filed_name = form_group.xpath('./label/text()')[0].replace('\n', '').strip(' ').replace(r'\n', '')
                    filed_value_list = form_group.xpath('./div[@class="col-sm-9"]//text()')
                    if len(filed_value_list) == 1:
                        filed_value = filed_value_list[0].replace('\n', '').strip(' ')
                    elif len(filed_value_list) > 1:
                        filed_value = [i.replace('\n', '').strip(' ') for i in filed_value_list]
                    else:
                        filed_value = ''
                    data_dict[filed_name] = filed_value
                except Exception as e:
                    pass
            LicenseTerms[name] = data_dict
    except Exception as e:
        print(e)
    return LicenseTerms, html

index = 1
def parseUrl(url):
    global index
    print('共有 {} 条， 正在抓取第  {}  条'.format(urls.count(), index))

    print('url= ', url)
    # 1. 数据集唯一标识，使用UUID生成32位唯一标识符
    uid = uuid.uuid1()
    suid = str(uid).replace('-', '')
    datasetId = suid

    # handle
    handle = ''

    # 版本
    version = url.rsplit('=')[-1]

    # doi
    doi = url.split('=')[1].strip('&version')

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    html_data = etree.HTML(html)

    # name
    name = ''
    try:
        name = html_data.xpath('//*[@id="title"]/text()')[0].strip('\n').strip(' ')
    except Exception as e:
        print('name e= ', e)
    print('name= ', name)
    # 引用规则和格式
    citationPolicy = getCitationPolicy(html_data)
    print('citationPolicy= ', citationPolicy)

    MetaData, meta_html = getMetaData(driver)
    print('MetaData= ', MetaData)
    LicenseTerms, license_tml = getLicenseTerms(driver)
    print('LicenseTerms= ', LicenseTerms)
    try:
        driver.close()
    except:
        driver.quit()
    spiderDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_json = {
        'datasetId': datasetId,
        'handle': handle,
        'doi': doi,
        'name': name,
        'url': url,
        'version': version,
        'citationPolicy': citationPolicy,
        'MetaData': MetaData,
        'MetaData_html': meta_html,
        'LicenseTerms': LicenseTerms,
        'LicenseTerms_html': license_tml,
        'path': '',
        'html': html,
        'spiderDateTime': spiderDateTime
    }
    if (MetaData == {}) or (LicenseTerms == {}):
        pass
    else:
        try:
            mycol.insert_one(data_json)
            print('data_json= ', data_json)
            myurl.update_one(
                {'url': url},
                {
                    '$set': {'is_read': 1}
                }
            )
            print('入库并修改该链接的is_read的值')
        except Exception as e:
            pass
    index += 1


if __name__ == '__main__':
    urls = myurl.find({'is_read': 0})
    for url in urls:
        filter = ['http://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/EF9YLX&version=1.0']
        url = url['url']
        if url not in filter:
            parseUrl(url)
    # main()
    # Urls = getUrls()
    # parseUrl(Urls)

