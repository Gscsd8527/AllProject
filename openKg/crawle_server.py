import requests
from lxml import etree
import uuid
import datetime
import pymongo

myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = myclient['OpenKg']  # 数据库
mydata = mydb['openKg_data']  # 表


base_url = 'http://openkg.cn'

def parseUrl(name, format, url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        html_data = etree.HTML(html)
        # 摘要
        abstract = ''
        try:
            abstract = html_data.xpath('//div[@class="notes embedded-content"]/p[1]/text()')[0]
        except Exception as e:
            print('摘要为： ', e)
        # print('abstract= ', abstract)
        broadside_html = html_data.xpath('//aside[@class="secondary span3"]/section')

        # 追从者
        follower = ''
        try:
            follower = broadside_html[0].xpath('.//span/text()')[0]
        except Exception as e:
            print('追从者;', e)
        # print('follower= ', follower)

        img_path = ''
        organization_name = ''
        try:
            organization_html = html_data.xpath('//aside[@class="secondary span3"]/div')[0].xpath('./section')[0]
            img_path = organization_html.xpath('.//*[@class="image"]/a/img/@src')[0].strip(' ').replace('\n', '')
            organization_name = organization_html.xpath('.//*[@class="heading"]/text()')[0].strip(' ').replace('\n', '').strip(' ')
        except Exception as e:
            print('organization=', e)
        organization = {
            'id': '',
            'organizationName': organization_name,
            'logo': img_path
        }
        # print(organization)

        authorization = ''
        try:
            authorization = broadside_html[-1].xpath('./*[@class="module-content"]/a/text()')[0].strip(' ').strip('\n')
        except Exception as e:
            print('权限：', e)
        # print('authorization= ', authorization)

        tags = []
        try:
            tags_html = html_data.xpath('//*[@class="tags"]/ul/li')
            for li in tags_html:
                tag = li.xpath('./a/text()')[0].strip(' ')
                tags.append(tag)
        except Exception as e:
            print('tags=', e)
        # print('tags= ', tags)

        source_metadata = {}
        try:
            source_metadata_tr = html_data.xpath('//section[@class="additional-info"]//tr')
            # print('source_metadata_tr长度为 ', len(source_metadata_tr))
            for tr in source_metadata_tr[1:]:
                td_name = tr.xpath('./th/text()')[0].strip(' ').replace('\n', '').replace('.', '_')
                try:
                    if ('最近更新' in td_name) or ('创建的' in td_name):
                        td_value = tr.xpath('./td/span/text()')[0].strip(' ').replace('\n', '').strip(' ')
                    else:
                        td_value = tr.xpath('./td/text()')[0].strip(' ').replace('\n', '').strip(' ')
                except:
                    td_value = tr.xpath('./td/a/text()')[0].strip(' ').replace('\n', '').strip(' ')
                source_metadata[td_name] = td_value
        except Exception as e:
            print('source_metadata:', e)
        print('source_metadata= ', source_metadata)

        dataAndResource = {}
        try:
            dataAndResource_html = html_data.xpath('//section[@id="dataset-resources"]/ul/li')
            for li in dataAndResource_html:
                dataAndResource_url = li.xpath('./a/@href')[0]
                resource_url = base_url + dataAndResource_url
                dataAndResource_name = li.xpath('./a/@title')[0].replace('.', '_')
                # print(dataAndResource_name, resource_url)
                resp = requests.get(resource_url)
                if resp.status_code == 200:
                    resp_html = resp.text
                    resp_data = etree.HTML(resp_html)
                    # 存储图片路径，有的话就加
                    path = ''
                    abs = ''
                    try:
                        # data_metadata = resp_data.xpath('//div[@class="row wrapper"]/section/div[@class="module-content"]')
                        data_metadata = resp_data.xpath('//section/div[@class="module-content"]')
                        path = data_metadata[0].xpath('.//p[@class="muted ellipsis"]/a/@href')[0]
                        abs = resp_data.xpath('.//blockquote/text()')[0]
                    except Exception as e:
                        print('path abs= ', e)
                    # print('path, abs=', path, abs)

                    metadata = {}
                    try:
                        table = resp_data.xpath('//div[@class="row wrapper"]/div[@class="primary span9"]//tr')
                        # 第一个是属性名称，需要去掉
                        for tr in table[1:]:
                            from lxml.html import tostring
                            td_name = tr.xpath('./th/text()')[0].strip(' ').replace('\n', '').replace('.', '_')
                            td_value = tr.xpath('./td/text()')[0].strip(' ').replace('\n', '')
                            metadata[td_name] = td_value
                    except Exception as e:
                        print('table=', e)
                    page_data = {
                        'resourceName': dataAndResource_name,
                        'url': resource_url,
                        'path': path,
                        'abstract': abs,
                        'metadata': metadata
                    }
                    dataAndResource[dataAndResource_name] = page_data.copy()

                else:
                    print('错误响应码为： ', resp.status_code)

        except Exception as e:
            print('数据和资源', e)
        uid = uuid.uuid1()
        suid = str(uid).replace('-', '')
        datasetId = suid
        spiderDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_json = {
            'datasetId': datasetId,
            'doi': '',
            'handle': '',
            'name': name,
            'abstract': abstract,
            'format': format,
            'organization': organization,
            'classfication': '',
            'metadata': source_metadata,
            'dataAndResource': dataAndResource,
            'tags': tags,
            'authorization': authorization,
            'follower': follower,
            'source': url,
            'spiderDateTime': spiderDateTime
        }
        print('data_json= ', data_json)
        try:
            mydata.insert_one(data_json)
        except Exception as e:
            print('插入错误： ', e)
    else:
        print('错误响应码为：', response.status_code)

def parseGetUrl():
    for i in range(1, 6):
        url = 'http://openkg.cn/dataset?page={}'.format(i)
        print('这是第 {}  页'.format(i))
        # url = 'http://openkg.cn/dataset'
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            html_data = etree.HTML(html)
            ul = html_data.xpath('//ul[@class="dataset-list unstyled"]/li')
            for li in ul:
                name = li.xpath('.//a/text()')[0]
                print('name= ', name)
                name = name.replace('.', '_')

                field_url = li.xpath('.//a/@href')[0]
                new_url = base_url + field_url
                format_data = li.xpath('./ul/li')
                format = []
                for i in format_data:
                    tgs = i.xpath('./a/text()')[0]
                    format.append(tgs)
                parseUrl(name, format, new_url)
        else:
            print('错误响应码为： ', response.status_code)

def main():
    parseGetUrl()

if __name__ == '__main__':
    main()