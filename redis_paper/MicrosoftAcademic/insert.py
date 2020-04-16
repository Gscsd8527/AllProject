import pymongo
import json
myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
# myclient = pymongo.MongoClient('mongodb://10.0.82.131:27017/')
mydb = myclient['Microsoft']  # 数据库
mycol = mydb['refer']  # 表

mycol1 = mydb['refer_simplify']

# f = open('ReferenceData.json', 'r', encoding='utf-8')
# datas = f.readlines()
# data_list = [i.strip('\n') for i in datas]
# for dt in data_list:
#     dt_json = json.loads(dt)
#     print(dt_json)
#     mycol.insert_one(dt_json)

data = mycol.find()

for dt in data:
    init_name = dt['init_data']['name']
    init_id = dt['init_data']['id']
    paper_name = dt['name']
    paper_id = dt['id']
    num = dt['num']
    data_json = {
        'init_name': init_name,
        'init_id': init_id,
        'type': dt['type'],
        'paper_name': paper_name,
        'paper_id': paper_id,
        'num': num,
    }
    mycol1.insert_one(data_json)