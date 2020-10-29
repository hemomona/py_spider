from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import re
import sys

#no need code in next line in python2
from importlib import reload

reload(sys)
#default encoding is unicode in python3, detdefaultencoding disappered
#sys.setdefaultencoding("utf-8")
def spider(url):
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    html = requests.get(url,headers=headers)    #伪装为浏览器
    selector = etree.HTML(html.text)
    content = selector.xpath('//figure[@class="post-image"]')   #提取figure标签
    for each in content:
        tmp = each.xpath('a/img/@src')  #提取src属性
        pic = requests.get(tmp[0])
        print('downloading: '+tmp[0])
        string = re.search('\d+/\d+/(.*?)\\.jpg',str(tmp[0])).group(1)  #匹配图片名字
        fp = open('matter\\'+string+'.jpg','wb')
        fp.write(pic.content)
        fp.close()

if __name__ == '__main__':
    pool = ThreadPool(2)    #双核电脑
    tot_page = []
    for i in range(1,5):   #提取1~4页的内容
        link = 'http://hotpics.cc/page/'+str(i)
        tot_page.append(link)
    pool.map(spider,tot_page)
    pool.close()
    pool.join()

