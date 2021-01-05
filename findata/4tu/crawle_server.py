import requests
import json
import pymongo
import time

myclient = pymongo.MongoClient('mongodb://*********:27017/')
mydb = myclient['dataset']  # 数据库
mycol = mydb['4tu']  # 表



class Tu4:
    def __init__(self):
        self.url = 'https://data.4tu.nl/api/graphql?thirdPartyCookies=true&type=current&operation=search'
        self.data = {
            "operationName":"search",
            "variables":{
                "q":"",
                "sort":
                    {
                        "by":"published_date",
                        "type":"desc"
                    },
                "filters":
                    {
                        "institutionId":898
                    },
                "cursor":"",
                "pageSize":40
            },
            "query":"query search($q: String, $cursor: String, $pageSize: Int, $sort: Order, $filters: SearchFiltersInput) {\n  search(searchTerm: $q, cursor: $cursor, pageSize: $pageSize, sort: $sort, filters: $filters) {\n    count\n    cursor\n    suggestions {\n      ... on ItemVersionListEntity {\n        __typename\n        id\n        title\n        version\n        openInNewTab\n        isEmbargoed\n        embargoDate\n        embargoType\n        timeline {\n          onlinePublication\n          publisherPublication\n          publisherAcceptance\n          submission\n          posted\n          revision\n        }\n        institution {\n          id\n          name\n        }\n        definedType: itemType {\n          id\n          name\n          icon\n        }\n        authors {\n          count\n          elements {\n            id\n            openInNewTab\n            name\n            urlName\n            url\n            isPublic\n            isActive\n          }\n        }\n        isConfidential\n        isMetadataRecord\n        thumb\n        url\n      }\n      ... on CollectionVersionListEntity {\n        __typename\n        id\n        title\n        version\n        timeline {\n          onlinePublication\n          publisherPublication\n          publisherAcceptance\n          submission\n          posted\n          revision\n        }\n        institution {\n          id\n          name\n        }\n        authors {\n          count\n          elements {\n            id\n            openInNewTab\n            name\n            urlName\n            url\n            isPublic\n            isActive\n          }\n        }\n        url\n      }\n      ... on ProjectListEntity {\n        __typename\n        id\n        title\n        authors {\n          count\n          elements {\n            id\n            openInNewTab\n            name\n            urlName\n            url\n            isPublic\n            isActive\n          }\n        }\n        institution {\n          id\n          name\n        }\n        url\n        publishedDate\n      }\n    }\n    items: elements {\n      ... on ItemVersionListEntity {\n        __typename\n        id\n        title\n        version\n        openInNewTab\n        isEmbargoed\n        embargoDate\n        embargoType\n        timeline {\n          onlinePublication\n          publisherPublication\n          publisherAcceptance\n          submission\n          posted\n          revision\n        }\n        institution {\n          id\n          name\n        }\n        definedType: itemType {\n          id\n          name\n          icon\n        }\n        authors {\n          count\n          elements {\n            id\n            openInNewTab\n            name\n            urlName\n            url\n            isPublic\n            isActive\n          }\n        }\n        isConfidential\n        isMetadataRecord\n        thumb\n        url\n      }\n      ... on CollectionVersionListEntity {\n        __typename\n        id\n        title\n        version\n        timeline {\n          onlinePublication\n          publisherPublication\n          publisherAcceptance\n          submission\n          posted\n          revision\n        }\n        institution {\n          id\n          name\n        }\n        authors {\n          count\n          elements {\n            id\n            openInNewTab\n            name\n            urlName\n            url\n            isPublic\n            isActive\n          }\n        }\n        url\n      }\n      ... on ProjectListEntity {\n        __typename\n        id\n        title\n        authors {\n          count\n          elements {\n            id\n            openInNewTab\n            name\n            urlName\n            url\n            isPublic\n            isActive\n          }\n        }\n        institution {\n          id\n          name\n        }\n        url\n        publishedDate\n      }\n    }\n  }\n}\n"

        }
        self.count = 6421
        self.CURSOR = ''

    def run(self):
        pages = self.get_pages()
        index = 1
        for _ in range(pages):
            self.request()
            print(index, '*'*100)
            index += 1

    def request(self):
        time.sleep(1)
        self.data['variables']['cursor'] = self.CURSOR
        response = requests.post(self.url, data=json.dumps(self.data))
        if response.status_code == 200:
            text = response.text
            data_json = json.loads(text)
            # print(data_json)
            self.CURSOR = data_json['data']['search']['cursor']
            items = data_json['data']['search']['items']
            for item in items:
                print(item['title'])
                # mycol.insert_one(item)


        else:
            print('错误响应码为： ', response.status_code)


    def get_pages(self):
        """
        获取页数
        :return:
        """
        pages = self.count // 40
        ys = self.count % 40
        if ys > 0:
            pages += 1
        return pages


def main():
    """
    4tu网站抓取
    :return:
    """
    tu4 = Tu4()
    tu4.run()


if __name__ == '__main__':
    main()
