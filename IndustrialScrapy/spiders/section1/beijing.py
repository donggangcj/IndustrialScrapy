import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from IndustrialScrapy.items import IndustrialItem


class BeijingSpider(CrawlSpider):
    name = 'beijing'
    header = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWe'
                            'bKit/537.36(KHTML, like Gecko) Chrome/6'
                            '3.0.3239.132 Safari/537.36',
              "Content-Type": 'application/x-www-form-urlencoded'}
    area = 'beijing'
    origin = "beijing"
    keys = ['工业互联网', '工业App']
    url = 'http://jxw.beijing.gov.cn:8080/oasearch/front/search.do'
    links = LinkExtractor(restrict_css='div.pagingrf a.fymar')
    rules = [Rule(links, callback='parse_item', follow=True)]

    def start_requests(self):
        for key in self.keys:
            yield scrapy.FormRequest(
                url=self.url,
                headers=self.header,
                formdata={"pageNo": "1", "orderField": "", "orderType": "", "query": key},
                callback=self.parse_item
            )

    # crawl spider :avoiding using 'parse' as callback
    def parse_item(self, response):
        keyword = response.css('div.inform_search input::attr(value)').extract_first()
        for _ in response.css('dl.result_text'):
            item = IndustrialItem()
            item['url'] = _.css('dd a i::text').extract_first()
            item['title'] = ''.join(_.css('dt a i::text,dt a i font::text').extract())
            item['time'] = _.css('dt p::text').extract_first().strip()
            item['area'] = self.origin
            item['nature'] = ''
            item['keyword'] = keyword
            yield item

            # try:
            #     next_page = response.css('div.pagingrf a.fymar')
            #     if next_page:
            #         yield response.follow(next_page, callback=self.parse)
            # except Exception as e:
            #     # FIXME : show the logger's sender class
            #     self.logger.warning('There is no next page:{}'.format(e))
