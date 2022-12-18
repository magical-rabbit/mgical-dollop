import requests
import bs4
from bs4 import BeautifulSoup #pip install bs4
from fake_useragent import UserAgent  #pip install fake-useragent
#pip install lxml
import urllib
import re
import datetime

ua = UserAgent()

def get_click_num(res_num): #获得点击量，如果可以异步就好啦
  url1='http://www.sdust.edu.cn/system/resource/code/news/click/dynclicks.jsp?clickid={click_id}&owner={own}&clicktype=wbnews'.format(click_id=res_num[1],own=res_num[0])
  headers={'User-Agent':ua.random}
  res = requests.get(url1,headers=headers)
  return res.text

def get_title_on_news(url:str):
  headers={'User-Agent':ua.random}
  res = requests.get(url)
  res.encoding = 'utf-8'
  soup = BeautifulSoup(res.text, 'html.parser')
  title = soup.find('p',class_='title')
  publish_time = soup.find('p',class_='time')
  publish_click = publish_time.find('script').get_text()
  
  res_num = re.findall(r"\d+\.?\d*",publish_click) #匹配 _showDynClicks("wbnews", 1470981840, 15717) 中的两个数字
  
  publish_click_num = get_click_num(res_num)
  publish_time_ls = re.findall(r"\d+\.?\d*",publish_time.get_text())
  publish_time_dt = datetime.datetime(year=int(publish_time_ls[0]),month=int(publish_time_ls[1]),day=int(publish_time_ls[2]))
  
  print("标题:{} 时间:{} 点击量:{}".format(title.get_text(),publish_time_dt.strftime("%Y-%m-%d"),publish_click_num))
  
get_title_on_news(url='http://www.sdust.edu.cn/info/1034/15717.htm')