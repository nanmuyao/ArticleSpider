# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
import time
import random

from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader

from ArticleSpider.utils.common import get_md5
from selenium import webdriver
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["python.jobbole.com"]
    start_urls = ['http://python.jobbole.com/all-posts/']

    def __init__(self, **kwargs):
        self.browser = webdriver.Chrome(executable_path="D:\workspace_p\pythondoc\chromedriver.exe")
        super(JobboleSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        """

        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        random_time = random.randint(2, 5)
        print("random_time", random_time)
        time.sleep(random_time)

        #提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()

        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        print(response.css(".entry-header h1::text").extract()[0])
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()

        yield article_item