# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import sys,datetime
sys.path.append(".")
import settings

class StockPipeline:
    def __init__(self):
        self.con = pymysql.connect(
            host=settings.MYSQL_HOST,  # host为数据库所在服务的ip地址
            port=settings.MYSQL_PORT,  # 端口号
            user=settings.MYSQL_USER,  # 用户名
            passwd=settings.MYSQL_PASSWD,  # 密码
            db=settings.MYSQL_DB,  # 数据库名
            charset='utf8',  # 编码格式，一定要写这个，否则会出现乱码
        )
        self.cursor = self.con.cursor()

    def process_item(self, item, spider):
        sql = "insert into stocks values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,curdate())"
        self.cursor.execute(sql,(item['stock_id'],item['stock_name'],item['cur_value'],item['change_value'],item['change_rate'],
                                 item['deal_num'],item['deal_money'],item['deal_rate'],item['trans_rate'],item['market_sale'],
                                 item['market_rate'],item['stock_loc']))
        self.con.commit()
        return item

    def close_spider(self,spider):
        filename = str(datetime.date.today()) + '.txt'
        path = '/home/zcreset/Mysql学习/爬虫数据/Stock/' + filename
        sql = "select * from stocks into outfile %s"
        self.cursor.execute(sql,path)
        self.cursor.close()
        self.con.close()