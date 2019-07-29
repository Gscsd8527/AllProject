import requests
import json
import uuid
import re
import datetime
import pymongo

myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = myclient['Kaggle']  # 数据库
mycol = mydb['data_test_two']  # 表
# getcol = mydb['Harvard_test']



# 数据集个数
DATASETS_UNM = 16813
# 原始的url
URL = 'https://www.kaggle.com/datasets_v2.json?sortBy=hottest&group=public&page={}&pageSize=20&size=all&filetype=all&license=all'
# 获取数据集url
def getDateSetsUrl():
    URLS = []
    # 页数，一个ajax里面包含20条纪录
    page_num = DATASETS_UNM // 20
    # 余数
    remainder = DATASETS_UNM % 20
    if remainder != 0:
        page_num += 1
    for num in range(1, page_num+1):
        URLS.append(URL.format(str(num)))
    return URLS

# 解析url得到HTML
def getHtml(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        html = resp.text
        return html
    else:
        print('错误码为： ', resp.status_code)
        return None

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
                    k, v = i[0].strip(' '), i[1].strip(' ')
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
                    k, v = i[0].strip(' '), i[1].strip(' ')
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



# 解析得到data字段数据
def parseData(html):
    try:
        re_compile = re.compile(r'<div data-component-name="DatasetContainer".*?<script>(.*?)</script>')
        data = re.findall(re_compile, html)[0]
        dt_compile = re.compile('push\((.*)}')
        dt = re.findall(dt_compile, data)[0]
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
        for i in a:
            file_name = i[0]
            file_size = i[1]
            file_about = i[2]
            file_column = i[3]
            file_type = ''
            if '.' in file_name:
                file_type = file_name.rsplit('.', 1)[-1]
            file_data[file_name] = {
                'fileSize': file_size,
                'fileType': file_type,
                'aboutThisFile': file_about,
                'columns': file_column
            }
        data_json = json.dumps(file_data)
    except:
        import traceback
        print('error= ', traceback.print_exc())
        file_data = {}
        data_json = json.dumps(file_data)
    return data_json

# 解析各页面信息
def parsePages(Urls):
    for url in Urls[:5]:
        try:
            print('url= ', url)
            response = requests.get(url)
            if response.status_code == 200:
                json_data = json.loads(response.text)
                datasetListItems = json_data['datasetListItems']
                # datasetListItems里面包含了20条记录，每个item就是一条记录
                for item in datasetListItems:
                    init_url = 'https://www.kaggle.com'
                    # 每篇论文的url
                    url = init_url + item['datasetUrl']

                    # 1. 数据集标识
                    uid = uuid.uuid1()
                    suid = str(uid).replace('-', '')
                    datasetId = suid

                    # # 2. 唯一标识
                    # datasetId = ''

                    # 3. doi
                    doi = ''

                    # 5. handle
                    handle = ''

                    # 6. tags
                    tags = []
                    temp = []
                    categories = item['categories']['categories']
                    for categorie in categories:
                        temp.append(categorie['name'])
                    tags = temp[:]

                    # 7. size，文件大小
                    size = item['datasetSize']

                    # 8. description 数据集描述（每个属性打标签）
                    description = ''
                    try:
                        html = getHtml(url)
                        re_compile = re.compile(r'<script type="application/ld\+json">(.*?)</script>')
                        data_set = re.findall(re_compile, html)[0]
                        re_description = re.compile(r'"description":(.*?)"url":')
                        description_temp = re.findall(re_description, data_set)[0].strip(',').strip('"')
                        # 清洗为自己需要的
                        dt = re.sub('<.*?>', '', description_temp)
                        # 去除 &gt
                        dt = dt.replace('&gt;', '').replace('&gt', '')
                        dt_compile = re.compile('###.*?\W.*?\s')
                        dt1 = re.findall(dt_compile, dt)
                        dt1_len = len(dt1)
                        i = 1
                        for na in dt1:
                            index = dt.index(na)
                            na_len = len(na)
                            index_len = index + na_len
                            if i < dt1_len:
                                next_index = dt.index(dt1[i])
                                text = dt[index_len:next_index]
                            else:
                                text = dt[index_len:]
                            i += 1
                            text = text.strip(' ').replace(r'\n', '').replace('\\', '')
                            na = re.findall('([a-zA-Z].*?)\W', na)[0]
                            temp_str = '<{}>{}<{}>'.format(na, text, na)
                            description += temp_str
                    except:
                        pass

                    # 9. 实体相关
                    # data = ''
                    # try:
                    html = getHtml(url)
                    data = parseData(html)
                    # except:
                    #     pass

                    # 10. 相似数据集
                    similarDatasets = ''
                    try:
                        similar_url = url + '/suggestions.json'
                        response = requests.get(similar_url)
                        if response.status_code == 200:
                            json_data = json.loads(response.text)
                            similarDatasets_dict = {}
                            for every in json_data:
                                name = every['title']
                                start_url = 'https://www.kaggle.com'
                                name_url = start_url + every['entityUrl']
                                similarDatasets_dict[name] = name_url
                            similarDatasets = json.dumps(similarDatasets_dict)
                        else:
                            print('code= ', response.status_code)
                    except:
                        pass

                    # 11. 版本信息
                    license = item['licenseName']

                    # 12. 可见性
                    visibility = 'Public'

                    # 13. provenance
                    provenance_source = ''

                    # 14. 数据集所有者
                    datasetOwner = item['ownerName']

                    # 15. 数据集所有者头像url
                    datasetOwnerIconPath = item['ownerAvatarUrl']

                    # 16. 合作者
                    collaborators = ''

                    # 17. 合作者的头像url
                    collaboratorIconPath = ''

                    # 18. 预计更新频率
                    expectedUpdateFrequency = ''
                    expectedUpdateFrequency_score = item['usabilityRating']['updateFrequencyScore']
                    if expectedUpdateFrequency_score == 0:
                        expectedUpdateFrequency = '0: Not specified'

                    # 19. 上次更新时间
                    lastUpdated = item['dateUpdated']

                    # 20. 数据创建时间
                    dateCreated = item['dateCreated']

                    # 21. 当前版本
                    currentVersion = item['currentDatasetVersionNumber']

                    # 22. 存储路径
                    path = ''

                    # 23. source
                    source = url

                    # 24. 文件url
                    start_url = 'https://www.kaggle.com'
                    file_url = start_url + item['downloadUrl']

                    # 25. 元数据
                    data_json = json.dumps(item)

                    # 24. 数据抓取时间
                    spiderDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    Data = {
                        'datasetId': datasetId,
                        'doi' : doi,
                        'handle' : handle,
                        'tags' : tags,
                        'size' : size,
                        'description' : description,
                        'data' : data,
                        'similarDatasets' : similarDatasets,
                        'license' : license,
                        'visibility' : visibility,
                        'provenance_source' : provenance_source,
                        'datasetOwner' : datasetOwner,
                        'datasetOwnerIconPath' : datasetOwnerIconPath,
                        'collaborators' : collaborators,
                        'collaboratorIconPath' : collaboratorIconPath,
                        'expectedUpdateFrequency' : expectedUpdateFrequency,
                        'lastUpdated' : lastUpdated,
                        'dateCreated' : dateCreated,
                        'currentVersion' : currentVersion,
                        'path' : path,
                        'source' : source,
                        'file_url' : file_url,
                        'data_json' : data_json,
                        'spiderDateTime' : spiderDateTime,
                    }
                    print('url= ', source)
                    print('data= ', data)
                    print(Data)
                    mycol.insert_one(Data)
                    print('===========================')
        except Exception as e:
            with open('except_url.txt', 'a+', encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
            print(e)

def main():
    urls = getDateSetsUrl()
    parsePages(urls)

if __name__ == '__main__':
    main()
