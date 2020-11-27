import requests
import re
import urllib.request

def getHtml(url):
    html=urllib.request.urlopen(url).read()
    return html

def getImg(html):
    r=r'"thumbURL":"(https://.+?\.jpg)"'  #定义正则
    imglist = re.findall(r, html)
    return imglist

def download(keyword):
    keyword_2 = keyword.replace(" ", "+")+'+city'
    html=str(getHtml("https://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=&st=-1&fm=result&fr=&sf=1&fmq=1606460438465_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1606460438466%5E00_1903X937&sid=&word="+keyword_2))
    url = getImg(html)[0]
    print(url)
    path = 'C:\\Users\\Catherine Chen\\Dropbox\\Brandeis\\FALL 2020\\Python\\Web Application - Flight Analysis\\graph\\%s.jpg' % keyword
    html_2 = requests.get(url)
    with open(path, 'wb') as file:
        file.write(html_2.content)
    print(keyword,"downloaded")