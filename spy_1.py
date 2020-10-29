import sys
# <class 'tuple'>: (<class 'SyntaxError'>, SyntaxError("(unicode error) 'unicodeescape' codec can't decode bytes in position 2-3:
# truncated \\UXXXXXXXX escape", ('D:/MyUni/知来者之可追/oTo/python/spy/spy_1.py', 2, 16,
# "sys.path.append('C:\\Users\\ASUS\\AppData\\Local\\Programs\\Python\\Python37')\n")), <traceback object at 0x00000178C21021C8>)
sys.path.append('C:\\Users\\ASUS\\AppData\\Local\\Programs\\Python\\Python37')
import json
import requests
from bs4 import BeautifulSoup

def get_page(page):
    url_temp = 'http://temp.163.com/special/00804KVA/cm_guonei_0{}.js'
    return_list = []
    for i in range(page):
        url = url_temp.format(i)
        response = requests.get(url)
        if response.status_code != 200:
            continue
        content = response.text
        _content = formatContent(content)
        result = json.loads(_content)
        return_list.append(result)
    return return_list

def get_content(url):
    source = ''
    author = ''
    body = ''
    resp = requests.get(url)
    if resp.status_code == 200:
        body = resp.text
        bs4 = BeautifulSoup(body)
        source = bs4.find('a',id='ne_article_source').get_text()
        author = bs4.find('span',class_='ep-editor').get_text()
        body = bs4.find('div',class_='post_text').get_text()
    return source,author,body
