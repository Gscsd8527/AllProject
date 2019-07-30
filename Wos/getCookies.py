import requests


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

# 解析传过来的cookie
def parseSetCookie(set_cookie, need_list):
    set_cookie_list = set_cookie.replace(',', ';').split(';')
    cookie = {}
    for k in set_cookie_list:
        for i in need_list:
            if i in k:
                k_v = k.split('=', 1)
                k = k_v[0].strip(' ')
                v = k_v[1].strip(' ')
                cookie[k] = v
    return cookie

# 排序
def order(cookies, referer, sid):
    print('================排序========================')
    url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&qid=1&SID={}&&page=1&action=sort&sortBy=TC.D;PY.D;AU.A;SO.A;VL.D;PG.A&showFirstPage=1&isCRHidden=false'.format(sid)
    headers = HEADERS.copy()
    headers['Referer'] = referer
    response = requests.get(url, cookies=cookies, headers=headers)
    set_cookie = response.headers['Set-Cookie']
    need_list = ['JSESSIONID', 'dotmatics.elementalKey', '_abck', 'bm_sv']
    cookies = parseSetCookie(set_cookie, need_list)
    return cookies, url

# 第七次请求，拿到数据页，如果翻页的话需要其cookie
def searchDo(base_url, cookies, referer):
    print('==============searchDo===============')
    cookies.pop('_abck')
    url = 'http://apps.webofknowledge.com/' + base_url
    headers = HEADERS.copy()
    headers['Referer'] = referer
    response = requests.get(url, headers=headers, cookies=cookies)
    # print(response.text)
    set_cookie = response.headers['Set-Cookie']
    need_list = ['JSESSIONID', 'dotmatics.elementalKey', '_abck', 'bm_sv']
    cookies = parseSetCookie(set_cookie, need_list)
    return cookies, url


