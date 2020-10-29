import time
from multiprocessing import Process
from proxy_spider.proxy_api import app
from proxy_spider.proxy_getter import Getter
from proxy_spider.proxy_tester import Tester
from proxy_spider.proxy_setting import *


class Scheduler():
    # 定时测试代理
    def schedule_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)

    # 定时获取代理
    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)

    # 开启API
    def schedule_api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行...')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()