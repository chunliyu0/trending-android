# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from datetime import datetime,timedelta
from dateutil.parser import parse
from scrapy.exceptions import DropItem

class StackoverflowPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient('127.0.0.1',27017)
        self.db = self.connection.testdb1
        self.collection = self.db.stackoverflow

    def enough_days_collected(self,item):
        asked_time = parse(item['asked_time'][0])
        return (datetime.now(tz=asked_time.tzinfo) - asked_time) >= timedelta(minutes=30)

    def process_item(self, item, spider):
        if not self.connection or not item:
            print('db not connected!')
            return

        if self.enough_days_collected(item):
            spider.crawler.engine.close_spider(spider,"enough items collected; stopping crawler...")
        print('saving item to db...')
        self.collection.save(item)

    def __del__(self):
        if self.connection:
            self.connection.close()

