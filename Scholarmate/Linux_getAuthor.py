import requests
from lxml import etree
import copy
import json
import datetime


class Authors(object):
    def __init__(self):
        # self.HEADERS = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        #     'x-requested-with': '1',
        # }
        self.COOKIES = {
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
        # 个人简历
        self.brief_url = 'https://www.scholarmate.com/psnweb/briefdesc/ajaxshow'
        # 关键词
        self.keywork_url = 'https://www.scholarmate.com/psnweb/keywords/ajaxshow'
        # 工作经历
        self.work_url = 'https://www.scholarmate.com/psnweb/workhistory/ajaxshow'
        # 教育经历
        self.edu_url = 'https://www.scholarmate.com/psnweb/eduhistory/ajaxshow'

    def Main(self, author):
        """
        主函数，通过这个函数得到作者的详细信息、项目、成果
        :param url:
        :return:
        """
        # pro_num = int(author['项目'])
        # ach_num = int(author['成果'])
        url = author['url']
        location = self.GetLocation(url)
        key = location.rsplit('=')[-1]
        # print('key=', key)
        text = self.GetAuthorData(location)
        author_data = self.ParseAuthorHtml(text)
        # print(author_data)
        brief_desc = self.Transition(self.Briefdesc(key))
        # print('brief_desc= ', brief_desc)
        keyword = self.Transition(self.Keyword(key))
        # print('keyword= ', keyword)
        work_history = self.Transition(self.Workhistory(key))
        # print('work_history= ', work_history)
        edu_inst = self.Transition(self.Eduhistory(key))
        # print('edu_inst= ', edu_inst)
        data_json = {}
        data_json.update(author_data)
        temp_data_dict = {
            'init_data': author,
            'location': location,
            'brief_desc': brief_desc,
            'keyword': keyword,
            'work_history': work_history,
            'edu_inst': edu_inst,
        }
        data_json.update(temp_data_dict)
        # print(data_json)
        # mycol1.insert_one(data_json)
        data_json_string = json.dumps(data_json, ensure_ascii=False)
        with open('data.json', 'a+', encoding='utf-8') as f:
            f.write('{}\n'.format(data_json_string))


    def GetLocation(self, url):
        """
        通过作者的原始URL，得到重定向的Location，从而得到作者的详细信息
        :param url:
        :return:
        """
        # headers = self.HEADERS.copy()
        cookies = self.COOKIES.copy()
        # response = requests.get(url, headers=headers, cookies=cookies, allow_redirects=False)
        response = requests.get(url, cookies=cookies, allow_redirects=False)
        location = response.headers['Location']
        return location

    def GetAuthorData(self, location):
        """
        通过location得到作者的详细数据
        :param location:
        :return:
        """
        # headers = self.HEADERS.copy()
        cookies = self.COOKIES.copy()
        # response = requests.get(url=location, headers=headers, cookies=cookies)
        response = requests.get(url=location, cookies=cookies)
        if response.status_code == 200:
            text = response.text
            return text

    def ParseAuthorHtml(self, text):
        if text is not None:
            html_data = etree.HTML(text)
            pro_head = html_data.xpath('//div[@class="pro-header headDiv"]//div[@class="pro-header__base-info"]')[0]
            author_img = pro_head.xpath('./div[@id="upload_img"]/img/@src')[0]
            au_sx_data_html = pro_head.xpath('./div[@class="pro-header__main"]')[0]
            author_name = au_sx_data_html.xpath('./div[@id="psn_name"]/span/@title')[0]
            author_inst = au_sx_data_html.xpath('./div[@id="psn_insAndDept"]/span/@title')[0]
            author_job_title = au_sx_data_html.xpath('./div[@id="psn_posAndTitolo"]/span/@title')[0]
            author_addr = ''
            try:
                author_addr = au_sx_data_html.xpath('./div[@id="psn_regionName"]/text()')[0]
            except:
                pass

            # author_id = html_data.xpath('//div[@class="pro-header headDiv"]/div[@class="new-scholarmate_ID-container"]//*[@class="new-scholarmate_ID-container_content-detaile"]/text()')[0]
            author_id = html_data.xpath(
                '//div[@class="pro-header headDiv"]//*[@class="new-scholarmate_ID-container_content-detaile"]/text()')[
                0]

            author_url = html_data.xpath('//*[@id="span_shorturl"]/text()')[0]

            pro_stats__list = html_data.xpath('//div[@class="pro-stats__list"]/div[@class="pro-stats__item"]')
            k_v = {}
            for p_s_l in pro_stats__list:
                a_k = p_s_l.xpath('./div[@class="pro-stats__item_title"]/text()')[0].strip()
                a_v = p_s_l.xpath('./div[@class="pro-stats__item_number"]/text()')[0].strip()
                k_v[a_k] = a_v
            author_data = {
                'name': author_name,
                'img': author_img,
                'inst': author_inst,
                'jobTitle': author_job_title,
                'address': author_addr,
                'ky_id': author_id,
                'url': author_url,
                'achievement': k_v
            }
            return author_data

    def Briefdesc(self, key):
        """
        个人简历
        :return:
        """
        # headers = copy.deepcopy(self.HEADERS)
        # headers['Referer'] = location
        cookie = self.COOKIES.copy()
        response = requests.post(self.brief_url, data={'des3PsnId': key}, cookies=cookie)
        if response.status_code == 200:
            try:
                text = response.text
                html_data = etree.HTML(text)
                brief_desc_list = html_data.xpath('//div[@class="global__padding_16"]/div[@class="global__para_body"]/text()')
                brief_desc = ''.join(brief_desc_list)
                # brief_desc = html_data.xpath('//input/@value')[0]
                return brief_desc
            except:
                pass

    def Keyword(self, key):
        """
        关键字
        :param key:
        :return:
        """
        cookie = self.COOKIES.copy()
        response = requests.post(self.keywork_url, data={'des3PsnId': key, 'editKeywords': key}, cookies=cookie)
        if response.status_code == 200:
            try:
                text = response.text
                html_data = etree.HTML(text)
                key_word_html = html_data.xpath('//div[@class="global__padding_16"]/div[@class="kw__box"]')
                key_word_list = []
                for k_w in key_word_html:
                    k_text = k_w.xpath('./div[@class="kw-stick"]/div/@title')[0]
                    key_word_list.append(k_text)
                return key_word_list
            except:
                pass

    def Workhistory(self, key):
        """
        工作经历
        :param key:
        :return:
        """
        cookie = self.COOKIES.copy()
        response = requests.post(self.work_url, data={'des3PsnId': key}, cookies=cookie)
        if response.status_code == 200:
            try:
                text = response.text
                html_data = etree.HTML(text)
                # work_his_html = html_data.xpath('//div[@class="exp-idx__main_box"]/div[@class="exp-idx__main"]')
                work_his_html = html_data.xpath('//div[@class="main-list__item"]')
                work_history = []
                for w_h in work_his_html:
                    img = ''
                    try:
                        img = w_h.xpath('.//div[@class="exp-idx__logo_img"]/img/@src')[0]
                    except:
                        pass
                    inst = ''
                    try:
                        inst = w_h.xpath('.//div[@class="exp-idx__main"]/div[@class="exp-idx__main_inst"]/text()')[0]
                    except:
                        pass
                    dept = ''
                    try:
                        dept = w_h.xpath('.//div[@class="exp-idx__main"]/div[@class="exp-idx__main_dept"]/text()')[0]
                    except:
                        pass
                    intro = ''
                    try:
                        intro = w_h.xpath('.//div[@class="exp-idx__main"]//div[@class="multipleline-ellipsis__content-box"]/text()')[0]
                    except:
                        pass
                    temp_dict = {
                        'institution': inst,
                        'img': img,
                        'dept': dept,
                        'intro': intro
                    }
                    work_history.append(copy.deepcopy(temp_dict))
                return work_history
            except:
                pass

    def Eduhistory(self, key):
        """
        教育经历
        :param key:
        :return:
        """
        cookie = self.COOKIES.copy()
        response = requests.post(self.edu_url, data={'des3PsnId': key}, cookies=cookie)
        if response.status_code == 200:
            try:
                text = response.text
                html_data = etree.HTML(text)
                edu_html = html_data.xpath('//div[@class="main-list__item"]')
                edu_inst = []
                for e_h in edu_html:
                    img = ''
                    try:
                        img = e_h.xpath('.//div[@class="exp-idx__logo_img"]/img/@src')[0]
                    except:
                        pass
                    inst = ''
                    try:
                        inst = e_h.xpath('.//div[@class="exp-idx__main"]/div[@class="exp-idx__main_inst"]/text()')[0]
                    except:
                        pass
                    dept = ''
                    try:
                        dept = e_h.xpath('.//div[@class="exp-idx__main"]/div[@class="exp-idx__main_dept"]/text()')[0]
                    except:
                        pass
                    intro = ''
                    try:
                        intro = e_h.xpath(
                            './/div[@class="exp-idx__main"]//div[@class="multipleline-ellipsis__content-box"]/text()')[0]
                    except:
                        pass
                    temp_dict = {
                        'institution': inst,
                        'img': img,
                        'dept': dept,
                        'intro': intro
                    }
                    edu_inst.append(copy.deepcopy(temp_dict))
                return edu_inst
            except:
                pass


    @staticmethod
    def Transition(value):
        """
        判断值是否是None,是的话将其转为空字符串
        :param value:
        :return:
        """
        if value is None:
            value = ''
        return value

    @staticmethod
    def getAuthorData():
        print('读取文件')
        AuthorsData = []
        f = open('Author.json', 'r', encoding='utf-8')
        data = f.read()
        data_list = data.split('\n')
        for dt in data_list[:-1]:
            dt_json = json.loads(dt)
            AuthorsData.append(dt_json)
        return AuthorsData

def main():
    Author = Authors()
    data = Author.getAuthorData()
    count = len(data)
    index = 326
    for dt in data[326:]:
        print(dt)
        print('{}  总共有  {}  个， 这是   {}   个'.format(datetime.datetime.now(), count, index))
        Author.Main(dt)
        index += 1

if __name__ == '__main__':
    main()