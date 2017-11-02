# -*- coding: utf-8 -*-

from ArticleSpider.zheye import zheye


z = zheye()
positions = z.Recognize('captcha_cn.gif')
print(positions)