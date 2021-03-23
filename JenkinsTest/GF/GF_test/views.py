import json
#from GF_test.GraphQuery import GraphQuery
from django.shortcuts import render, HttpResponse
# Create your views here.


def keyword(request, keyword):
    """
    模糊查询接口
    :param request:
    :param keyword: 模糊查询的值
    :return:返回模糊查询结果列表，默认前五哥
    """
    query_result = {
        "code": "200",
        "data": [
            {
                "id": "sou_suo_id_1",
                "name": "sou_suo_name_1"
            },
            {
                "id": "sou_suo_id_2",
                "name": "sou_suo_name_2"
            },
            {
                "id": "sou_suo_id_3",
                "name": "sou_suo_name_3"
            },
            {
                "id": "sou_suo_id_4",
                "name": "sou_suo_name_4"
            },
            {
                "id": "sou_suo_id_5",
                "name": "sou_suo_name_5"
            }
        ]
    }

    print(query_result)
    return HttpResponse(json.dumps(query_result), content_type="application/json")


def keyword_query(request, keyword):
    """
    检索查询接口
    :param request:
    :param keyword: 检索的值
    :return: 返回泡泡：如果是武器类，则返回基本信息、北理工需求字段等等
    """
    query_result = {
        "code": "200",
        "data": [
            {
                "id": "pao_pao_id_1",
                "name": "pao_pao_name_1"
            },
            {
                "id": "pao_pao_id_2",
                "name": "pao_pao_name_2"
            },
            {
                "id": "pao_pao_id_3",
                "name": "pao_pao_name_3"
            }
        ]
    }

    print(query_result)
    return HttpResponse(json.dumps(query_result), content_type="application/json")


def pao_query(request, keyword, keyword_pao):
    """
    点击泡泡后进行的查询，传递检索参数以及泡泡关键词
    :param request:
    :param keyword:
    :param keyword_pao:
    :return:
    """
    query_result = {
        "code": "200",
        "data": {
            "nodes": [
                {
                    "id": "id_1",
                    "name": "name_1"
                },
                {
                    "id": "id_2",
                    "name": "name_2"
                },
                {
                    "id": "id_3",
                    "name": "name_3"
                },
                {
                    "id": "id_4",
                    "name": "name_4"
                }
            ],
            "links": [
                {
                    "from": "id_1",
                    "to": "id_2"
                },
                {
                    "from": "id_2",
                    "to": "id_3"
                },
                {
                    "from": "id_1",
                    "to": "id_4"
                }
            ]
        }
    }
    print(query_result)
    return HttpResponse(json.dumps(query_result), content_type="application/json")

