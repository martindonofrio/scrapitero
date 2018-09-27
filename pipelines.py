# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime
from tutorial import settings
import logging

class TutorialPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            charset = 'utf8',
            use_unicode = True
        )
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "insert into article (createDate, codigoAnunciante, codigoZonaProp, direccion, antiguedadAviso, precio, superficieTotal) value(%s, %s, %s, %s, %s, %s, %s)",
                (datetime.datetime.now(), item['codigoAnunciante'], item['codigoZonaProp'], item['direccion'], item['antiguedadAviso'], item['precio'], item['superficieTotal']))
            self.connect.commit()
        except Exception as error:
            logging.log(error)
        return item

    def close_spider(self, spider):
        self.connect.close();