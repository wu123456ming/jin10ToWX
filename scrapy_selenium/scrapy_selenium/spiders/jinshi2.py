# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy import signals
from scrapy import Selector
import json
import re
class JinshiSpider(scrapy.Spider):
    name = 'jinshi2'
    allowed_domains = ['jinshi.com']
    start_urls = ['https://www.jin10.com/']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(JinshiSpider, cls).from_crawler(crawler, *args, **kwargs)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        spider.chrome = webdriver.Chrome(chrome_options=options)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.chrome.quit()
        print('爬虫结束了--------------------')

    def parse(self, response):
        contents = response.xpath('//div[@class="jin-flash"]/div[@id="J_flashList"]')
        for content in contents:
            id = re.findall(r'<div id="(\d+)" data-id=".*?" class=".*?">',response.text,re.DOTALL)
            dates = content.xpath('//div[@class="jin-flash"]/div[@id="J_flashList"]//div/@data-id').extract()
            infos = content.xpath('//div[@class="jin-flash"]/div[@id="J_flashList"]//div[@class="jin-flash_b"]').extract()
            for date, info in zip(dates, infos):
                tt =  {
                    'date': date,
                    'info': info
                }
                print(id)


