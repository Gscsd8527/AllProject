from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains
import re
import json
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait       #WebDriverWait注意大小写
from selenium.webdriver.common.by import By

class Dans:
    def __init__(self):
        # self.driver = webdriver.PhantomJS(executable_path='D:\software\PhantomJS\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
        self.driver = webdriver.Chrome()
        self.js = 'window.open("{}");'
        self.base_url = 'https://easy.dans.knaw.nl/ui/browse'
        self.join_url = 'https://easy.dans.knaw.nl/ui/'


    def request(self):
        index = 1
        while index:
            print(f'index = {index}')
            if index == 1:
                self.driver.get(self.base_url)
            else:
                js = "var q=document.documentElement.scrollTop=100000"
                self.driver.execute_script(js)
                # print(self.driver.page_source)
                # self.driver = WebDriverWait(self.driver, 10).until(EC.find_element_by_xpath((By., 'kw')))
                # element = WebDriverWait(self.driver, 100).until(
                #     EC.presence_of_element_located((By.XPATH, '//ul[@class="pagination"]/li[last()]/a'))
                # )
                # print('----------')
                ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath('//ul[@class="pagination"]/li[last()]/a')).perform()
                self.driver.find_element_by_xpath('//ul[@class="pagination"]/li[last()]/a').click()  # 翻页

            html = self.driver.page_source
            self.parse_html(html, index)
            index += 1


    def request_detail(self, url, source_handle, index):
        """
        请求详细页
        :param url: 详细页url
        :param source_handle: 主页的handle句柄
        :return:
        """
        print('请求详细页')
        self.driver.execute_script(self.js.format(url))  # 开启新窗口
        # self.driver.get(url)
        handles = self.driver.window_handles
        detail_handle = None
        for handle in handles:
            if handle != source_handle:
                detail_handle = handle
        self.driver.switch_to.window(detail_handle)  # 切换到详细页窗口
        self.driver.find_element_by_xpath('//div[@class="tab-row"]//li[2]').click()
        html = self.driver.page_source
        self.parse_detail(html, index)
        self.driver.close()
        self.driver.switch_to.window(source_handle)  # 切换回原始窗口


    def parse_html(self, html, index):
        """
        解析
        :param html:
        :return:
        """
        print('解析')
        source_handle = self.driver.current_window_handle  # 当前句柄
        # print('source_handle', source_handle)
        html_xpath = etree.HTML(html)
        lis = html_xpath.xpath('//ul[@class="list-group search-hits"]/li')
        for li in lis:
            title = li.xpath('./a/h2/span/text()')[0].strip().strip('\n').strip()
            url = li.xpath('./a/@href')[0]
            temp_dict = {
                'title': title,
                'url': self.join_url + url
            }
            print(temp_dict)
            try:
                self.request_detail(temp_dict['url'], source_handle, index)
            except Exception as e:
                print('e= ', e)


    def parse_detail(self, html, index):
        """
        解析 Overview 这页
        :param html:
        :return:
        """
        html_xpath = etree.HTML(html)
        rows = html_xpath.xpath('//div[@class="tab-panel"]//div[@class="row"]')
        temp_dict = {}
        for row in rows:
            key = row.xpath('./div[1]/label/text()')[0].strip()
            value_xpath = row.xpath('./div[2]')[0]
            value_string = etree.tostring(value_xpath, encoding='utf-8').decode('utf-8')
            value_list = re.findall('>(.*?)<', value_string)
            value_list = [i for i in value_list if i != '']
            value = '\n'.join(value_list).strip()
            temp_dict[key] = value.strip('\n')
        temp_dict['page'] = index
        temp_string = json.dumps(temp_dict, ensure_ascii=False)
        with open('data.json', 'a+', encoding='utf-8') as f:
            f.write('{}\n'.format(temp_string))


def main():
    dans = Dans()
    dans.request()


if __name__ == '__main__':
    main()
