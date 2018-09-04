# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


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

