# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from scrapy.http import HtmlResponse, Response
import time
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
#from stock.settings import IPPOOL
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

# 代理池
# class IPPOOLS(HttpProxyMiddleware):
#     def __init__(self,ip=''):
#         self.ip = ip
#
#     def process_request(self, request, spider):
#         thisip = random.choice(IPPOOL)
#         request.meta["proxy"] = "http://"+thisip["ipaddr"]

class StockSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumStockDownloaderMiddleware:
# class DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
#     option = webdriver.ChromeOptions()
#     # option.add_argument('headless')
#     # prefs = {
#     #     "profile.managed_default_content_settings.images": 2,  # 禁止加载图片
#     #     'permissions.default.stylesheet': 2,  # 禁止加载css
#     # }
#     # option.add_experimental_option("prefs", prefs)
#     self.browser.implicitly_wait(2)
#     self.browser.execute_script('window.open("","_blank");')  # 新建一个标签页
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
#
    def process_request(self, request, spider):
        if spider.name == "stock":
            spider.driver.get(request.url)
            origin_code = spider.driver.page_source
            # 将源代码构造成为一个Response对象，并返回。
            res = HtmlResponse(url=request.url, encoding='utf8', body=origin_code, request=request)

            # if request.meta['page'] <= 30:
            #     print('next')
            #     spider.driver.find_element_by_class_name('next').click()  # get next page
            return res
        # if spider.name == 'bole':
        #     request.cookies = {}
        #     request.headers.setDefault('User-Agent', '')
        return None

    def process_response(self, request, response, spider):
        print(response.url, response.status)
        return response
#


    #
    # def process_request(self, request, spider):
    #     # Called for each request that goes through the downloader
    #     # middleware.
    #
    #     # Must either:
    #     # - return None: continue processing this request
    #     # - or return a Response object
    #     # - or return a Request object
    #     # - or raise IgnoreRequest: process_exception() methods of
    #     #   installed downloader middleware will be called
    #     return None
    #
    # def process_response(self, request, response, spider):
    #     # Called with the response returned from the downloader.
    #
    #     # Must either;
    #     # - return a Response object
    #     # - return a Request object
    #     # - or raise IgnoreRequest
    #     return response
    #
    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
