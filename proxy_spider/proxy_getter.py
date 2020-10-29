from proxy_spider.proxy_crawler import Crawler
from proxy_spider.proxy_setting import *
from proxy_spider.proxy_db import MysqlClient
import sys

class Getter():
    def __init__(self):
        self.mysql = MysqlClient()
        self.crawler = Crawler()

    # 判断数量是否足够
    def is_over_threshold(self):
        return self.mysql.count() >= POOL_UPPER_THRESHOLD

    def run(self):
        print('获取器开始执行...')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                all_ip = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for ip in all_ip:
                    self.mysql.addIP(ip)

if __name__ == '__main__':
    proc = Getter()
    proc.run()