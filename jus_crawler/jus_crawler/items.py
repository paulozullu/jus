# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class InMemoryItemStore(object):
    __ITEM_STORE = None

    @classmethod
    def pop_items(cls):
        items = cls.__ITEM_STORE or []
        cls.__ITEM_STORE = None
        return items

    @classmethod
    def add_item(cls, item):
        if not cls.__ITEM_STORE:
            cls.__ITEM_STORE = []
        cls.__ITEM_STORE.append(item)


class ProcessItem(scrapy.Item):
    process_number = Field()
    court = Field()
    class_ = Field()
    area = Field()
    subject = Field()
    distribution_date = Field()
    judge = Field()
    value = Field()
    parts = Field()
    changes = Field()

