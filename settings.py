# Scrapy settings for stock project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'stock'

SPIDER_MODULES = ['stock.spiders']
NEWSPIDER_MODULE = 'stock.spiders'
# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
HEADER = {'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'em_hq_fls=js; qgqp_b_id=83c9bf40f67ef9ed017efa01d17b0eb0; st_si=55741315349612; cowCookie=true; cowminicookie=true; _qddaz=QD.76in2e.se9ao3.kp5da427; intellpositionL=80%25; intellpositionT=1409px; st_asi=delete; HAList=a-sh-600000-%u6D66%u53D1%u94F6%u884C%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-601377-%u5174%u4E1A%u8BC1%u5238%2Ca-sh-601963-%u91CD%u5E86%u94F6%u884C%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570; _adsame_fullscreen_18009=1; st_pvi=42542456286991; st_sp=2021-05-26%2000%3A06%3A03; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Fs; st_sn=159; st_psi=20210527145421304-117001313005-1785166592',
'Host': 'guba.eastmoney.com',
'Upgrade-Insecure-Requests': 1,
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}
MYSQL_HOST = 'localhost'#'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '123'  # 密码请写自己的
MYSQL_DB = 'test'  # 数据库也请写自己的

DOWNLOAD_DELAY = 2
ITEM_PIPELINES = {
    'stock.pipelines.StockPipeline': 200,
}

# ip代理池
# IPPOOL=[
#     {"ipaddr":"114.233.189.60:9999"},
#     {"ipaddr":"182.87.136.50:9999"},
#     {"ipaddr":"27.152.192.225:8888"},
#     {"ipaddr":"223.243.245.33:9999"},
#     # {"ipaddr":"49.70.151.25:3256"},
#     # {"ipaddr":"114.101.251.91:9999"},
#     # {"ipaddr":"120.222.17.151:3128"},
#     # {"ipaddr":"101.133.216.135:80"},
#     # {"ipaddr":"211.144.213.145:80"},
#     # {"ipaddr":"112.64.233.130:9991"},
#     # {"ipaddr":"58.247.127.145:53281"},
#     # {"ipaddr":"183.195.106.118:8118"}
# ]
# # 下载中间件
DOWNLOADER_MIDDLEWARES = {
   #'qianmu.middlewares.MyCustomDownloaderMiddleware': 543,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':123,
    'stock.middlewares.SeleniumStockDownloaderMiddleware':543
    # 'stock.middlewares.IPPOOLS':125
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stock (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'stock.middlewares.StockSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'stock.middlewares.StockDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'stock.pipelines.StockPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
