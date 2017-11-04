# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from ArticleSpider.items import HupuItem
import json
import time
from scrapy.selector import Selector


class WeiboNbaSpider(scrapy.Spider):
    name = 'weibo_nba'
    allowed_domains = ['www.weibo.com']
    start_urls = ['http://weibo.com/hoopchina?refer_flag=1001030102_&is_all=1']
    cookie = None
    def __init__(self, **kwargs):
        try:
            with open('fileTest.json') as json_file:
                self.cookie = json.load(json_file)
        except IOError:
            print("Error: 没有找到文件或读取文件失败")

        self.browser = webdriver.Chrome(executable_path="D:\workspace_p\pythondoc\chromedriver.exe")
        super(WeiboNbaSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        # self.browser.quit()
        pass

    def parse(self, response):
        for i in range(3):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(3)
        t_selector = Selector(text=self.browser.page_source)
        print(t_selector.extract())

        print(response.text)

        article_item = HupuItem()
        pass
