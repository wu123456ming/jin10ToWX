# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy import signals
import re
class JinshiSpider(scrapy.Spider):
    name = 'jinshi'
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
        print('一次爬取结束-----等待下次循环爬取')

    def parse(self, response):
        contents = response.xpath('//div[@class="jin-flash"]/div[@id="J_flashList"]')
        for content in contents:
            dates = content.xpath('//div[@class="jin-flash"]/div[@id="J_flashList"]//div/@data-id').extract()
            infos = content.xpath('//div[@class="jin-flash"]/div[@id="J_flashList"]//div[@class="jin-flash_b"]').extract()
            date_ids = re.findall(r'<div id="(\d+)" data-id=".*?" class=".*?">', response.text, re.DOTALL)
            for date_id,date,info in zip(date_ids,dates,infos):
                news = {'info':info}
                for neirong in news.values():
                    base_url = 'https:'
                    wenzhanglianjie = '阅读更多'
                    wenzi = re.sub(r'<.*?>', '',neirong).strip().strip('\u200b')
                    wenzi_text = wenzi.replace('\n', '').replace('\t\t\t\t\t\t\t\t\t\t\t\t\t','  ').replace('\t\t\t\t\t\t\t\t\t\t\t','  ').replace('\t\t\t\t\t\t','  ').replace('\t\t\t\t\t\t\t\t','   ').replace('\t\t','')
                    gengduo  = re.compile('<a href="(.*?)" target="_blank" class="jin-flash_text-more1">阅读更多<i class="jin-icon jin-icon_rightArrow"></i></a>')
                    gengduo_url = ''.join(gengduo.findall(neirong))
                    wenzi_href = re.compile('<h4 class="jin-flash_data-title"><a href="(.*?)" target="_blank">.*?</a></h4>')
                    wenzi_href_url = base_url+''.join(wenzi_href.findall(neirong))
                    photo = re.compile('<img class="J_lazyImg" data-original="(.*?)" src=".*?">')
                    photo_url = base_url+''.join(photo.findall(neirong))
                    if wenzi_text.__contains__("【行情】"):
                        yield {'date_id':date_id,'date': date, 'wenzi_text': wenzi_text,'gengduo_url':gengduo_url,'wenzi_href_url':wenzi_href_url,'photo_url':photo_url}
