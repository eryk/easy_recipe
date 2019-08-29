# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os


class EasyRecipePipeline(object):
    def process_item(self, item, spider):
        return item


class MeishijPipeline(object):
    def __init__(self):
        self.store_file = os.path.dirname(__file__) + '/meishij.csv'
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        with open(self.store_file, 'a+') as f:
            for item in self.items:
                f.write(("%s,%s,%s\n" % (item['title'], item['url'], ' '.join(item['ingredient']))).encode('gb2312'))
