# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem

try:
    from jus_crawler.jus_crawler.items import InMemoryItemStore
except ImportError:
    from jus_crawler.items import InMemoryItemStore


class JusCrawlerPipeline(object):

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
            return item
