# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from ArticleSpider.items import HupuItem

class WeiboNbaSpider(scrapy.Spider):
    name = 'weibo_nba'
    allowed_domains = ['www.weibo.com']
    start_urls = ['http://weibo.com/hoopchina?refer_flag=1001030102_&is_all=1']

    def __init__(self, **kwargs):
        self.browser = webdriver.Chrome(executable_path="D:\workspace_p\pythondoc\chromedriver.exe")
        super(WeiboNbaSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        print(response.text)

        article_item = HupuItem()


        pass
