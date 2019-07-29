import requests
from lxml import etree
import datetime
import uuid
import re
from lxml import etree
import pymongo

# myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
# mydb = myclient['MyData']
# mycol = mydb['ccf_data']

myclient = pymongo.MongoClient('mongodb://10.0.82.131:27017/')
mydb = myclient['DataSet']
mycol = mydb['ccf_data']


# 解析得到所有字段的值
def parseFiled(datas):
    for data in datas:
        # 时间
        date = data[0]
        awards = data[1]
        print(date, awards)
        for dt in data[2]:
            name_url_img = dt[0]
            introduce = dt[1].replace('\n', '')
            name_org_img_lst = name_url_img.split('=')
            name = name_org_img_lst[0]
            organiza = name_org_img_lst[1]
            name_image = name_org_img_lst[2]
            source_url = name_org_img_lst[3]

            # 加个字段，这个字段可以解析出培养单位 履历介绍
            record = organiza

            uid = uuid.uuid1()
            suid = str(uid).replace('-', '')
            # 1. 成果唯一标识
            achievementID = suid

            # 2.中文名称
            chineseTitle = ''

            # 3. 英文名称
            englisthTitle = ''
            #
            # 4. 完成人
            if ' ' in name:
                # 有些有名字和奖项放一起的
                name = name.split(' ')[0]
            owner = name

            # 5. 完成单位
            # organization = ''
            organ = ''
            try:
                # 培养单位：北京航空航天大学
                re_xuexiao = re.compile('培养单位：(.*?大学)')
                # 航天工程大学教授
                re_daxue = re.compile('(.*?大学)')
                # 太极计算机股份有限公司总裁
                re_gongsi = re.compile('(.*?公司)')
                # 360集团创始人兼CEO
                re_jt = re.compile('(.*?集团)')
                # 国家并行计算机工程技术研究中心副研究员
                re_fyjy = re.compile('(.*?)副研究员')
                # 中国科学院计算技术研究所研究员
                re_yjy = re.compile('(.*?)研究员')
                organ_xuexiao = re.findall(re_xuexiao, organiza)
                organ_daxue = re.findall(re_daxue, organiza)
                organ_gongsi = re.findall(re_gongsi, organiza)
                organ_jt = re.findall(re_jt, organiza)
                organ_fyjy = re.findall(re_fyjy, organiza)
                organ_yjs = re.findall(re_yjy, organiza)
                if len(organ_xuexiao):
                    organ = organ_xuexiao[0].strip(' ')
                elif len(organ_daxue):
                    organ = organ_daxue[0]
                elif len(organ_gongsi):
                    organ = organ_gongsi[0]
                elif len(organ_jt):
                    organ = organ_jt[0]
                elif len(organ_fyjy):
                    organ = organ_fyjy[0]
                elif len(organ_yjs):
                    organ = organ_yjs[0]

            except Exception as e:
                print(e)

            if (organ == '') and ('培养单位：' in introduce):
                try:
                    # 培养单位：北京理工大学  # 培养大学：浙江大学
                    re_compile = re.compile('培养.*?：(.*?大学)')
                    organ_re = re.findall(re_compile, introduce)
                    if len(organ_re):
                        organ = organ_re[0].strip(' ')
                except Exception as e:
                    print(e)

            # 8. 国家,根据人民判断是否是中国还是国外
            # country = ''
            re_compile = re.compile('[\u4E00-\u9FA5]')
            country = re.findall(re_compile, owner)
            if len(country):
                country = '中国'
                # 9. 语言
                language = '中文'
            else:
                country = '国外'
                # 9. 语言
                language = '英文'

            #  6. 奖励时间
            date = date

            #  7. 奖励种类
            rewardType = 'CCF' + awards

            # 10. 奖励等级
            rewardRank = ''
            if awards == '科学技术奖':
                rewardRank = organiza
                organ = ''


            # 11. 受奖机构
            issuedBy = '中国科学技术协会'
            #
            # 12. 证书编号
            rewardNo = ''
            #
            # 13. 来源
            source = source_url

            # 15. 抓取时间
            spiderDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #
            data_json = {
                'achievementID': achievementID,
                'chineseTitle': chineseTitle,
                'englisthTitle': englisthTitle,
                'owner': owner,
                'organization': organ,
                'record': record,
                'date': date,
                'rewardType': rewardType,
                'country': country,
                'language': language,
                'rewardRank': rewardRank,
                'issuedBy': issuedBy,
                'rewardNo': rewardNo,
                'source': source,
                'owner_picture': name_image,
                'introduce': introduce,
                'spiderDateTime': spiderDateTime,
            }
            print(data_json)
            try:
                # mycol.insert_one(data_json)
                pass
            except Exception as e:
                print(e)


# 获取URL
def getUrls():
    Urls = []
    url_2005 = 'https://www.ccf.org.cn/qb/'
    Urls.append(url_2005)
    base_url = 'https://www.ccf.org.cn/awards/lnhjqk/{}/qb/'
    for year in range(2006, 2019):
        url = base_url.format(str(year))
        Urls.append(url)
    return Urls[:]

# 解析得到每个URL中每个奖项及每个奖项对应的信息
def parseUrls(Urls):
    Data = []
    for url in Urls:
        if url == 'https://www.ccf.org.cn/qb/':
            date = 2005
        else:
            date = int(url[37:41])
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            html = response.text
            html_data = etree.HTML(html)
            data = html_data.xpath('//div[@class="p-l p-r"]')[0]
            rewardType = data.xpath('./div[@class="title-com clear t-height m-sm"]/h3/text()')
            name_introduce = []
            clear = data.xpath('./div[@class="clear"]')
            for cle in clear[1:]:
                cols = cle.xpath('./div[@class="col-md-6"]')
                temp = []
                base_url = 'https://www.ccf.org.cn'
                for col in cols:
                    name = col.xpath('.//div[@class="media-body"]/h4/a/text()')[0]
                    organization = ''
                    organ = col.xpath('.//div[@class="media-body"]/div/text()')
                    name_img = col.xpath('.//div[@class="media-left"]/a/img/@src')
                    name_image = ''
                    if len(name_img):
                        if len(name_img[0]) > 1:
                            name_image = base_url + name_img[0]
                    if len(organ):
                        organization = organ[0]
                    # 将名字和培养单位和图片的url放一起+ source_url
                    name_org_img = name + "=" + organization + '=' + name_image + '=' + url
                    introduce = col.xpath('.//p[@class="clamp5"]/text()')[0]
                    temp.append([name_org_img, introduce])
                name_introduce.append(temp)
            data = zip(rewardType, name_introduce)
            for i in data:
                Data.append([date, i[0], i[1]])
    return Data




def main():
    Urls= getUrls()
    DataSets = parseUrls(Urls)
    parseFiled(DataSets)
if __name__ == '__main__':
    main()
