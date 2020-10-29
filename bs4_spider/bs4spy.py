# >>>import re
# >>> pattern = re.compile(r'([a-z]+) ([a-z]+)', re.I)   # re.I 表示忽略大小写
# >>> m = pattern.match('Hello World Wide Web')
# >>> print m                               # 匹配成功，返回一个 Match 对象
# <_sre.SRE_Match object at 0x10bea83e8>
# >>> m.group(0)                            # 返回匹配成功的整个子串
# 'Hello World'
# >>> m.span(0)                             # 返回匹配成功的整个子串的索引
# (0, 11)
# >>> m.group(1)                            # 返回第一个分组匹配成功的子串
# 'Hello'
# >>> m.span(1)                             # 返回第一个分组匹配成功的子串的索引
# (0, 5)
# >>> m.group(2)                            # 返回第二个分组匹配成功的子串
# 'World'
# >>> m.span(2)                             # 返回第二个分组匹配成功的子串的索引
# (6, 11)
# >>> m.groups()                            # 等价于 (m.group(1), m.group(2), ...)
# ('Hello', 'World')
# >>> m.group(3)                            # 不存在第三个分组
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# IndexError: no such group

# r'(.*) are (.*?) .*'
# 解析:
#
# 首先，这是一个字符串，前面的一个 r 表示字符串为非转义的原始字符串，让编译器忽略反斜杠，也就是忽略转义字符。但是这个字符串里没有反斜杠，所以这个 r 可有可无。
#  (.*) 第一个匹配分组，.* 代表匹配除换行符之外的所有字符。
#  (.*?) 第二个匹配分组，.*? 后面多个问号，代表非贪婪模式，也就是说只匹配符合条件的最少字符
#  后面的一个 .* 没有括号包围，所以不是分组，匹配效果和第一个一样，但是不计入匹配结果中。
# matchObj.group() 等同于 matchObj.group(0)，表示匹配到的完整文本字符
# matchObj.group(1) 得到第一组匹配结果，也就是(.*)匹配到的
# matchObj.group(2) 得到第二组匹配结果，也就是(.*?)匹配到的
# 因为只有匹配结果中只有两组，所以如果填 3 时会报错。

# import re
# s = '1102231990xxxxxxxx'
# res = re.search('(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{4})',s)
# print(res.groupdict()) #直接将匹配结果直接转为字典模式，方便使用。

import requests
from bs4 import BeautifulSoup

def get_content(url):
    try:
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
        response = requests.get(url, headers={'User-Agent': user_agent})
        response.raise_for_status() #返回状态吗不是200则异常
        response.encoding = response.apparent_encoding
    except Exception:
        print('error')
    else:
        print(response.url)
        print('link success')
        return response.content

def parser_content(htmlContent):
    # 其后加.encode('utf-8')报bytes' object has no attribute 'head'
    soup = BeautifulSoup(htmlContent, 'html.parser') #第一个参数是匹配内容，第二个参数是采用模块即规则
    head_obj = soup.head
    # class是python的保留关键字，若要匹配标签内class的属性，需要特殊的方法，有以下两种：
    # 在attrs属性用字典的方式进行参数传递 soup.find(attrs={'class':'item-1'})
    # BeautifulSoup自带的特别关键字class_ soup.find(class_ = 'item-1')

    # div_obj = soup.find_all('div', class_="blog-content-box")[0] #csdn爬取内容
    div_obj = soup.find_all('div', class_="reader-page ssr")[0] #baidu爬取内容

    with open('百度文库爬取test.html', 'w', encoding="utf-8") as f:
        # 其后加.encode('utf-8')报write() argument must be str, not bytes
        f.write(str(head_obj))
        f.write(str(div_obj))
        print("download success")

if __name__ == '__main__':
    # url = "https://blog.csdn.net/qq_43194257/article/details/87361164"
    url = "https://wenku.baidu.com/view/572b54790640be1e650e52ea551810a6f524c8f4.html"
    content = get_content(url)
    parser_content(content)
