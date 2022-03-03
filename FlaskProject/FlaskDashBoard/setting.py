import os
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

DEBUG = True


SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{config["MySQL"]["mysql_username"]}:{config["MySQL"]["mysql_password"]}' \
    f'@{config["MySQL"]["mysql_host"]}:{config["MySQL"]["mysql_port"]}/{config["MySQL"]["mysql_db"]}?charset=utf8'

SQLALCHEMY_TRACK_MODIFICATIONS = False
