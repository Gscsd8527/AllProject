import requests
from lxml import etree
import re
import json
import tabula

data_list = []

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

def parseHtml(html):
    html_data = etree.HTML(html)
    trs = html_data.xpath('//div[@id="lista0"]//tr[@class="tr_normal"]')
    for tr in trs:
        tds = tr.xpath('./td')
        title_url = tds[1].xpath('./a/@onclick')[0]
        url_compile = re.compile("openW\('(.*?)'")
        new_url = re.findall(url_compile, title_url)[0].strip('..')
        # req_url = 'http://service.most.gov.cn/2015tztg_all/20190726/2995.html'
        req_url = 'http://service.most.gov.cn' + new_url
        title_name = tds[1].xpath('./a/@title')[0]
        department = tds[2].xpath('./@title')[0]
        date = tds[3].xpath('./text()')[0]
        print('req_url= ', req_url)
        print('title_name= ', title_name)
        print('department= ', department)
        print('date= ', date)
        data_dict = {
            'url': req_url,
            'title': title_name,
            'department': department,
            'date': date
        }
        data_list.append(data_dict)

def getUrls():
    for i in range(1, 72):
        if i == 1:
            url = 'http://service.most.gov.cn/2015tztg_all/'
            headers = HEADERS
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                html = response.text
                parseHtml(html)
            else:
                print('错误响应码为： ', response.status_code)
        else:
            url = 'http://service.most.gov.cn/2015tztg_all/index_{}.html'.format(i)
            headers = HEADERS
            headers['Upgrade-Insecure-Requests'] = '1'
            if i == 2:
                headers['Referer'] = 'http://service.most.gov.cn/2015tztg_all/'
            else:
                headers['Referer'] = 'http://service.most.gov.cn/2015tztg_all/index_{}.html'.format(i-1)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                response.encoding = 'utf-8'
                html = response.text
                parseHtml(html)
            else:
                print('错误响应码为： ', response.status_code)

def saveJson():
    for dt in data_list:
        str_dt = json.dumps(dt, ensure_ascii=False)
        with open('data.json', 'a+', encoding='utf-8') as f:
            f.write(str_dt)
            f.write('\n')

# 得到我们得到的url中的关于专家的pdf
def getSpecialist():
    f = open('data.json', 'r', encoding='utf-8')
    data = f.read()
    data_list = data.split('\n')
    for dt in data_list:
        if len(dt):
            dt_json = json.loads(dt)
            title = dt_json['title']
            if '申报指南' in title:
                url = dt_json['url']
                print('url=', url)
                response = requests.get(url)
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    html = response.text
                    pdf_list = re.findall('、.*?<a href="(.*?)".*?指南编制专家名单', html)
                    for pdf in pdf_list:
                        if len(pdf):
                            # paf_url = 'http://service.most.gov.cn/u/cms/static/201907/231702594876.pdf'
                            pdf_url = 'http://service.most.gov.cn' + pdf
                            new_dict = dt_json
                            new_dict['pdf_url'] = pdf_url
                            str_pdf = json.dumps(new_dict, ensure_ascii=False)
                            with open('pdf.json', 'a+', encoding='utf-8') as f:
                                f.write(str_pdf)
                                f.write('\n')

                else:
                    print('错误响应码为： ', response.status_code)


def parsePdf():
    f = open('pdf.json', 'r', encoding='utf-8')
    data = f.read()
    pdf_list = data.split('\n')
    aa = 25
    for pdf in pdf_list:
        print('index= ', aa)
        # if len(pdf):
        pdf_json = json.loads(pdf)
        print(pdf_json['pdf_url'])
        projectName = pdf_json['title']
        releaseDepartment = pdf_json['department']
        date = pdf_json['date']
        pdf_file = pdf_json['pdf_url']
        # print('pdf_file', pdf_file)
        df = tabula.read_pdf(pdf_file, encoding='utf-8', pages='all')
        print(df)
        for index in df.index[:]:
            data = df.loc[index]
            name = data.values[1]
            organization = data.values[3]
            title = data.values[5]
            data_json = {
                'year': date,
                'projectName': projectName,
                'name': name,
                'organization': organization,
                'title': title,
                'releaseDepartment': releaseDepartment
            }
            str_dt = json.dumps(data_json, ensure_ascii=False)
            with open('new_data.json', 'a+', encoding='utf-8') as f:
                f.write(str_dt)
                f.write('\n')
        aa += 1






def main():
    # getUrls()
    # saveJson()

    # getSpecialist()

    parsePdf()

if __name__ == '__main__':
    main()

