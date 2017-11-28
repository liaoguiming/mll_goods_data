# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Item, Field


class GoodsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = Field()
    goods_title = Field()
    goods_sn = Field()
    goods_price = Field()
    goods_desc = Field()
    goods_type = Field()
    add_time = Field()
class GoodsItem1(scrapy.Item):
    goods_id = Field()
    add_time = Field()