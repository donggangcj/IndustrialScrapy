# -*- coding: utf-8 -*-
import re
from math import ceil

import scrapy

from IndustrialScrapy.items import IndustrialItem
from ..util import format_return_date


class ShanghaiSpider(scrapy.Spider):
    name = 'shanghai'
    url = 'http://www.sheitc.gov.cn/cms/ArtiSearch.do'
    keys = ['工业互联网', '工业App']
    area = "shanghai"
    origin = "shanghaijingjihexinxihuaweiyuanhui"

    def start_requests(self):
        for key in self.keys:
            yield scrapy.FormRequest(
                dont_filter=True,
                url=self.url,
                formdata={"searchKey": key.encode('GB2312')},
                callback=lambda response, key=key: self.get_page(response, key)
            )

    def get_page(self, response, key):
        pattern = re.compile(r'共(\d+)条记录')
        pages = int(pattern.search(''.join(response.css('div.page::text').extract())).group(1))
        print(pages)
        for i in range(1, ceil(pages / 10) + 1):
            yield scrapy.FormRequest(
                dont_filter=True,
                url='http://www.sheitc.gov.cn/cms/ArtiSearch_{}.do'.format(i),
                formdata={"searchKey": key.encode('GB2312')},
                callback=self.parse_item
            )

    def parse_item(self, response):
        keyword = response.css('div.search_t input::attr(value)').extract_first()
        print(keyword)
        for item in response.css('ul.earch_list li'):
            industrial_item = IndustrialItem()
            industrial_item['title'] = item.css('a::attr(title)').extract_first()
            industrial_item['url'] = item.css('a::attr(href)').extract_first()
            pattern = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})')
            industrial_item['time'] = format_return_date(
                pattern.search(item.css('p::text').extract_first().replace(' ', '')).group())
            industrial_item['nature'] = item.css('p::text').extract_first().replace(' ', '').split('：')[-1].split()[0]
            industrial_item['keyword'] = keyword
            industrial_item['area'] = self.area
            industrial_item['origin'] = self.origin
            yield industrial_item
