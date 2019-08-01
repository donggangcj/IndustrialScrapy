# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy

from IndustrialScrapy.items import IndustrialItem


class NetofthingsguojiSpider(scrapy.Spider):
    name = 'netofthingsguoji'
    allowed_domains = ['netofthingsguoji']
    start_urls = ['http://www.netofthings.cn/GuoJi/']
    key = "工业物联网"

    def parse(self, response):
        selectors = response.xpath('//div[@class="summary"]')
        for selector in selectors:
            self.logger.debug(len(selectors))
            try:
                datetime_string = selector.xpath('.//div[@class="foot"]/span//text()').extract_first().strip()
                publish_time = datetime.strptime(datetime_string, '%m月%d日').replace(datetime.utcnow().year)
            except Exception as e:
                self.logger.warn("{} cannot format".format(datetime_string))
                publish_time = None
            if publish_time is None or abs((datetime.utcnow() - publish_time).days) > 180:
                yield None
            item = IndustrialItem()
            item['time'] = publish_time
            item['url'] = response.request.url.rstrip('GuoJi/') + selector.xpath(
                './/a[@class="nLink"]/@href').extract_first().lstrip('..')
            item['title'] = selector.xpath('.//a[@class="nLink"]/text()').extract_first()
            item['origin'] = 'netofthings'
            item['area'] = 'netofthings'
            item['keyword'] = self.key
            yield item
