# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import MySQLdb
import MySQLdb.cursors
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
# from ArticleSpider.models.es_types import ArticleType
from w3lib.html import remove_tags
import sys
import csv
import itertools
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        self.file.flush()
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'kbe', 'kbe', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        print (insert_sql, params)
        cursor.execute(insert_sql, params)


class JsonExporterPipleline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                if ok:
                    image_file_path = value["path"]
                else:
                    image_file_path = "no img"
            item["front_image_path"] = image_file_path

        return item

#
# class ElasticsearchPiepeline(object):
#
#     def process_item(self, item, spider):
#         article = ArticleType()
#         article.title = item['title']
#         article.create_date = item['create_date']
#         article.content = item
#         article.content = remove_tags(item["content"])

# 链家到处到csv

# class CSVPipeline(object):

   # def __init__(self):
   #    self.csvwriter = csv.writer(open('lianjia.csv', 'wb'), delimiter=',')
   #    self.csvwriter.writerow(['names', 'starts', 'subjects', 'reviews'])
   #
   # def process_item(self, item, ampa):
   #
   #    rows = zip(item['names'],item['stars'],item['subjects'],item['reviews'])
   #
   #    for row in rows:
   #       self.csvwriter.writerow(row)
   #
   #    return item


class CSVPipeline(object):
   def __init__(self):
       self.files = {}

   @classmethod
   def from_crawler(cls, crawler):
       pipeline = cls()
       crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
       crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
       return pipeline

   def spider_opened(self, spider):
       # file = open('%s_items.csv' % spider.name, 'w+b')
       file = open('lianjia_items.csv', 'w+b')
       self.files[spider] = file
       self.exporter = CsvItemExporter(file)
       self.exporter.fields_to_export =  ['house_title', 'house_unit_price']
       self.exporter.start_exporting()

   def spider_closed(self, spider):
       self.exporter.finish_exporting()
       self.files[spider] = self.files.pop(spider)
       self.files[spider].close()

   def process_item(self, item, spider):
        if self.exporter:
            self.exporter.export_item(item)
        return item