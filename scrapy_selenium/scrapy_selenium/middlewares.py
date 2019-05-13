# -*- coding: utf-8 -*-
import time

from scrapy.http import HtmlResponse
class ScrapySeleniumSpiderMiddleware(object):
    def process_request(self, request, spider):
        url = request.url
        spider.chrome.get(url)
        time.sleep(3)
        html = spider.chrome.page_source
        return HtmlResponse(url=url,body=html,request=request,encoding='utf-8')