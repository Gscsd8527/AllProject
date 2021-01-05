import requests
import json

class Aminer:
    def __init__(self):
        self.gcy_url = 'https://apiv2.aminer.cn/magic?a=getExpertBases__expertbase.search.gctsearch___'  # 工程院院士
        self.kxy_url = 'https://apiv2.aminer.cn/magic?a=SEARCH__expertbase.search.gctsearch___'  # 科学院院士
        self.gcy_data = """[{"action":"expertbase.search.gctsearch","parameters":{"searchType":"ToBPerson","offset":%s,"size":20,"switches":["lang_zh","intell_expand"],"filters":{"dims":{"eb":["55e6573845ce9da5c99535a9"]}}},"schema":{"person":["id","name","title","name_zh","avatar","tags",{"profile":["position","position_zh","affiliation","affiliation_zh","org","org_zh"]},{"indices":["hindex","gindex","pubs","citations","newStar","risingStar","activity","diversity","sociability"]},"tags_translated_zh"]}}]"""
        self.kxy_data = """[{"action":"expertbase.search.gctsearch","parameters":{"searchType":"ToBPerson","offset":%s,"size":20,"switches":["lang_zh","intell_expand"],"filters":{"dims":{"eb":["55ebd8b945cea17ff0c53d5a"]}}},"schema":{"person":["id","name","title","name_zh","avatar","tags",{"profile":["position","position_zh","affiliation","affiliation_zh","org","org_zh"]},{"indices":["hindex","gindex","pubs","citations","newStar","risingStar","activity","diversity","sociability"]},"tags_translated_zh"]}}]"""
        self.gcy_pages = 86
        self.kxy_pages = 75
        self.person_url = 'https://gct.aminer.cn/eb/profile/'
        self.person_data = """[{"action":"expertbase.search.gctsearch","parameters":{"ids":["%s"]},"schema":{"person":["id","name","name_zh","avatar","num_view","is_follow","work","hide","nation","language","bind","acm_citations","links","educations","tags","tags_zh","num_view","num_follow","is_upvoted","num_upvoted","is_downvoted","is_lock",{"indices":["hindex","pubs","citations"]},{"profile":["position","position_zh","affiliation","affiliation_zh","work","gender","lang","homepage","phone","email","fax","bio","edu","address","note","homepage"]}]}}]"""
        self.file_path = './file/'
        self.headers = {
            'Referer': 'https://gct.aminer.cn/eb/gallery/detail/eb/55e6573845ce9da5c99535a9'
        }

    def run(self):
        request_data = [[self.gcy_url, self.gcy_pages, '工程院'], [self.kxy_url, self.kxy_pages, '科学院']]
        for data in request_data:
            for page in range(0, data[1]):
                print(data[0], page, data[2])
                self.request(data[0], page, data[2])


    def request(self, url, page, person_type):
        if person_type == '工程院':
            response = requests.post(url, data=self.gcy_data % (page * 20) , headers=self.headers)
        elif person_type == '科学院':
            response = requests.post(url, data=self.kxy_data % (page * 20), headers=self.headers)

        if response.status_code == 200:
            text = response.text
            data_json = json.loads(text)
            data_list = data_json['data'][0]['items']
            for data in data_list:
                print(data['name_zh'], person_type, page)
                data.update({'type': person_type})
                temp_string = json.dumps(data, ensure_ascii=False)
                with open('data.json', 'a+', encoding='utf-8') as f:
                    f.write('{}\n'.format(temp_string))
        else:
            print('错误响应码为： ', response.status_code)


    def parse(self):
        data = self.get_person_id()
        for dt in data:
            print(dt)
            person_id = dt['id']
            person_type = dt['person_type']
            if person_type == '工程院':
                url = self.gcy_url
            elif person_type == '科学院':
                url = self.kxy_url
            response = requests.post(url, data=self.person_data % (person_id))
            if response.status_code == 200:
                text = response.text
                data_json = json.loads(text)
                item = data_json['data'][0]['items'][0]
                name_zh = item['name_zh']
                name = item['name']
                id = item['id']
                try:
                    position = item['profile']['position']
                except:
                    position = ''
                try:
                    affiliation = item['profile']['affiliation']
                except:
                    affiliation = ''
                try:
                    homepage = item['profile']['homepage']
                except:
                    homepage = ''
                try:
                    edu = item['profile']['edu']
                except:
                    edu = ''
                try:
                    work = item['profile']['work']
                except:
                    work = ''
                try:
                    bio = item['profile']['bio']
                except:
                    bio = ''
                try:
                    img_url = item['avatar']
                except:
                    img_url = ''

                data_json = {
                    'name_zh': name_zh,
                    'name': name,
                    'id': id,
                    'position': position,
                    'affiliation': affiliation,
                    'homepage': homepage,
                    'edu': edu,
                    'work': work,
                    'bio': bio,
                    'img_url': img_url,
                    'type': person_type,
                    'soucre_data': item,
                }
                print(data_json)
                # temp_string = json.dumps(data_json, ensure_ascii=False)
                # with open('data_json.json', 'a+', encoding='utf-8') as f:
                #     f.write('{}\n'.format(temp_string))

            else:
                print('错误响应码为： ', response.status_code)


    @staticmethod
    def get_person_id():
        """
        获取人的id
        :return:
        """
        f = open('data.json', encoding='utf-8')
        ids = [{'id': json.loads(i.strip('\n'))['id'], 'person_type': json.loads(i.strip('\n'))['type'], 'name': json.loads(i.strip('\n'))['name_zh']} for i in f.readlines()]
        return ids


    def img_download(self):
        """
        图片下载
        :return:
        """
        f = open('data_json.json', encoding='utf-8')
        img_url = [{'id': json.loads(i.strip('\n'))['id'], 'img_url': json.loads(i.strip('\n'))['img_url'], 'name': json.loads(i.strip('\n'))['name_zh']} for i in f.readlines()]

        for img_info in img_url:
            try:
                url = img_info['img_url']
                id = img_info['id']
                print(img_info)
                response = requests.get(url)
                if response.status_code == 200:
                    with open(self.file_path + '{}.jpg'.format(id), 'wb') as fd:
                        # 每到128位就写入
                        for chunk in response.iter_content(128):
                            fd.write(chunk)
                else:
                    print(f'获取图片失败： 错误响应码为{response.status_code}')

            except:
                pass


def main():
    """
    全球华人专家库
    :return:
    """
    aminer = Aminer()
    # aminer.run()
    # aminer.parse()
    # aminer.img_download()


if __name__ == '__main__':
    main()
