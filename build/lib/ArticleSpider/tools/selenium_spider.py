# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.selector import Selector
import time

browser = webdriver.Chrome(executable_path="D:\workspace_p\pythondoc\chromedriver.exe")

# browser.get("https://www.zhihu.com/#signin")
# time.sleep(15)
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("222222")
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("admin125")
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()

browser.get("https://www.weibo.com/")
time.sleep(15)
# browser.find_element_by_css_selector("#loginname").send_keys("15114626480")
# browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys("111111")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

browser.find_element_by_css_selector("#loginname").send_keys("liyao198705@sina.com")
browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys("da_ge_da")
browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

for i in range(3):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    time.sleep(3)
t_selector = Selector(text=browser.page_source)
print (t_selector.css(".tm-promo-price .tm-price::text").extract())

# browser.quit()
