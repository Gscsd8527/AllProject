import requests
from lxml import etree
from selenium import webdriver
import time
import json

# 页数
PAGE_NUMS = 64
VERSION_URLS = {}
# 获取待抓取的页面的url
def getUrls():
    url_list = []
    start_url = 'https://dataverse.harvard.edu/dataverse/harvard?q=&fq0=subject_ss%3A%22Computer+and+Information+Science%22&sort=dateSort&order=desc&page={}&types=datasets'
    for num in range(1, PAGE_NUMS+1):
        url = start_url.format(str(num))
        url_list.append(url)
    return url_list

# 获取每个页面中论文的url
def getPageUrls(urls):
    page_urls = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print('==解析==')
                html = response.content
                html_data = etree.HTML(html)
                datas = html_data.xpath('//table[@id="resultsTable"]/tbody/tr')
                for url in datas:
                    ul = url.xpath('.//div[@class="card-title-icon-block"]/a/@href')[0]
                    ul = 'https://dataverse.harvard.edu' + ul
                    page_urls.append(ul)
            else:
                print('失败： ', response.status_code)
        except Exception as e:
            print(e)
    print('page_urls = ', page_urls)
    return page_urls


# 获取每篇论文对应的版本url
def getPageVersionUrls(page_urls):
    for url in page_urls:
        try:
            driver = webdriver.Firefox()
            driver.get(url)
            time.sleep(3)
            # 将页面拉到底部
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            # ActionChains(driver).move_to_element(driver.find_element_by_xpath('//ul[@class="ui-tabs-nav ui-helper-reset ui-widget-header ui-corner-all"]/li[4]')).perform()
            driver.find_element_by_xpath('//ul[@class="ui-tabs-nav ui-helper-reset ui-widget-header ui-corner-all"]/li[4]').click()
            time.sleep(3)
            html = driver.page_source
            html_data = etree.HTML(html)
            url_data = html_data.xpath('//a[@id="versionLink"]/@href')
            temp_list = []
            for ver_url in url_data:
                ver_url = 'https://dataverse.harvard.edu' + ver_url
                temp_list.append(ver_url)
                VERSION_URLS[url] = temp_list
                print(ver_url)


            driver.close()
        except Exception as e:
            with open('miss_url.txt', 'a+', encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
            print(e)



def main():
    url_list = getUrls()
    page_urls = getPageUrls(url_list)
    getPageVersionUrls(page_urls)
    data_json = json.dumps(VERSION_URLS)
    with open('version_url.txt', 'a+', encoding='utf-8') as f:
        f.write(data_json)
        f.write('\n')



if __name__ == '__main__':
    main()