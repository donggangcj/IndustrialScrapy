# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy

from IndustrialScrapy.items import ProjectDeclareItem


class NetofthingsSpider(scrapy.Spider):
    name = 'netofthings'
    allowed_domains = ['netofthings']
    keys = ['工业互联网', '工业物联网', '工业4.0', '智慧工厂', '智能制造2025']
    url = 'http://www.netofthings.cn/search.aspx?keyword={keyword}&where=title'

    def start_requests(self):
        for key in self.keys:
            yield scrapy.Request(url=self.url.format(keyword=key),
                                 callback=lambda response, key=key: self.get_page(response, key))

    def get_page(self, response, key):
        selects = response.xpath('//div[@class="pager"]/ul/li[1]/text()')
        if len(selects) == 0:
            return
        pages = int(selects.extract()[0].split('/')[-1])
        for page in range(pages):
            if pages == 1:
                url = self.url.format(keyword=key)
            else:
                url = self.url + '&page={page}'.format(keyword=key, page=page + 1)
            self.logger.info(url)
            yield scrapy.Request(url=url,
                                 callback=lambda inter_response, key=key: self.parse(inter_response, key),
                                 dont_filter=True
                                 )

    def parse(self, response, key):
        for _ in response.xpath('//div[@class="mm"]/div[@class="sResult"]'):
            item_datetime = datetime.strptime(_.xpath('//div[@class="foot"]/span/text()').extract()[-1].strip(),
                                              '%Y/%m/%d %H:%M:%S')
            if abs((datetime.utcnow() - item_datetime).days) > 180:
                return
            item = ProjectDeclareItem()
            item['name'] = _.xpath('//div[@class="sum"]/text()').extract()[0].strip()
            item['url'] = _.xpath('//div[@class="foot"]/span/text()').extract()[0].strip()
            item['date'] = item_datetime
            item['origin'] = self.name
            item['keyword'] = key
            yield item
