# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy import log
from scrapy.exceptions import DropItem

from settings import MONGO_URI, MONGO_DATABASE


class JusCrawlerPipeline(object):
    collection_name = 'processes'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        Pull in information from settings.py.
        """
        return cls(
            mongo_uri=MONGO_URI,
            mongo_db=MONGO_DATABASE
        )

    def open_spider(self, spider):
        """
        Initializes spider and open db connection.
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """
        Clean up when spider is closed.
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        Save the result in MongoDB.
        """
        valid = True

        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))

        if valid:
            self.db[self.collection_name].replace_one({
                'process_number': item['process_number'],
                'court': item['court']
            },
                dict(item),
                True)
            log.msg("Process added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

