"""
该模块主要包括对图数据库的查询、检索等功能
"""
from py2neo import Graph, Node, Relationship, NodeMatcher



class GraphQuery(object):
    def __init__(self):
        self.g = Graph('bolt://localhost:7687', username='neo4j', password='123456')

    def query_weapon(self, weapon_name):
        """
        对武器装备类进行查询，对标北理工的需求
        :param weapon_name:
        :return:返回查询的结构-字典
        """
        cypher = ''
        return 0

    def query_unit(self, unit_name):
        """
        对部队类进行查询，对标郭老师需求，主要查询内容为部队可执行的任务
        :param unit_name:
        :return:返回查询的结构-字典
        """
        cypher = ''
        return 0