# 第六次请求，拿到得到数据的location，以及更改cookie
def ua_GeneralSearch_do(referer, cookie, sid):
    print('============ua_GeneralSearch_do==============')
    cookie.pop('_abck')
    url = 'http://apps.webofknowledge.com/UA_GeneralSearch.do'
    headers = HEADERS.copy()
    update_header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': referer
    }
    start_year = '2017'
    end_year = '2017'
    key_word = 'computer'
    data = '''fieldCount=1&action=search&product=UA&search_mode=GeneralSearch&SID={}&max_field_count=25&max_field_notice=%E6%B3%A8%E6%84%8F%3A+%E6%97%A0%E6%B3%95%E6%B7%BB%E5%8A%A0%E5%8F%A6%E4%B8%80%E5%AD%97%E6%AE%B5%E3%80%82&input_invalid_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E8%AF%B7%E8%BE%93%E5%85%A5%E6%A3%80%E7%B4%A2%E8%AF%8D%E3%80%82&exp_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E4%B8%93%E5%88%A9%E6%A3%80%E7%B4%A2%E8%AF%8D%E5%8F%AF%E4%BB%A5%E5%9C%A8%E5%A4%9A%E4%B8%AA%E5%AE%B6%E6%97%8F%E4%B8%AD%E6%89%BE%E5%88%B0+%28&input_invalid_notice_limits=+%3Cbr%2F%3E%E6%B3%A8%E6%84%8F%3A+%E6%BB%9A%E5%8A%A8%E6%A1%86%E4%B8%AD%E6%98%BE%E7%A4%BA%E7%9A%84%E5%AD%97%E6%AE%B5%E5%BF%85%E9%A1%BB%E8%87%B3%E5%B0%91%E4%B8%8E%E4%B8%80%E4%B8%AA%E5%85%B6%E4%BB%96%E6%A3%80%E7%B4%A2%E5%AD%97%E6%AE%B5%E7%9B%B8%E7%BB%84%E9%85%8D%E3%80%82&sa_params=UA||{}|http://apps.webofknowledge.com|'&formUpdated=true&value%28input1%29=information&value%28select1%29=TS&value%28hidInput1%29=&limitStatus=collapsed&ss_lemmatization=On&ss_spellchecking=Suggest&SinceLastVisit_UTC=&SinceLastVisit_DATE=&period=Range+Selection&range=ALL&startYear=1900&endYear=2019&editions=WOS.CCR&editions=WOS.SCI&editions=WOS.ISTP&editions=WOS.IC&collections=WOS&editions=CSCD.CSCD&collections=CSCD&editions=CCC.CCCB&editions=CCC.CCCA&editions=CCC.CCCY&editions=CCC.CCCT&editions=CCC.CCCBC&editions=CCC.CCCS&editions=CCC.CCCEC&editions=CCC.CCCP&editions=CCC.CCCC&collections=CCC&editions=DIIDW.EDerwent&editions=DIIDW.MDerwent&editions=DIIDW.CDerwent&collections=DIIDW&editions=KJD.KJD&collections=KJD&editions=MEDLINE.MEDLINE&collections=MEDLINE&editions=RSCI.RSCI&collections=RSCI&editions=SCIELO.SCIELO&collections=SCIELO&update_back2search_link_param=yes&ssStatus=display%3Anone&ss_showsuggestions=ON&ss_query_language=auto&ss_numDefaultGeneralSearchFields=1&rs_sort_by=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A'''.format(
        sid, sid)
    data = '''fieldCount=1&action=search&product=UA&search_mode=GeneralSearch&SID={}&max_field_count=25&max_field_notice=%E6%B3%A8%E6%84%8F%3A+%E6%97%A0%E6%B3%95%E6%B7%BB%E5%8A%A0%E5%8F%A6%E4%B8%80%E5%AD%97%E6%AE%B5%E3%80%82&input_invalid_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E8%AF%B7%E8%BE%93%E5%85%A5%E6%A3%80%E7%B4%A2%E8%AF%8D%E3%80%82&exp_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E4%B8%93%E5%88%A9%E6%A3%80%E7%B4%A2%E8%AF%8D%E5%8F%AF%E4%BB%A5%E5%9C%A8%E5%A4%9A%E4%B8%AA%E5%AE%B6%E6%97%8F%E4%B8%AD%E6%89%BE%E5%88%B0+%28&input_invalid_notice_limits=+%3Cbr%2F%3E%E6%B3%A8%E6%84%8F%3A+%E6%BB%9A%E5%8A%A8%E6%A1%86%E4%B8%AD%E6%98%BE%E7%A4%BA%E7%9A%84%E5%AD%97%E6%AE%B5%E5%BF%85%E9%A1%BB%E8%87%B3%E5%B0%91%E4%B8%8E%E4%B8%80%E4%B8%AA%E5%85%B6%E4%BB%96%E6%A3%80%E7%B4%A2%E5%AD%97%E6%AE%B5%E7%9B%B8%E7%BB%84%E9%85%8D%E3%80%82&sa_params=UA||{}|http://apps.webofknowledge.com|'&formUpdated=true&value%28input1%29={}&value%28select1%29=TS&value%28hidInput1%29=&limitStatus=collapsed&ss_lemmatization=On&ss_spellchecking=Suggest&SinceLastVisit_UTC=&SinceLastVisit_DATE=&range=CUSTOM&period=Year+Range&startYear={}&endYear={}&editions=WOS.CCR&editions=WOS.SCI&editions=WOS.ESCI&editions=WOS.ISTP&editions=WOS.IC&collections=WOS&editions=CSCD.CSCD&collections=CSCD&editions=CCC.CCCB&editions=CCC.CCCA&editions=CCC.CCCY&editions=CCC.CCCT&editions=CCC.CCCBC&editions=CCC.CCCS&editions=CCC.CCCEC&editions=CCC.CCCP&editions=CCC.CCCC&collections=CCC&editions=DIIDW.EDerwent&editions=DIIDW.MDerwent&editions=DIIDW.CDerwent&collections=DIIDW&editions=KJD.KJD&collections=KJD&editions=MEDLINE.MEDLINE&collections=MEDLINE&editions=RSCI.RSCI&collections=RSCI&editions=SCIELO.SCIELO&collections=SCIELO&update_back2search_link_param=yes&ssStatus=display%3Anone&ss_showsuggestions=ON&ss_query_language=auto&ss_numDefaultGeneralSearchFields=1&rs_sort_by=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A'''.format(
        sid, sid, key_word, start_year, end_year)
    headers.update(update_header)
    response = requests.post(url, headers=headers, cookies=cookie, data=data, allow_redirects=False)
    location = response.headers['Location']
    set_cookie = response.headers['Set-Cookie']
    need_list = ['JSESSIONID', 'dotmatics.elementalKey', '_abck']
    cookies = parseSetCookie(set_cookie, need_list)
    return location, cookies, url


