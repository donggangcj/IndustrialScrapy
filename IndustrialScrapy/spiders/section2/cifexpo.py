# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy

from IndustrialScrapy.items import IndustrialItem


class CifexpoSpider(scrapy.Spider):
    name = 'cifexpo'
    allowed_domains = ['cifexpo']
    start_urls = ['http://www.cif-expo.com/']
    key = '工业互联网'

    def parse(self, response):
        selectors = response.xpath('//ul[@class="index-infor-row index-infor-rowfirst clear"]')
        for selector in selectors:
            publish_time = datetime.strptime(
                '-'.join([selector.xpath('.//span[@class="infor-year"]//text()').extract_first(),
                          selector.xpath('.//span[@class="infor-day"]//text()').extract_first()]), '%y-%m-%d')
            if abs((datetime.utcnow() - publish_time).days) > 180:
                yield None
            item = IndustrialItem()
            item['time'] = publish_time
            item['title'] = selector.xpath('.//a[@class="infor-title"]//text()').extract_first().strip()
            self.logger.info(item['title'])
            item['url'] = response.request.url + selector.xpath('.//a[@class="infor-title"]//@href').extract_first()
            print('------ {}'.format(item['url']))
            item['origin'] = self.name
            item['area'] = self.name
            item['keyword'] = self.key
            yield item

