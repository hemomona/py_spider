#coding=utf-8
# 头部指定编码解决正则表达式中的中文被误认为？问题
import re
import requests
from bs4 import BeautifulSoup
import openpyxl

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
    ol_obj = soup.find_all('ol', class_='grid_view')[0]
    details = ol_obj.find_all('li')
    for detail in details:
        name = detail.find('span', class_='title').get_text()
        href = detail.find('div', class_='hd').a.get('href')
        score = detail.find('span', class_='rating_num').get_text()
        comment_num = str(detail.find(text=re.compile(r'\d+人评价')))
        comment_obj = detail.find('span', class_='inq')
        if comment_obj:
            comment = comment_obj.get_text()
        else:
            comment = "not found"
        # append() takes exactly one argument (4 given)
        movie_info.append((name, href, score, comment_num, comment))

def create_excel(path, data, sheetname='Sheet1'):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = sheetname
    for row, item in enumerate(data):
        for column, cellValue in enumerate(item):
            cell = sheet.cell(row=row+1, column=column+1)
            cell.value = cellValue
    wb.save(path)
    print("write in %s successfully" %path)

if __name__ == '__main__':
    doubanTopPage = 4
    perPage = 25
    movie_info = []
    for page in range(1,doubanTopPage+1):
        url = "https://movie.douban.com/top250?start=%s" %((page-1) * perPage)
        content = get_content(url)
        parser_content(content)
    create_excel("doubanTopMovie.xlsx", movie_info, sheetname="豆瓣电影信息")