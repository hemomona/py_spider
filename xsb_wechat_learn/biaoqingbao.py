import os
import requests
from time import time
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

class DownloadBiaoqingbao(Thread):
    def __init__(self, queue, path):
        Thread.__init__(self)
        self.queue = queue
        self.path = './biaoqingbao/'
        if not os.path.exists(path):
            os.makedirs(path)

    def run(self):
        while True:
            url = self.queue.get()
            try:
                download_biaoqingbao(url, self.path)
            finally:
                self.queue.task_done()

def download_biaoqingbao(url, path):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    img_list = soup.find_all('img', class_='ui image lazy')
    for img in img_list:
        image = img.get('data-original')
        title = img.get('title')
        print('downloading ', title)
        try:
            with open(path+title+os.path.splitext(image)[-1],'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except OSError:
            print('failed ', title)
            break

if __name__ == '__main__':
    start = time()
    url = 'https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
    urls = [url.format(page=page) for page in range(1, 4)]
    queue = Queue()
    path = './biaoqingbao/'
    # 创建线程
    for x in range(10):
        worker = DownloadBiaoqingbao(queue, path)
        worker.daemon = True
        worker.start()
    # 加入队列
    for url in urls:
        queue.put(url)
    queue.join()
    print('all finished in ', time()-start)
