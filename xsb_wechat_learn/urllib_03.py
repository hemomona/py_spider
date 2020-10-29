from urllib import request, parse
import ssl

# response = urllib.request.urlopen('http://www.baidu.com')
# print(response.read().decode('utf-8'))
# 此网站已不能使用
url = 'https://biihu.cc//account/ajax/login_process/'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
dict = {
    'return_url':'https://biihu.cc/',
    'user_name':'xiaoshuaib@gmail.com',
    'password':'123456789',
    '_post_type':'ajax',
}
data = bytes(parse.urlencode(dict), 'utf-8')
req = request.Request(url, data=data, headers={'User-Agent': user_agent}, method='POST')
context = ssl._create_unverified_context()
res = request.urlopen(req, context=context, timeout=10)
print(res.read().decode('utf-8'))
