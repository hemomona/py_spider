# robots：机器人协议，放在网站的开头，供给爬虫读取，当爬虫读到robots之后，就知道那些是允许爬取的数据，哪些是禁止爬取的数据
# （爬虫道德问题：1.不许过频繁爬取 2.不许爬取禁止内容）
from urllib import request
import requests

if __name__ == '__main__':
    url = "https://jobs.zhaopin.com/CC375882789J00033399409.htm"
    # 有些服务器在实现http协议时可能存在bug, 不支持identify或者请求头中并没有发送Accept - Encoding,
    # 那么服务器倾向于使用http1.0中的"gzip" and "compress"
    # rsp = request.urlopen(url)
    resp = requests.get(url)
    html = str(resp.content, 'utf-8')
    print(html)
