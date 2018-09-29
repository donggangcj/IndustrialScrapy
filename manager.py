#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : manager.py
@Author: donggangcj
@Date  : 2018/9/29
@Desc  : 
'''

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import  get_project_settings

"""Use the scrapy.crawler.CrawlerProcess to run the Spiders in a process simultaneously"""

def run_crawer_single_prcess():
    process = CrawlerProcess(get_project_settings())
    process.crawl('aii_alliance')
    process.crawl('beijing')
    process.start()



