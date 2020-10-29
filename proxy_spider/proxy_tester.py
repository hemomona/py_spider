# 异步请求库在请求发出之后，程序可以继续接下去执行其他的事情，
# 当响应到达时会通知程序再去处理这个响应，这样程序就没有被阻塞，可以充分把时间和资源利用起来
import asyncio
import aiohttp
import time
import sys
from aiohttp import ClientError
from proxy_spider.proxy_db import MysqlClient
from proxy_spider.proxy_setting import *

class Tester(object):
    def __init__(self):
        self.mysql = MysqlClient()

    async def test_single_ip(self, ip):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(ip, bytes):
                    ip = ip.decode('utf-8')
                real_ip = 'http://' + ip
                print('正在测试 ', ip)
                async with session.get(TEST_URL, proxy=real_ip, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.mysql.maxScore(ip)
                    else:
                        self.mysql.decreaseScore(ip)
            except (ClientError, aiohttp.ClientConnectionError, asyncio.TimeoutError, AttributeError):
                self.mysql.decreaseScore(ip)

    def run(self):
        print('测试器开始执行...')
        try:
            count = self.mysql.count()
            print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i+BATCH_TEST_SIZE, count)
                test_ip_group = self.mysql.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_ip(ip_tuple[0]) for ip_tuple in test_ip_group]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print(e.args)

if __name__ == "__main__":
    test = Tester()
    test.run()