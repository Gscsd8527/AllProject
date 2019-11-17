import requests
import re
import json
import uuid
import datetime

BASE_URL = 'https://www.kaggle.com'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
Session = requests.session()
# 最多给显示1万的数据，所以写个10020
DATASETS = 10020

def getToken():
    headers = HEADERS.copy()
    headers['upgrade-insecure-requests'] = '1'
    url = 'https://www.kaggle.com/datasets'
    response = Session.get(url, headers=headers)
    token = ''
    if response.status_code == 200:
        text = response.text
        token = re.findall("antiForgeryToken: '(.*?)',", text)[0]
    else:
        print('错误响应码为： ', response.status_code)
    return token

# 获取每一页请求的data数据
def getEveryPageData(token):
    # data_list = []
    pages = DATASETS // 20
    ys = DATASETS % 20
    if ys > 1:
        pages += 1
    for num in range(1, pages+1):
    # for num in range(1, DATASETS+1):
        print('总共有 {}  页，这是第  {}  条数据'.format(pages, num))
        data = {
            "page": num,
            "group": "public",
            "size": "all",
            "fileType": "all",
            "license": "all",
            "viewed": "all",
            "categoryIds": [],
            "search": "",
            # "sortBy": "hottest",
            # "sortBy": "votes",
            # "sortBy": "published",
            # "sortBy": "updated",
            "sortBy": "usability",
            "userId": None,
            "organizationId": None,
            "maintainerOrganizationId": None,
            "minSize": None,
            "maxSize": None,
            "isUserQuery": 'false'
        }
        requestEveryPageData(token, data)
    #     data_list.append(data)
    # return data_list

# 将数组大小对齐
def myadd(lst1, lst2):
    if len(lst2) < len(lst1):
        my_len = len(lst1) - len(lst2)
        for i in range(my_len):
            lst2.append(' ')
    return lst2

# 解析文件带后缀
def parse1(dt, filenames, filesizes, about_this_files, Columns):
    try:
        filename = re.findall('"relativePath":"(.*?)",', dt)
        # 提取文件名和文件大小
        for na in filename:
            try:
                name = na.split('/')[-1]
                filenames.append(name)
                size = re.findall('%s.*?"rowCount":(\d+)' % name, dt)
                if len(size):
                    filesizes.append(size[0])
                else:
                    filesizes.append(' ')
            except:
                pass
        # 提取关于文件的介绍
        for name in filenames:
            try:
                about_this_file = re.findall('"name":"%s","description":"(.*?)"}' % name, dt)
                if len(about_this_file):
                    about_file = about_this_file[0].replace('\n', '').replace('\\', '').replace('u0022', '').replace('u0026gt;', '').replace('u0026lt;', '').replace('u0027', '')
                    about_this_files.append(about_file)
                else:
                    about_this_files.append(' ')
            except:
                pass
        # 提取columns，这个columns在文件名上方
        for name in filenames:
            filename_len = len(filenames)
            index = filenames.index(name)
            # 判断是否不是最后一个文件
            column = ''
            if index < (filename_len-1):
                # 从出现这个文件开始到下个文件开始结束，遇到带后缀的就还能匹配
                try:
                    col_compile = re.compile('%s.*?"columns":.*?%s' % (name, name))
                    data1 = re.findall(col_compile, dt)[0]
                    column = re.findall('"name":"(.*?)","description":("\w+.*?"|null)', data1)
                except:
                    pass
            elif filenames[-1] == name:
                try:
                    col_compile = re.compile('%s.*?"columns":.*?%s' % (name, name))
                    data1 = re.findall(col_compile, dt)[0]
                    column = re.findall('"name":"(.*?)","description":("\w+.*?"|null)', data1)
                except:
                    pass
            columns = []
            dct = {}
            if len(column):
                # temp = []
                for i in column:
                    k, v = i[0].strip(' '), i[1].strip(' ').strip(r'\"')
                    dct[k] = v
                for k, v in dct.items():
                    if len(k):
                        if len(k) > 300:
                            k = ''
                        if len(v) > 500:
                            v = ''
                        # temp.append(k)
                        if k not in filenames:
                            columns.append([k, v])
                Columns.append(columns)
            else:
                Columns.append(['',''])
            del dct
    except:
        pass
    return filenames, filesizes, about_this_files, Columns

