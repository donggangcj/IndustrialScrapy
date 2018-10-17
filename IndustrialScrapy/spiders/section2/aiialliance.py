# -*- coding: utf-8 -*-
import scrapy

from IndustrialScrapy.items import ProjectDeclareItem


class AiiAllianceSpider(scrapy.Spider):
    name = 'aii-alliance'

    def start_requests(self):
        url = 'http://www.aii-alliance.org/index.php?m=content&c=search&a=search'
        myFormData = {'search': '项目申报'}
        yield scrapy.FormRequest(url=url, formdata=myFormData, callback=self.parse)

    def parse(self, response):
        for _ in response.css('ul.download_list li'):
            item = ProjectDeclareItem()
            item['name'] = _.css('h2::text').extract_first()
            item['url'] = _.css('a::attr(href)').extract_first()
            item['date'] = _.css('div.download_list_time::text').extract_first()
            yield item
        try:
            next_page = response.css('#pages a.a1').extract()[-1]
            if next_page:
                yield response.follow(next_page, callback=self.parse)
        except Exception as e:
            # Scrapy provides a logger within each Spider instance
            self.logger.warning('There is not next page:{}'.format(e))
