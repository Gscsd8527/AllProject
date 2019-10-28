from selenium import webdriver
import time
from lxml.html import etree
import copy
import json

def getAuthors():
    j1 = set()
    f = open('Author.json', 'r', encoding='utf-8')
    data = f.read()
    data_list = data.split('\n')
    for dt in data_list:
        j1.add(dt)
    f.close()
    print('j1= ', len(j1))
    j2 = set()
    f1 = open('yzq.json', 'r', encoding='utf-8')
    data1 = f1.read()
    data_list1 = data1.split('\n')
    for dt in data_list1:
        j2.add(dt)
    print('j2= ', len(j2))
    countSet = j1 - j2
    print('countset= ', len(countSet))
    AuthorsData = []
    for dt in countSet:
        dt_json = json.loads(dt)
        if int(dt_json["成果"]) > 0:
            AuthorsData.append(dt_json)
    # dt = {'img': 'https://www.scholarmate.com/avatars/99/92/62/37572.jpg', 'name': '吴伟',
    #       'url': 'https://www.scholarmate.com/P/aeiUZr', 'org': '复旦大学, 教授', '项目': 20, '成果': 234, 'H指数': '24'}
    print('AuthorData= ', len(AuthorsData))
    return AuthorsData

def parseHtml(html, i):
    temp_list = []
    html_data = etree.HTML(html)
    project_html = html_data.xpath('//div[@class="pub-idx__main"]')
    for p in project_html:
        # pro_name = p.xpath('./div[@class="pub-idx__main_title"]/a/@title')[0]
        pro_name = p.xpath('.//a/@title')[0].strip().replace(r'\xa0', '')
        # pro_url = p.xpath('./div[@class="pub-idx__main_title"]/a/@href')[0]
        pro_url = p.xpath('.//a/@href')[0]
        pro_author = p.xpath('./div[2]/@title')[0].strip().replace('\xa0', '')
        # pro_author = p.xpath('.//div[@class="pub-idx__main_author"]/@title')
        pro_inst = p.xpath('./div[3]/@title')[0]
        temp_dict = {
            'num': i,
            'pro_name': pro_name,
            'pro_url': pro_url,
            'pro_author': pro_author,
            'pro_inst': pro_inst
        }
        temp_list.append(copy.deepcopy(temp_dict))
    return temp_list



def parseData(author_data):
    try:
        url = author_data['url']
        ach_num = int(author_data['成果'])
        pages = ach_num // 10
        pages_ys = ach_num % 10
        if pages_ys > 0:
            pages += 1
        driver = webdriver.Chrome()
        driver.get(url)
        psn_data = []
        for i in range(1, pages+1):
            if i == 1:
                # 防止抓取到半路的时候页面没有响应，这部分数据就直接扔掉
                try:
                    driver.find_element_by_xpath('//*[@id="pubTab"]').click()
                    time.sleep(2)
                    html = driver.page_source
                    temp_dict = parseHtml(html, i)
                    psn_data.append(copy.deepcopy(temp_dict))
                except:
                    pass
            else:
                # driver.find_element_by_xpath('//*[@id="pubTab"]').click()
                # 将页面拉到底部
                try:
                    js = "var q=document.documentElement.scrollTop=100000"
                    driver.execute_script(js)
                    time.sleep(3)
                    driver.find_element_by_xpath('//div[@class="pagination__pages_next"]').click()
                    time.sleep(3)
                    html = driver.page_source
                    temp_dict = parseHtml(html, i)
                    psn_data.append(copy.deepcopy(temp_dict))
                except:
                    pass
        driver.close()
        psn_data = {
            'init_data': author_data,
            'psn_data': psn_data
        }
        print(psn_data)
        psn_data_string = json.dumps(psn_data, ensure_ascii=False)
        with open('data.json', 'a+', encoding='utf-8') as f:
            f.write('{}\n'.format(psn_data_string))
        # 断点续爬
        author_data_string = json.dumps(author_data, ensure_ascii=False)
        with open('yzq.json', 'a+', encoding='utf-8') as f:
            f.write('{}\n'.format(author_data_string))
    except:
        pass





def main():
    AuthorsData = getAuthors()
    for authors in AuthorsData:
        print('author= ', authors)
        parseData(authors)


if __name__ == '__main__':
    main()