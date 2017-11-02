# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import LagouArticleItem, ArticleItemLoader
import sys
import time
import random

class Lagouspider2Spider(scrapy.Spider):
    current_page_num = 2
    name = 'lagouSpider_2'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/UIshejishi/']

    def parse(self, response):
        post_nodes = response.css("#s_position_list .item_con_list .list_item_top .p_top a")
        # company_name_job_url = response.css(".company_name ::attr(href)").extract_first("")
        company_name = response.css(".company_name a::text").extract()
        index = 0
        random_time = random.randint(0, 7)
        print("random_time", random_time)
        time.sleep(random_time)
        for post_node in post_nodes:
            article_url = post_node.css("::attr(href)").extract_first("")
            print("image_url:",article_url)
            print("company_name:", company_name[index])

            random_time = random.randint(2, 5)
            print("random_time", random_time)
            time.sleep(random_time)

            yield Request(url=parse.urljoin(response.url, article_url),
                          meta={"job_url": article_url, "company_name": company_name[index]}, callback=self.parse_detail)
            index = index + 1

        # 这里超过30的话爬虫会自动关闭
        # 提取下一页并交给scrapy进行下载
        if self.current_page_num < 31 :
            next_url = "https://www.lagou.com/zhaopin/UIshejishi/{0}/".format(self.current_page_num)
            if next_url:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
                self.current_page_num = self.current_page_num + 1


    def parse_detail(self, response):
        job_url = response.meta.get("job_url", "")  # 文章封面图
        company_name = response.meta.get("company_name", "")  # 文章封面图
        title = response.css(".job-name ::attr(title)").extract()[0]
        print("title", title)
        content1 = response.css(".job_bt p::text").extract()
        content = " ".join(content1)
        print(content)

        job_request = response.css(".job_request span::text").extract()
        job_request = " ".join(job_request)
        print(job_request)

        article_item = LagouArticleItem()
        item_loader = ArticleItemLoader(item=LagouArticleItem(), response=response)
        item_loader.add_css("title", ".job-name ::attr(title)")
        item_loader.add_css("content", ".job_bt p::text")
        item_loader.add_css("job_request", ".job_request span::text")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_value("job_url", job_url)
        item_loader.add_value("company_name", company_name)
        article_item = item_loader.load_item()

        yield article_item