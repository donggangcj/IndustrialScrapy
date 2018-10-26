# -*- coding: utf-8 -*-
from urllib.parse import urlparse, urljoin
from datetime import datetime
import json

import scrapy
import requests

from IndustrialScrapy.items import IndustrialItem


class ShandongSpider(scrapy.Spider):
    name = 'shandong'
    area = 'shandong'
    origin = 'shandong'
    url = 'http://www.sdeic.gov.cn/gentleCMS/f_articlesearch/getSearchArticleListForNameorContent.do'
    base_url = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    header = header = {'Cache-Control': 'max-age=0', 'Origin': 'http://www.aheic.gov.cn',
                       'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                       'Referer': 'http://www.sheitc.gov.cn/zxgkxx/index.htm',
                       'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                       'Cookie': '_sheitc=jinasgKzas; _gscu_1260451812=302449692ovey868; _gscbrs_1260451812=1; gwideal_date=day; gwdshare_firstime=1530244999495; _gscs_1260451812=t30258567798d7510|pv:12'}

    keyword = ['工业互联网', '工业App']

    def start_requests(self):
        for key in self.keyword:
            res = requests.post(
                url=self.url,
                data={"siteid": "934369d9-7c20-45e0-a919-08ed9d557a1d", "pageIndex": "1", "pageSize": "15", "name": key,
                      "sitePubUrl": "/", "number": "", "time": "", "channelid": ""},
                headers=self.header
            )
            if res.ok:
                page_num = res.json().get('result').get('pagesize')
            for i in range(1, page_num + 1):
                yield scrapy.FormRequest(
                    dont_filter=True,
                    url=self.url,
                    formdata={"siteid": "934369d9-7c20-45e0-a919-08ed9d557a1d", "pageIndex": str(i), "pageSize": "15",
                              "name": key,
                              "sitePubUrl": "/", "number": "", "time": "", "channelid": ""},
                    headers=self.header,
                    callback=lambda response, key=key: self.parse(response, key)
                )

    def parse(self, response, key):
        articlelist = json.loads(response.body).get('result').get('articleList')
        for item in articlelist:
            industrial_item = IndustrialItem()
            industrial_item['title'] = item.get('NAME')
            industrial_item['time'] = datetime.fromtimestamp(int(item.get('PUBDATE')) / 1000)
            industrial_item['area'] = self.area
            industrial_item['url'] = urljoin(self.base_url, item.get('PUBURL'))
            industrial_item['nature'] = item.get('CHANNELNAME')
            industrial_item['keyword'] = key
            yield industrial_item
