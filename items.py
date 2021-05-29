# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_id = scrapy.Field()
    stock_name = scrapy.Field()
    cur_value = scrapy.Field()
    change_value = scrapy.Field()
    change_rate = scrapy.Field()
    deal_num = scrapy.Field()
    deal_money = scrapy.Field()
    deal_rate = scrapy.Field()
    trans_rate = scrapy.Field()
    market_sale = scrapy.Field()
    market_rate = scrapy.Field()
    stock_loc = scrapy.Field()

