# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Clawler01Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GuanchaItem(scrapy.Item) :
    title = scrapy.Field()      # 文章标题
    url = scrapy.Field()        # 文章链接
    time = scrapy.Field()       # 发表时间
    source = scrapy.Field()     # 文章来源
    content = scrapy.Field()    # 文章内容

class SouhuItem(scrapy.Item):
    title = scrapy.Field()      # 文章标题
    url = scrapy.Field()        # 文章链接
    time = scrapy.Field()       # 发表时间
    content = scrapy.Field()    # 文章内容
    tag = scrapy.Field()        # 文章标签
