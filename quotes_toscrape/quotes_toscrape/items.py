# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesToscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名言
    quote = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 标签
    tags = scrapy.Field()

    # url
    url = scrapy.Field()

    # 出生日期
    born_date = scrapy.Field()
    # 出生位置
    born_location = scrapy.Field()
    # 描述
    description = scrapy.Field()


