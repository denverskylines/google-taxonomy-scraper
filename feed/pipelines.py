# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
import pymongo
from settings import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION


class FeedsPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = connection[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def process_item(self,item,spider):
        self.collection.insert(dict(item))
        return item

