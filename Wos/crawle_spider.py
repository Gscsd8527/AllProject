import requests
from lxml import etree
import re
from lxml.html import tostring
import html
import uuid
import datetime
import pymongo

myclient = pymongo.MongoClient('mongodb://10.0.82.131:27017/')
mydb = myclient['Wos_Computer']  # 数据库
mydata = mydb['data2017']  # 表


from getCookies import getCookies, parseSetCookie, HEADERS
# from spider.getCookies import getCookies, parseSetCookie, HEADERS

COOKIES = {}
INDEX = 1
K = False

def parseHtml(url, cookie, name_string):
    print('===========parseHtml================')
    headers = HEADERS
    qid = re.findall('qid=(.*?)&', url)[0]
    sid = re.findall('SID=(.*?)&', url)[0]
    page = re.findall('page=(.*?)&', url)[0]
    headers['Referer'] = 'http://apps.webofknowledge.com/summary.do?product=UA&colName=&qid={}&SID={}&search_mode=GeneralSearch&formValue(summary_mode)=GeneralSearch&update_back2search_link_param=yes&page={}'.format(qid, sid, page)
    response = requests.get(url, headers=headers, cookies=cookie)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        set_cookie = response.headers['Set-Cookie']
        need_list = ['JSESSIONID', 'dotmatics.elementalKey', '_abck', 'bm_sv']
        cookies = parseSetCookie(set_cookie, need_list)
        # 翻页时需要用到这个cookie
        new_cookie = cookie.update(cookies)
        html_text = response.text
        html_data = etree.HTML(html_text)
        # HTML主体
        content = html_data.xpath('//div[@class="l-content"]//div[@class="block-record-info"]')
        # 论文名称 name
        paper_Name = name_string
        print('name= ', paper_Name)
        # 作者 author
        author = ''
        try:
            author_jc_list = []
            author_qc_list = []
            author_a = content[0].xpath('./p/a')
            for a in author_a:
                jc = a.xpath('./text()')[0].strip(' ')
                author_jc_list.append(jc)
            author_qc = content[0].xpath('./p/text()')
            for i in author_qc:
                if '(' in i:
                    qc = i.strip(' ')
                    author_qc_list.append(qc)
            for i in range(len(author_jc_list)-len(author_qc_list)):
                author_qc_list.append(' ')
            author_zip = zip(author_jc_list, author_qc_list)
            author_list = []
            for i in author_zip:
                auth = i[0] + i[1]
                author_list.append(auth)
            author = author_list
        except Exception as e:
            print(e)

        # 信息资源 info_source
        info_source = {}
        try:
            info = html_data.xpath('//div[@class="l-content"]//div[@class="block-record-info block-record-info-source"]')[0]
            sourceTitle = ''
            try:
                try:
                    sourceTitle = html_data.xpath('//*[@class="sourceTitle"]/value/text()')
                    sourceTitle_list = [i.strip(' ') for i in sourceTitle if i != '']
                    sourceTitle = ''.join(sourceTitle_list)
                except:
                    sourceTitle = html_data.xpath('//*[@class="sourceTitle"]/a/text()')
                    sourceTitle_list = [i.strip(' ') for i in sourceTitle if i != '']
                    sourceTitle = ''.join(sourceTitle_list)
            except Exception as e:
                print('sourceTitle error', e)
            info_source['sourceTitle'] = sourceTitle
            try:
                sourceValue = info.xpath('./div[@class="block-record-info-source-values"]/p')
                for i in sourceValue:
                    name = i.xpath('./span/text()')[0].strip(' ').strip(':')
                    value = i.xpath('./value/text()')[0].strip(' ')
                    info_source[name] = value
            except:
                pass
            try:
                fileds = info.xpath('./p[@class="FR_field"]')
                for filed in fileds:
                    name = filed.xpath('./span[@class="FR_label"]/text()')[0].strip(' ').strip(':')
                    try:
                        value = filed.xpath('./value/text()')[0].strip(' ')
                    except Exception as e:
                        value = filed.xpath('./text()')
                        value_list = [i for i in value if i != '\n']
                        value = ''.join(value_list)
                    info_source[name] = value
            except:
                pass
            try:
                data = content[1:]
                for dt in data:
                    title = dt.xpath('./div[@class="title3"]/text()')[0]
                    dt_string = tostring(dt).decode()
                    value_re = re.findall('>(.*?)<', dt_string)
                    value_list1 = [i.strip('\n').strip(' ') for i in value_re if i != '']
                    value_list2 = ' '.join(value_list1).strip('\n').strip(' ')
                    value_string = html.unescape(value_list2)
                    value = ''
                    if '摘要' in title:
                        value = value_string.strip('摘要').strip(' ').strip('\n')
                    elif '会议名称' in title:
                        try:
                            conference = {}
                            value_list = re.findall('(.*?):(.*?)会议', value_string)
                            value_string_end = value_string.rsplit('会议', 1)[-1].split(':')
                            for i in value_list:
                                name = i[0].strip(' ')
                                name_value = i[1].strip(' ')
                                conference[name] = name_value
                            name = '会议' + value_string_end[0].strip(' ')
                            name_value = value_string_end[1].strip(' ')
                            conference[name] = name_value
                            value = conference
                        except:
                            pass

                    elif '关键词' in title:
                        try:
                            value = {}
                            value_str = value_string.strip('关键词').strip(' ')
                            value_tuple = value_str.partition('KeyWords Plus:')
                            value_tuple1 = value_tuple[0].split(':')
                            value[value_tuple1[0]] = value_tuple1[1]
                            value[value_tuple[1].strip(':')] = value_tuple[2].strip(' ')
                        except:
                            pass
                    elif '作者信息' in title:
                        try:
                            value = {}
                            clean_data = {}
                            temp_dict = {}
                            temp_value = []
                            temp_list = []
                            value['source_data'] = value_string
                            try:
                                ps = dt.xpath('./p')
                                tables = dt.xpath('./table')
                                ps_tables = zip(ps, tables)
                                for p_t in ps_tables:
                                    p_list = p_t[0].xpath('./text()')
                                    p_str = ''.join(p_list)
                                    p_new_str = p_str.strip(' ')
                                    if '通讯作者' in p_new_str:
                                        try:
                                            table_bq = p_t[1].xpath('.//*[@class="fr_address_row2"]/text()')
                                            table_bq_strip = [i.strip(' ') for i in table_bq if i != '']
                                            temp_value.extend(table_bq_strip)
                                            p_new_str = p_new_str.strip(' ').strip('\n')
                                            if p_new_str in temp_dict.keys():
                                                temp_value.extend(table_bq_strip)
                                                temp_dict[p_new_str] = temp_value
                                            else:
                                                temp_dict[p_new_str] = table_bq_strip
                                        except:
                                            pass
                                    else:
                                        try:
                                            table_bq = p_t[1].xpath('.//*[@class="fr_address_row2"]/a/text()')
                                            table_bq_strip = [i.strip(' ') for i in table_bq if i != '']
                                            temp_list = table_bq_strip
                                        except:
                                            pass
                                clean_data['地址'] = temp_list
                                clean_data['通讯作者地址'] = temp_dict
                                email = ''
                                try:
                                    email = ps[-1].xpath('.//a/text()')
                                except:
                                    pass
                                clean_data['邮箱'] = email
                            except Exception as e:
                                print('e=', e)
                            value['clean_data'] = clean_data
                        except:
                            pass
                    elif '基金资助致谢' in title:
                        value = re.findall('授权号(.*?)查看基金资助信息 ', value_string)[0].strip(' ')
                    elif '出版商' in title:
                        value = value_string.strip('出版商').strip(' ')
                    elif '/' in title:
                        try:
                            value = {}
                            value_tuple = value_string.split(':')
                            value['研究方向'] = value_tuple[1].strip(' ').strip('类别').strip(' ').strip('Web of Science').strip(' ')
                            value['类别'] = value_tuple[2].strip(' ')
                        except:
                            pass
                    elif '文献信息' in title:
                        try:
                            value = {}
                            value_string = value_string.strip('文献信息').strip(' ')
                            value_list = [i.strip(':').strip(' ') for i in value_string.split(' ')]
                            for i in range(len(value_list) // 2):
                                j = i * 2
                                value[value_list[j]] = value_list[j + 1]
                        except:
                            pass
                    elif '其他信息' in title:
                        value = value_string.strip('文献信息').strip(' ')
                    else:
                        value = value_string
                    info_source[title] = value


            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        # works_cited 引用文献
        works_cited = {}
        try:
            # 右侧介绍
            sidebar = html_data.xpath('//div[@id="sidebar-container"]')[0]
            columns = sidebar.xpath('.//div[@class="flex-column"]')
            if len(columns) == 2:
                column1 = columns[0]
                value = column1.xpath('.//*[@class="large-number"]/text()')
                works_cited['被引频次'] = value[0].strip(' ')
                works_cited['引用的参考文献'] = value[1].strip(' ')
                column2 = columns[1]
                value2 = column2.xpath('.//*[@class="large-number"]/text()')
                name = column2.xpath('.//div/span[@class="box-label"]/text()')
                if '引用的参考文献' not in name:
                    works_cited[name[0]] = value2[0].strip(' ')
                    works_cited[name[1]] = value2[1].strip(' ')
        except Exception as e:
            print(e)

        # 引用参考文献
        references_datasets = {}
        try:
            references_data = html_data.xpath('//div[@class="cited-ref-section"]')[0]
            separator = references_data.xpath('./div[@class="cited-ref-separator"]/h2/text()')[0]
            num = 30
            if ':' in separator:
                try:
                    num = int(separator.split(':')[1].strip(' '))
                except:
                    num = 30
            page_num = num // 30
            page_num_yushu = num / 30
            if page_num_yushu > page_num:
                nums = page_num + 1
            else:
                nums = page_num
            for pages in range(1, nums+1):
                headers = HEADERS.copy()
                headers['Referer'] = url
                references_url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=CitedRefList&parentQid=1&parentDoc=2&qid=3&SID={}&colName=WOS&page={}'.format(sid, pages)
                references_url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=CitedRefList&parentQid=1&parentDoc=1&qid=2&SID={}&colName=WOS&page={}'.format(sid, pages)
                response = requests.get(url=references_url, headers=headers, cookies=new_cookie)
                print('共有 {}  页，这是第   {}   页'.format(nums, pages))
                if response.status_code == 200:
                    html_context = response.text
                    references = {}
                    html_context = etree.HTML(html_context)
                    references_data = html_context.xpath('//div[@class="search-results-item"]')
                    for dt in references_data:
                        id_list = dt.xpath('./div[@class="search-results-number"]/div/text()')
                        id_str = ''.join(id_list).strip('\n').strip(' ').strip('.')
                        title_name = ''
                        try:
                            # name_list = dt.xpath('./a[@class="smallV110 snowplow-full-record"]//value/text()')
                            name_list = dt.xpath('.//span[@class="reference-title"]/value/text()')
                            name_str = ''.join(name_list)
                            title_name = name_str.strip('\n').strip(' ')
                            if title_name == '':
                                title_name = '标题不可用'
                        except Exception as e:
                            print('name错误：', e)
                        divs = dt.xpath('./*[@class="summary_data"]/div')
                        author_string = '未截取'
                        conference_info = {}
                        paper_info = {}
                        for div in divs:
                            div_str = tostring(div).decode()
                            div_str_un = html.unescape(div_str)
                            div_string = re.findall('>(.*?)<', div_str_un)
                            div_string = ''.join(div_string)
                            if '作者' in div_string:
                                try:
                                    author_string = div_string.strip('作者: ').strip(' ').strip('等.')
                                    if '标题' in author_string:
                                        author_list = re.findall(':.*?(.*?)\.', author_string)
                                        author_str = ''.join(author_list)
                                        if ':' in author_str:
                                            author_string = author_str.split(':')[-1].strip(' ').strip('等.')
                                    elif '作者' in author_string:
                                        author_string = re.findall('作者:(.*)\.', author_string)
                                        author_string = ''.join(author_string)
                                        zw_len = re.findall('([\u4e00-\u9fa5])', author_string)
                                        if len(zw_len):
                                            paper_data1 = re.sub('\s{2,5}', '=', div_string)
                                            paper_data2 = paper_data1.split('=')
                                            paper_data3 = paper_data2[0]
                                            if ':' in paper_data3:
                                                author_string = paper_data3.split(':')[-1].strip(' ')
                                            else:
                                                author_string = paper_data3
                                except Exception as e:
                                    print('zuoze： ', e)
                            if '会议' in div_string:
                                try:
                                    div_list = div_string.split('会议')
                                    conference_name = [i for i in div_list if ':' not in i][0].strip(' ')
                                    temp_dict = {i.split(':')[0].strip(' '): i.split(':')[1].strip(' ') for i in div_list if ':' in i}
                                    conference_info['conference_name'] = conference_name
                                    conference_info.update(temp_dict)
                                except:
                                    pass
                            if ('丛书' in div_string) or ('卷' in div_string) or ('页' in div_string) or ('出版年' in div_string):
                                try:
                                    paper_data1 = re.sub('\s{2,5}', '=', div_string)
                                    paper_data2 = paper_data1.split('=')
                                    if ':' not in paper_data2[0]:
                                        paper_name = paper_data2[0].strip(' ')
                                        paper_info['paper_name'] = paper_name
                                    if '作者' in paper_data2[0]:
                                        paper_name = paper_data2[0].rsplit('.', 1)[-1]
                                        paper_info['paper_name'] = paper_name
                                    if ':' not in paper_data2[-1]:
                                        paper_info['出版日期'] = paper_data2[-1].strip(' ')
                                    paper_dict = {i.split(':')[0].strip(' '): i.split(':')[1].strip(' ') for i in
                                                  paper_data2 if ':' in i}
                                    paper_info.update(paper_dict)
                                except:
                                    pass

                        # 清洗page_info, 主要是出版商、出版日期、脏数据
                        paper_info_copy = paper_info.copy()
                        for k, v in paper_info.items():
                            if '出版商' in k:
                                sz = re.findall('\d+', k)
                                if len(sz):
                                    paper_info_copy['出版日期'] = sz[0]
                                    paper_info_copy['出版商'] = v
                                    del paper_info_copy[k]
                            if len(k) > 25:
                                del paper_info_copy[k]

                        frequency = ''
                        try:
                            frequency = dt.xpath('.//div[@class="search-results-data-cite"]/a/text()')[0].strip(' ')
                        except:
                            pass
                        temp_references = {
                            'name': title_name,
                            'author': author_string,
                            'conference_info': conference_info,
                            'paper_info': paper_info_copy,
                            'frequency': frequency
                        }
                        references[id_str] = temp_references
                        # print('references= ', references)
                        references_datasets.update(references.copy())
                else:
                    print('翻页这里的错误响应码为： ', response.status_code)
        except Exception as e:
            pass
        uid = uuid.uuid1()
        suid = str(uid).replace('-', '')
        # 1. 成果唯一标识
        datasetId = suid
        spiderDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_json = {
            'datasetId': datasetId,
            'handle': '',
            'source': url,
            'name': paper_Name,
            'author': author,
            'info_source': info_source,
            'works_cited': works_cited,
            'references_json': references_datasets,
            'spiderDateTime': spiderDateTime,
        }
        print('data_json', data_json)
        try:
            mydata.insert_one(data_json)
        except Exception as e:
            # data_json = json.dumps(data_json, ensure_ascii=False)
            # # print('文本类型为： ', data_json)
            # with open('data.txt', 'a+', encoding='utf-8') as f:
            #     f.write(data_json)
            #     f.write('\n')
            print('插入数据库报错： ', e)
    else:
        print('错误的响应码为： ', response.status_code)


# 解析得到总数和每条记录的URL
def parseGetUrlAndNum(html, cookie):
    html_data = etree.HTML(html)
    data = html_data.xpath('//div[@class="search-results-item"]')
    for dt in data:
        url = dt.xpath('./div[@class="search-results-content"]/div[1]//a/@href')[0]
        new_url = 'http://apps.webofknowledge.com' + url
        print('new_url= ', new_url)

        name_list = dt.xpath('./div[@class="search-results-content"]/div[1]//a/value/text()')
        name_list = [i.strip(' ') for i in name_list if i != '']
        name_string = ''.join(name_list)
        name_string = name_string.strip(' ').replace('\n', '')
        print('name_string********* ', name_string)

        parseHtml(new_url, cookie, name_string)
        # urls.append(new_url)
        # name = dt.xpath('./div[@class="search-results-content"]/div[1]//a/value/text()')[0]
        # print(name)

# 计数原则更新cookie
def updateCookie(sid, headers, referer):
    print('=========updateCookie=========')
    url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&qid=1&SID={}&&page=1&action=changePageSize&pageSize=50'.format(sid)
    headers['Referer'] = referer
    response = requests.get(url, headers=headers, cookies=COOKIES)
    if response.status_code == 200:
        set_cookie = response.headers['Set-Cookie']
        need_list = ['JSESSIONID', 'dotmatics.elementalKey', '_abck', 'bm_sv']
        cookies = parseSetCookie(set_cookie, need_list)
        # print('更改过后的cookie', cookies)
        COOKIES.update(cookies)
    return COOKIES

# 选择一页50条记录
def summary(sid, cookie, referer):
    print('================summary=====================')
    COOKIES = cookie
    COOKIES.pop('_abck')
    for i in range(1, 2001):
        print('这是第   {}    页'.format(i))
        headers = HEADERS.copy()
        global INDEX
        if (i > 0) and (i < 2):
            global K
            K = True
        # global K
        # K = True
        # if i < 0 or i > 1:
        #     # global K
        #     K = True
            print('i的值在1和10之间')
        else:
            if K:
                if INDEX > 9:
                    print('********************* 重新获取cookie *********************')
                    sid, cookie, url = getCookies()
                    COOKIES = cookie
                    COOKIES.pop('_abck')
                    INDEX = 1
                    print('INDEX 的值为：', INDEX)
                    cookies = updateCookie(sid, cookie, referer)
                    COOKIES.update(cookies)

                url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&qid=1&SID={}&&page={}&action=changePageSize&pageSize=50'.format(sid, i)
                if i == 1:
                    headers['Referer'] = referer
                else:
                    headers['Referer'] = url
                response = requests.get(url, headers=headers, cookies=COOKIES)
                if response.status_code == 200:
                    set_cookie = response.headers['Set-Cookie']
                    need_list = ['JSESSIONID', 'dotmatics.elementalKey', '_abck', 'bm_sv']
                    cookies = parseSetCookie(set_cookie, need_list)
                    # print('更改过后的cookie', cookies)
                    COOKIES.update(cookies)
                    print('SID的值为： ', COOKIES['SID'])
                    # if i != 1:
                    html = response.text
                    parseGetUrlAndNum(html, cookie)
                    # else:
                    #     print('因为i的值为1，所以跳过')
                else:
                    print('错误的响应吗为：', response.status_code)
            INDEX += 1
def main():
    sid, cookie, url = getCookies()
    summary(sid, cookie, url)


if __name__ == '__main__':
    main()