# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class jdbraitem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content=Field()
    productColor=Field()
    productSize=Field()
    referenceName=Field()
    score=Field()
    id=Field()
