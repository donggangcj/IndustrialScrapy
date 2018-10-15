#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : manager.py
@Author: donggangcj
@Date  : 2018/9/29
@Desc  : 
'''

import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

"""Use the scrapy.crawler.CrawlerProcess to run the Spiders in a process simultaneously"""


def run_crawer_single_prcess():
    process = CrawlerProcess(get_project_settings())
    process.crawl('aii-alliance')
    process.crawl('beijing')
    process.crawl('sohu')
    process.crawl('jiangsu')
    process.crawl('huodongjia')
    process.crawl('gongxinbu')
    process.crawl('zhejiang')
    process.crawl('anhui')
    process.start()
    #TODO:定时任务实现
    # time.sleep(86400)


if __name__ == '__main__':
    run_crawer_single_prcess()
