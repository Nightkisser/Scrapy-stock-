import scrapy,time
from stock.items import StockItem
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions

class StockSpider(scrapy.Spider):
    name = 'stock'
    # 允许爬取的域名
    allowed_domains = ['quote.eastmoney.com']
    # 爬虫的起始网页
    start_urls = ['http://quote.eastmoney.com/center/gridlist.html#sh_hk_board']

    def __init__(self):
        # 因为东方财富网行情表为相同网站下爬取不同页的数据
        # 定义网站页码变量
        self.page = 0
        self.max_page = 30
        self.name = ''
        self.nm=''
        super(StockSpider, self).__init__(name='stock')
        # option = ChromeOptions()
        # option.headless = True
        chrome = '/home/zcreset/Scrapy/爬虫/chromedriver'
        self.driver = webdriver.Chrome(executable_path=chrome)


    def start_requests(self):
        # f = open('/home/zcreset/Scrapy/爬虫/stock/stock/share.txt','r')
        # text = f.read()
        # url_list = re.findall('http:.+\.html',text)
        url_list = ["http://quote.eastmoney.com/center/gridlist.html#sh_hk_board",
                    "http://quote.eastmoney.com/center/gridlist.html#sz_hk_board"]
        for url in url_list:
            self.page = 1
            self.name = url.split('#')[-1][:2]
            self.driver.get(url)
            yield scrapy.Request(url, callback=self.parse)
            # while self.page <= self.max_page:
            #     try:
            #         self.page += 1
            #         self.driver.find_element_by_class_name('next').click()
            #         WebDriverWait(self.driver, 10)  # 浏览器等待10s
            #         yield scrapy.Request(url, callback=self.parse, meta={
            #             'page': self.page,
            #         })#,dont_filter=True)
            #     except:
            #         continue
            # yield scrapy.Request(url, callback=self.parse)

    #Parse(StockSpider类中的函数)
    # def parse(self, response):
    #     # 循环获取列表中a标签的链接信息
    #     urls = response.xpath('//*[@class="ngbglistdiv"]/ul/li')
    #     for href in urls:
    #         try:
    #             # 通过正则表达式获取链接中想要的信息
    #             stock_name = href.xpath('./a/text()').extract()[0]
    #             stock_url = href.css('a::attr(href)').extract()[0]
    #             # 生成百度股票对应的链接信息
    #             url = 'http://guba.eastmoney.com/' + stock_url
    #             # content = {}
    #             # content[stock_name] = url
    #             f = open('share.txt','a')
    #             f.write(str({stock_name:url})+"\n")
    #             f.close()
    #             # yield是生成器
    #             # 将新的URL重新提交到scrapy框架
    #             # callback给出了处理这个响应的处理函数为parse_stock
    #             yield scrapy.Request(url, callback=self.parse_stock,headers=settings.HEADER)
    #         except:
    #             continue

    # 定义如何存百度的单个页面中提取信息的方法
    def parse(self, response):

        # con = response.xpath('//*[@id="stockhqh"]')
        # info = response.xpath('//*[@id="stockheader"]')
        # 因为每个页面返回 的是一个字典类型，所以定义一个空字典
        # content_list = response.xpath('//*[@id="table_wrapper-table"]/tbody/tr')
        Item = StockItem()
        if self.name == 'sh':
            self.max_page = 30
            self.nm = '沪股通'
        elif self.name == 'sz':
            self.max_page = 45
            self.nm = '深股通'

        while self.page <= self.max_page:
            content_list = self.driver.find_elements_by_xpath('//*[@id="table_wrapper-table"]/tbody/tr')
            for content in content_list:
                Item['stock_id'] = content.find_element_by_xpath('./td[2]/a').text
                Item['stock_name'] = content.find_element_by_xpath('./td[3]/a').text

                Item['cur_value'] = content.find_element_by_xpath('./td[5]/span').text
                Item['change_value'] = content.find_element_by_xpath('./td[6]/span').text
                Item['change_rate'] = content.find_element_by_xpath('./td[7]/span').text
                Item['deal_num'] = content.find_element_by_xpath('./td[8]').text
                Item['deal_rate'] = content.find_element_by_xpath('./td[10]').text
                Item['deal_money'] = content.find_element_by_xpath('./td[9]').text
                    # Item['trans_money'] = content.xpath('./tbody/tr[1]/td[9]/text()').extract()[0]
                Item['trans_rate'] = content.find_element_by_xpath('./td[15]').text
                Item['market_sale'] = content.find_element_by_xpath('./td[16]').text
                Item['market_rate'] = content.find_element_by_xpath('./td[17]').text
                Item['stock_loc'] = self.nm
                # Item['stock_id'] = content.xpath('./td[2]/a/text()').extract()[0]
                # Item['stock_name'] = content.xpath('./td[3]/a/text()').extract()[0]
                #
                # Item['cur_value'] = content.xpath('./td[5]/span/text()').extract()[0]
                # Item['change_value'] = content.xpath('./td[6]/span/text()').extract()[0]
                # Item['change_rate'] = content.xpath('./td[7]/span/text()').extract()[0]
                # Item['deal_num'] = content.xpath('./td[8]/text()').extract()[0]
                # Item['deal_rate'] = content.xpath('./td[10]/text()').extract()[0]
                # Item['deal_money'] = content.xpath('./td[9]/text()').extract()[0]
                # #Item['trans_money'] = content.xpath('./tbody/tr[1]/td[9]/text()').extract()[0]
                # Item['trans_rate'] = content.xpath('./td[15]/text()').extract()[0]
                # Item['market_sale'] = content.xpath('./td[16]/text()').extract()[0]
                # Item['market_rate'] = content.xpath('./td[17]/text()').extract()[0]
                yield Item
            self.page += 1
            self.driver.find_element_by_class_name('next').click()
            time.sleep(1)
            yield scrapy.Request(url, callback=self.parse)

        # if self.page < self.max_page:
        #     next_url = "http://quote.eastmoney.com/center/gridlist.html#sh_hk_board"
        #     yield scrapy.Request(next_url,callback=self.parse,meta={
        #         'page': self.page,
        #         },dont_filter=False)



        # Item['stock_id'] = info.css('span a::attr(href)').extract()[0].split(',')[-1][:6]
        # print(Item['stock_id'])
        # Item['stock_name'] = info.xpath('./span[0]/span/a/text()').extract()[0]
        # print(Item['stock_name'])
        # Item['cur_value'] = con.xpath('./span[1]/span[0]/text()').extract()[0]
        # Item['change_value'] = con.xpath('./span[1]/span[1]/text()').extract()[0]
        # Item['change_rate'] = con.xpath('./span[1]/span[2]/text()').extract()[0]
        # Item['deal_num'] = con.xpath('./ul/li[0]/span/text()').extract()[0]
        # Item['deal_rate'] =
        # #Item['deal_money'] = con.xpath('./ul/li[1]/span/text()').extract()[0]
        # Item['trans_money'] = con.xpath('./ul/li[2]/span/text()').extract()[0]
        # Item['trans_rate'] = con.xpath('./ul/li[3]/span/text()').extract()[0]
        # Item['market_value'] = con.xpath('./ul/li[4]/span/text()').extract()[0]
        # 将提取的信息保存到字典中
        #     yield Item