# 解析文件不带后缀
def parse2(dt, filenames, filesizes, about_this_files, Columns):
    try:
        data = re.findall('],"name":"(.*?)","description":"(.*?)"', dt)
        filenames = []
        filesizes = []
        about_this_files = []
        Columns = []
        # 得到文件名和文件描述
        for i in data:
            filter_str = 'Context'
            if filter_str not in i[1]:
                k = i[0].strip(' ')
                if len(k) > 300:
                    k = ' '
                v = i[1].strip(' ')
                if len(v) > 500:
                    v = ' '
                filenames.append(k)
                about_this_files.append(v)
        # 得到文件大小
        for name in filenames:
            size = re.findall('%s.*?"rowCount":(\d+)' % name, dt)
            if len(size):
                filesizes.append(size[0])
            else:
                filesizes.append(' ')
        # 得到column
        for name in filenames:
            index = filenames.index(name)
            if index == 0:
                col_compile = re.compile('"columns":.*?%s' % name)
                data1 = re.findall(col_compile, dt)[0]
                column = re.findall('"name":"(.*?)","description":("\w+.*?"|null|"")', data1)
            else:
                col_compile = re.compile('%s.*?"columns":.*?%s' % (filenames[index - 1], name))
                data1 = re.findall(col_compile, dt)[0]
                column = re.findall('"name":"(.*?)","description":("\w+.*?"|null|".*?")', data1)
            columns = []
            dct = {}
            if len(column):
                # temp = []
                for i in column:
                    k, v = i[0].strip(' '), i[1].strip(' ').strip(r'\"')
                    dct[k] = v
                for k, v in dct.items():
                    if len(k):
                        if len(k) > 300:
                            k = ''
                        if len(v) > 500:
                            v = ''
                        # temp.append(k)
                        if k not in filenames:
                            columns.append([k, v])
                Columns.append(columns)
            else:
                Columns.append(['', ''])
            del dct
            # if len(column):
            #     for i in column:
            #         k = i[0].strip(' ')
            #         if len(k) > 300:
            #             k = ' '
            #         v = i[1].strip(' ')
            #         if len(v) > 500:
            #             v = ' '
            #         if k not in filenames:
            #             columns.append([k, v])
            #     Columns.append(columns)
            # else:
            #     Columns.append([['', ''],])
    except:
        pass
    return filenames, filesizes, about_this_files, Columns


def parseData(dt):
    # 提取文件名
    filename = re.findall('"relativePath":"(.*?)",', dt)
    # 根据filename的值来判断两套解析规则
    # 文件名列表
    filenames = []
    # 文件大小列表
    filesizes = []
    # 关于文件解释列表
    about_this_files = []
    # 每个文件对应的columns列表
    Columns = []
    if filename:
        filenames, filesizes, about_this_files, Columns = parse1(dt, filenames, filesizes, about_this_files, Columns)
    else:
        filenames, filesizes, about_this_files, Columns = parse2(dt, filenames, filesizes, about_this_files, Columns)
    filesizes = myadd(filenames, filesizes)
    about_this_files = myadd(filenames, about_this_files)
    Columns = myadd(filenames, Columns)
    a = zip(filenames, filesizes, about_this_files, Columns)
    file_data = {}
    index = 1
    for i in a:
        file_name = i[0]
        file_size = i[1]
        file_about = i[2]
        file_column = i[3]
        file_type = ''
        if '.' in file_name:
            file_type = file_name.rsplit('.', 1)[-1]
        temp_dict = {
            index: {
                'fileName': file_name,
                'fileSize': file_size,
                'fileType': file_type,
                'aboutThisFile': file_about,
                'columns': file_column
            }
        }
        file_data.update(temp_dict)
        index += 1
    return file_data



def parseUrl(url):
    headers = HEADERS.copy()
    temp_headers = {
        'accept': 'text/html, application/xhtml+xml',
        'Referer': 'https://www.kaggle.com/datasets',
        'Turbolinks-Referrer': 'https://www.kaggle.com/datasets'
    }
    headers.update(temp_headers)
    response = requests.get(url, headers=headers)
    text = response.text
    # re_compile = re.compile(r'<script type="application/ld\+json">(.*?)</script>')
    re_compile = re.compile(r'<script.*?type="application/ld\+json">(.*?)</script>')
    description_str = re.findall(re_compile, text)[0]
    # re_compile = re.compile(r'<div data-component-name="DatasetContainer".*?<script>(.*?)</script>')
    re_compile = re.compile(r'<div data-component-name="DatasetContainer".*?<script.*?>(.*?)</script>')
    data = re.findall(re_compile, text)[0]
    dt_compile = re.compile('push\((.*)}')
    dt = re.findall(dt_compile, data)[0]
    return description_str, dt



