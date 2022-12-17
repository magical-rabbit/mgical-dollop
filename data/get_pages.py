#获得页面的数据
#感谢:https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

url1 = 'https://ta.sdust.edu.cn/info/1025/36630.htm'
url2 = 'http://news.sdust.edu.cn/info/1117/77548.htm'

import requests
import bs4
from bs4 import BeautifulSoup #pip install bs4
from fake_useragent import UserAgent  #pip install fake-useragent
#pip install lxml
import urllib


def fix_url(orgin_url,url_need_fix):#URL自动补全
  #print(fix_url('http://news.sdust.edu.cn/info/1160/77593.htm','/__local/C/CC/6B/A7534B3E2A44181553A7F6B68B8_E99B0979_18B74.jpg'))
  url_str= urllib.parse.urljoin(orgin_url,url_need_fix) #修复url
  return url_str

ua = UserAgent()

def get_pages_only_text(url:str):
  res = requests.get(url)
  headers={'User-Agent':ua.random} #随机生成UA
  res.encoding = 'utf-8'
  soup = BeautifulSoup(res.text, 'html.parser')
  
  news_con = soup.find('div',class_ ='v_news_content')
  
  news_only_text = news_con.get_text().strip()#.replace('\n','')
  
  
  f=open("out.test.txt","w",encoding="utf-8")
  f.write(news_only_text)
  f.close()
  print(news_only_text)

def get_pages(url:str):
  headers={'User-Agent':ua.random} #随机生成UA
  res = requests.get(url,headers=headers)#发送请求
  res.encoding = 'utf-8' #编码格式
  soup = BeautifulSoup(res.text, 'html.parser')

  news_con = soup.find('div',class_ ='v_news_content')
  
  ls = []
  for i in news_con: #图片添加到目录
    if i == '\n': #不优雅的去除多余的内容
      continue
    if i.find("img") !=None: #寻找图片
      img1 = i.find('img')
      img_=img1.attrs['src']
      pic_url = fix_url(url,img_)
      print(pic_url)
    print(i.get_text())
    # print(i)
  

get_pages(url=url1)