# 第五次请求，更改cookie，更改了'JSESSIONID', 'dotmatics.elementalKey', 'bm_sv'
def ua_GeneralSearch_input(base_url, cookies):
    print('=============ua_GeneralSearch_input==================')
    url = 'http://apps.webofknowledge.com' + base_url
    heasers = HEADERS.copy()
    response = requests.get(url, headers=heasers, cookies=cookies)
    need_list = ['JSESSIONID', 'dotmatics.elementalKey', 'bm_sv']
    set_cookie = response.headers['Set-Cookie']
    cookies = parseSetCookie(set_cookie, need_list)
    return url, cookies


# 第四次请求， 获取下一次的location， 更改了'JSESSIONID', 'dotmatics.elementalKey'，加了'bm_sv'
def home(base_url, cookies):
    print('=============home==============')
    url = 'http://apps.webofknowledge.com/' + base_url
    headers = HEADERS.copy()
    response = requests.get(url, headers=headers, cookies=cookies, allow_redirects=False)
    location = response.headers['Location']
    need_list = ['JSESSIONID', 'dotmatics.elementalKey', 'bm_sv']
    set_cookie = response.headers['Set-Cookie']
    cookies = parseSetCookie(set_cookie, need_list)
    return location, cookies


# 第三次请求，更改JSESSIONID， dotmatics.elementalKey，增加ak_bmsc
def appWebofknowledge(url, cookies):
    print('==============appWebofknowledge==============')
    headers = HEADERS.copy()
    response = requests.get(url, headers=headers, cookies=cookies, allow_redirects=False)
    location = response.headers['Location']
    need_list = ['JSESSIONID', 'dotmatics.elementalKey', 'ak_bmsc']
    set_cookie = response.headers['Set-Cookie']
    cookies = parseSetCookie(set_cookie, need_list)
    return location, cookies


# 第二次请求，获取setcookie中的SID、CUSTOMER、E_GROUP_NAME_WOK5_SID
def webofknowledge(cookie):
    print('==============webofknowledge=================')
    url = 'http://www.webofknowledge.com/?'
    headers = HEADERS.copy()
    response = requests.get(url, cookies=cookie, headers=headers, allow_redirects=False)
    location = response.headers['Location']
    need_list = ['SID', 'CUSTOMER', 'E_GROUP_NAME']
    set_cookie = response.headers['Set-Cookie']
    cookies = parseSetCookie(set_cookie, need_list)
    cookies.pop('WOK5_SID')  # 多余的值
    return location, cookies


# 第一次加载页面,获取重定向的链接和set-cookie JSESSIONID, dotmatics.elementalKey, bm_sz, _abck
def generalSearch_input():
    print('============generalSearch_input==============')
    url = 'http://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=8ESRKD1H5nmMIIIZXdq&preferencesSaved='
    url = 'http://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=6BxcKabM9aKiB6BZ8x8&preferencesSaved='
    headers = HEADERS.copy()
    response = requests.get(url, headers=headers, allow_redirects=False)
    need_list = ['JSESSIONID', 'dotmatics.elementalKey', 'bm_sz', '_abck']
    set_cookie = response.headers['Set-Cookie']
    cookie = parseSetCookie(set_cookie, need_list)
    return cookie

# 初始调用函数
def getCookies():
    cookie = generalSearch_input()
    location, change_cookie1 = webofknowledge(cookie.copy())
    cookie.update(change_cookie1)
    home_location, app_cookie = appWebofknowledge(location, cookie.copy())
    sid = home_location.rsplit('=', 1)[-1]
    cookie.update(app_cookie)
    ua_location, ua_cookie = home(home_location, cookie.copy())
    cookie.update(ua_cookie)
    referer, input_cookie = ua_GeneralSearch_input(ua_location, cookie.copy())
    cookie.update(input_cookie)
    search_url, search_cookie, url = ua_GeneralSearch_do(referer, cookie.copy(), sid)
    cookie.update(search_cookie)
    summary_cookie, url = searchDo(search_url, cookie.copy(), url)
    cookie.update(summary_cookie)
    order_cookie, url = order(cookie, url, sid)
    cookie.update(order_cookie)
    # print('cookie= ', cookie)
    # print('url= ', url)
    # print('sid= ', sid)
    return sid, cookie, url

# getCookies()
