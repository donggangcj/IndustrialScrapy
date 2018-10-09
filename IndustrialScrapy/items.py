# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndustrialscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProjectDeclareItem(scrapy.Item):
    ''' 项目申报 数据结构 '''
    # FIXME the comment format
    date = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()


class JobItem(scrapy.Item):
    jobname = scrapy.Field()
    url = scrapy.Field()
    origin = scrapy.Field()
    money = scrapy.Field()
    natural = scrapy.Field()
    exp = scrapy.Field()
    education = scrapy.Field()
    time = scrapy.Field()
    com_id = scrapy.Field()
    city = scrapy.Field()
    description = scrapy.Field()


class IndustrialItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    # data = scrapy.Field()
    area = scrapy.Field()
    origin = scrapy.Field()
    nature = scrapy.Field()
    time = scrapy.Field()
    # file_urls = scrapy.Field()
    keyword = scrapy.Field()
    begin_time = scrapy.Field()
    end_time = scrapy.Field()
