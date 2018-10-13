# -*- coding: utf-8 -*-
import scrapy
from math import ceil
from urllib.parse import urljoin, urlparse
import re

from IndustrialScrapy.items import IndustrialItem


class AnhuiSpider(scrapy.Spider):
    name = 'anhui'
    area = "anhui"
    origin = "anhui"

    url = 'http://www.aheic.gov.cn/search.jsp'
    base_url = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    formdata = {'keyValue': '工业互联网'.encode('GB2312'), 'keyName': 'strMasTitle'}
    keys = ['工业互联网', '工业App']

    def start_requests(self):
        for key in self.keys:
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.formdata,
                callback=lambda response, key=key: self.get_page(response, key)
            )

    def get_page(self, response, key):
        page_number = int(response.css('div.manu b::text').extract_first())
        for i in range(1, ceil(page_number / 10) + 1):
            self.formdata['PageSizeIndex'] = str(i)
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.formdata,
                callback=lambda response, key=key: self.parse_item(response, key)
            )

    def parse_item(self, response, key):
        for item in response.css('div.nest p'):
            url = urljoin(self.base_url, item.css('a::attr(href)').extract_first())
            yield scrapy.Request(
                url=url,
                callback=lambda response, key=key: self.parse(response, key)
            )

    def parse(self, response, key):
        industrial_item = IndustrialItem()
        industrial_item['title'] = response.css('div.atctitle h1::text').extract_first()
        industrial_item['url'] = response.url
        # TODO learn the python re
        pattern = re.compile(r'.*(\d\d\d\d-\d\d-\d\d)')
        industrial_item['time'] = pattern.match(response.css('div.atctitle h5::text').extract_first()).group(1)
        industrial_item['area'] = self.area
        industrial_item['nature'] = response.xpath('//span[@class="where"]/a[last()]/text()').extract()[0]
        industrial_item['keyword'] = key
        yield industrial_item
