from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
# execute(["scrapy", "crawl", "zhihu"])
# execute(["scrapy", "crawl", "lagou"])
# execute(["scrapy", "crawl", "lagouSpider_2"])
# execute(["scrapy", "crawl", "weibo_nba"]) 这个工程后续用微博第三方开发者平台来拉去数据，不属于爬虫的范畴了，只要能拿到数据就行
execute(["scrapy", "crawl", "lianjiaDL"])

