# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SohuItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    updatetime = scrapy.Field()
    img_path = scrapy.Field()
    img_url = scrapy.Field()
    href = scrapy.Field()
    copy_from = scrapy.Field()
    content = scrapy.Field()
    pass
