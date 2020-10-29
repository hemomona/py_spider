# a='python'
# b=a[::-1]
# print(b) #nohtyp
# c=a[::-2]
# print(c) #nhy
# #从后往前数的话，最后一个位置为-1
# d=a[:-1]  #从位置0到位置-1之前的数
# print(d)  #pytho
# e=a[:-2]  #从位置0到位置-2之前的数
# print(e)  #pyth
# b = a[i:j]   # 表示复制a[i]到a[j-1]，以生成新的list对象
#
# a = [0,1,2,3,4,5,6,7,8,9]
# b = a[1:3]   # [1,2]
#
# # 当i缺省时，默认为0，即 a[:3]相当于 a[0:3]
# # 当j缺省时，默认为len(alist), 即a[1:]相当于a[1:10]
# # 当i,j都缺省时，a[:]就相当于完整复制一份a
#
# b = a[i:j:s]    # 表示：i,j与上面的一样，但s表示步进，缺省为1.
# # 所以a[i:j:1]相当于a[i:j]
#
# # 当s<0时，i缺省时，默认为-1. j缺省时，默认为-len(a)-1
# # 所以a[::-1]相当于 a[-1:-len(a)-1:-1]，也就是从最后一个元素到第一个元素复制一遍，即倒序。

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
    soup = BeautifulSoup(htmlContent, 'html.parser') #第一个参数是匹配内容，第二个参数是采用模块即规则
    div_objs = soup.find_all('div', class_='article-item-box')
    for div_obj in div_objs[1:]:
        title = div_obj.h4.a.get_text().split()[1]
        # print(title.encoding)报'str' object has no attribute 'encoding'
        blogurl = div_obj.h4.a.get('href')
        global bloginfo
        bloginfo.append((title,blogurl))

if __name__ == '__main__':
    blogpage = 2
    bloginfo = []
    for page in range(1,blogpage+1):
        url = "https://blog.csdn.net/King15229085063/article/list/%s" %(page)
        content = get_content(url)
        parser_content(content)
        print("page %d is classified successfully" %(page))
    # r只读，w可写， a追加
    # 清空文件内容f.truncate()仅当以"r+"   "rb+"    "w"   "wb" "wb+"等以可写模式打开的文件才可以执行该功能
    with open('py博客爬取.md', 'w', encoding='utf-8') as f:
        f.truncate()
        for index, info in enumerate(bloginfo[::-1]):
            f.write('blog %d: [%s](%s)\n' %(index+1, info[0], info[1]))
    print("all success")