# 请求每一页的数据
def requestEveryPageData(token, data):
    url = 'https://www.kaggle.com/requests/SearchDatasetsRequest'
    headers = HEADERS.copy()
    temp_headers = {
        '__requestverificationtoken': token,
        'accept': 'application/json',
        'content-type': 'application/json',
        'Referer': 'https://www.kaggle.com/datasets',
        'x-xsrf-token': token
    }
    headers.update(temp_headers)
    # for data in data_list:
    response = Session.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        text = response.text
        data_json = json.loads(text)
        items = data_json['result']['items']
        for item in items:
            try:
                # 1. 数据集标识
                uid = uuid.uuid1()
                suid = str(uid).replace('-', '')
                datasetId = suid
                doi = ''
                handle = ''
                title = item['title']
                print('name= ', title)
                datasetOwner = item['ownerName']
                datasetOwnerIconPath = item['ownerAvatarUrl']
                overview = item['overview']
                downloadUrl = ''
                try:
                    downloadUrl = BASE_URL + item['downloadUrl']
                except:
                    print('downloadUrl error')
                source = BASE_URL + item['datasetUrl']
                lastUpdated = item['dateUpdated']
                dateCreated = item['dateCreated']
                license = item['licenseName']
                visibility = 'Public'
                datasetSize = ''
                try:
                    datasetSize = item['datasetSize']
                except:
                    print('datasetSize error')
                currentVersion = item['currentDatasetVersionNumber']
                expectedUpdateFrequency = ''
                try:
                    expectedUpdateFrequency_score = item['usabilityRating']['updateFrequencyScore']
                    if expectedUpdateFrequency_score == 0:
                        expectedUpdateFrequency = '0: Not specified'
                except Exception as e:
                    print('expectedUpdateFrequency error', e)
                tags = []
                categories = item['categories']['categories']
                for categorie in categories:
                    tags.append(categorie['name'])
                collaborators = ''
                collaboratorIconPath = ''
                # 相似数据集
                similarDatasets = ''
                try:
                    similar_url = source + '/suggestions.json'
                    similar_headers = headers.copy()
                    similar_headers['Referer'] = source
                    response = requests.get(similar_url, similar_headers)
                    if response.status_code == 200:
                        json_data = json.loads(response.text)
                        similarDatasets_dict = {}
                        similar_index = 1
                        for every in json_data:
                            name = every['title']
                            start_url = 'https://www.kaggle.com'
                            name_url = start_url + every['entityUrl']
                            thumbnailImageUrl = every['thumbnailImageUrl']
                            temp_dict = {
                                similar_index: {
                                    'name': name,
                                    'nameUrl': name_url,
                                    'nameImgUrl': thumbnailImageUrl
                                }
                            }
                            similarDatasets_dict.update(temp_dict)
                            similar_index += 1
                        similarDatasets = similarDatasets_dict.copy()
                except:
                    pass
                description = ''
                description_json = ''
                ColumsData_str = ''
                try:
                    description_str, ColumsData_str = parseUrl(source)
                    description_json = json.loads(description_str)
                    description = description_json['description']
                    # data = parseData(ColumsData_str)
                except Exception as e:
                    print('description error', e)

                spiderDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # print('url=  ', source)
                Data = {
                    'datasetId': datasetId,
                    'doi': doi,
                    'handle': handle,
                    'name': title,
                    'overview': overview,
                    'tags': tags,
                    'size': datasetSize,
                    'description': description,
                    'description_source': description_json,
                    'data': '',
                    'data_source': ColumsData_str,
                    'similarDatasets': similarDatasets,
                    'license': license,
                    'visibility': visibility,
                    'provenance_source': '',
                    'datasetOwner': datasetOwner,
                    'datasetOwnerIconPath': datasetOwnerIconPath,
                    'collaborators': collaborators,
                    'collaboratorIconPath': collaboratorIconPath,
                    'expectedUpdateFrequency': expectedUpdateFrequency,
                    'lastUpdated': lastUpdated,
                    'dateCreated': dateCreated,
                    'currentVersion': currentVersion,
                    'path': '/data/www/html/dataset/Kaggle',
                    'source': source,
                    'file_url': downloadUrl,
                    'data_json': item,
                    'spiderDateTime': spiderDateTime,
                }
                Data_json = json.dumps(Data)
                with open('KaggleData4.json', 'a+', encoding='utf-8') as f:
                    f.write(Data_json)
                    f.write('\n')
            except Exception as e:
                print('cuowu= ', e)
                with open('error.json', 'a+', encoding='utf-8') as f:
                    f.write(BASE_URL + item['downloadUrl'])
                    f.write('\n')
    else:
        print('错误响应码为---： ', response.status_code)

def main():
    token = getToken()
    # data_list = getEveryPageData()
    # requestEveryPageData(token, data_list)
    getEveryPageData(token)

if __name__ == '__main__':
    main()

