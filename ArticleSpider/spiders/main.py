from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
# execute(["scrapy", "crawl", "zhihu"])
# execute(["scrapy", "crawl", "lagou"])
# execute(["scrapy", "crawl", "lagouSpider_2"])
execute(["scrapy", "crawl", "weibo_nba"])
