# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy

from IndustrialScrapy.items import IndustrialItem


class CcidnetSpider(scrapy.Spider):
    name = 'ccidnet'
    allowed_domains = ['ccidnet']
    start_urls = ['http://app.ccidnet.com/?app=search&controller=index&action=search&type=all&wd=%E5%B7%A5%E4%B8%9A%E4%BA%92%E8%81%94%E7%BD%91']
    key = '工业互联网'

    def parse(self, response):
        selectors = response.xpath('//div[@class="num_zi F_Left"]')
        for selector in selectors:
            item = IndustrialItem()
            item['title'] = selector.xpath('.//a/text()').extract_first()
            item['url'] =selector.xpath('.//a//@href').extract_first()
            item['origin'] = self.name
            item['area'] = self.name
            item['keyword'] = self.key
            item['time'] = datetime.utcnow()
            yield item
