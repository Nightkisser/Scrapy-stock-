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
        self.page = 1
        # 手动定义最大页码，暂时还没有编写从网页自行获取
        self.max_page = 0
        # 爬取网页的列表索引
        self.index = 0
        # 辅助判断沪股还是深股
        self.name = ''
        self.nm = ''
        # 定义标签页的句柄
        self.first_h = None
        # 爬取网页列表
        self.url_list = ["http://quote.eastmoney.com/center/gridlist.html#sh_hk_board",
                    "http://quote.eastmoney.com/center/gridlist.html#sz_hk_board"]

        super(StockSpider, self).__init__(name='stock')
        # 定义模拟浏览器的路径
        chrome = '/home/zcreset/Scrapy/爬虫/chromedriver'
        # 设置无头爬取模式，即后台运行，无界面显示
        # chorme_options = ChromeOptions()
        # chorme_options.add_argument("--headless")
        # chorme_options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(executable_path=chrome,chrome_options=chorme_options)
        
        # 给爬虫设置Chrome浏览器
        self.driver = webdriver.Chrome(executable_path=chrome)

    def start_requests(self):
        url = self.url_list[self.index]
        self.name = url.split('#')[-1][:2]
        self.driver.get(url)
        # 获取当前标签页句柄
        self.first_h = self.driver.current_window_handle
        # 在当前标签页进行爬取请求
        yield scrapy.Request(url, callback=self.parse, dont_filter= True)

    # 定义如何存百度的单个页面中提取信息的方法
    def parse(self, response):
        # 调用字段函数创建数据存储字典
        # 暂时手动是手动记录最大页码
        Item = StockItem()
        # 判断股票归属地
        if self.name == 'sh':
            self.max_page = 30
            self.nm = '沪股通'
        elif self.name == 'sz':
            self.max_page = 45
            self.nm = '深股通'
            
        # 根据页码设定重复切换页码爬取的次数
        while self.page <= self.max_page:
            # 根据网页源码提取需要的信息，使用selenium的元素查找方法
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
                Item['trans_rate'] = content.find_element_by_xpath('./td[15]').text
                Item['market_sale'] = content.find_element_by_xpath('./td[16]').text
                Item['market_rate'] = content.find_element_by_xpath('./td[17]').text
                Item['stock_loc'] = self.nm
                yield Item
            # 页码更新
            self.page += 1
            # 搜索下一页按钮并点击下一页
            self.driver.find_element_by_class_name('next').click()
            # 等待页面加载
            time.sleep(1)
            
        # 定义新建标签页并切换至指定网站的脚本
        js = 'window.open("http://quote.eastmoney.com/center/gridlist.html#sz_hk_board");'
        # 更新网页索引
        self.index += 1
        if self.index < len(self.allowed_domains):
            url = self.url_list[self.index]
            self.name = url.split('#')[-1][:2]
            # 运行脚本
            self.driver.execute_script(js)
            # 获取新建标签页的句柄
            handles = self.driver.window_handles
            h = None
            for handle in handles:
                if handle != self.first_h:
                    h = handle
            # 切换当前标签页
            self.driver.switch_to.window(h)
            # 在新的标签页进行爬取请求
            yield scrapy.Request(url, callback=self.parse)
