# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import os
import csv
import codecs
import json

from scrapy.exporters import JsonLinesItemExporter
from scrapy.exporters import JsonItemExporter

class Clawler01Pipeline:
    def process_item(self, item, spider):
        return item

class ClawlerGuanChaPipeline_CSV:
    def open_spider(self, spider):
        store_file = os.path.dirname(__file__) + '/spiders/guanchaWeb.csv'
        self.file = codecs.open(filename= store_file, mode= 'wb', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['文章标题', '文章链接', '发表时间', '文章来源', '文章内容'])


    def process_item(self, item, spider):
        line = (item['title'], item['url'], item['time'], item['source'], item['content']) 
        self.writer.writerow(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class ClawlerGuanChaPipeline_JSON:
    def open_spider(self, spider):
        store_file = os.path.dirname(__file__) + '/spiders/guanchaWeb.json'
        self.file = open(store_file, 'wb')
        self.exporter = JsonLinesItemExporter(self.file, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
 
    def close_item(self, spider):
        self.file.close()
        pass

class ClawlerSouhuPipeline_JSON:
    def open_spider(self, spider):
        # store_file = os.path.dirname(__file__) + '/data/souhuCarNews.json'
        # store_file = os.path.dirname(__file__) + '/data/souhuCarUse.json'
        store_file = os.path.dirname(__file__) + '/data/souhuCarBuy.json'
        self.file = open(store_file, 'wb')
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, Item, spider):
        self.exporter.export_item(Item)
        return Item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
