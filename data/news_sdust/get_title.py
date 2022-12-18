#获得标题，时间，点击量（主要是点击量）
#接口调用: get_title_on_news(url)
#接口返回: [202,3,title.get_text(),publish_time_dt,publish_click_num]
#接口示例: [202, 3, '校党委理论学习中心组开展2022年第十九次集体学习', datetime.datetime(2022, 12, 16, 0, 0), '844']

import requests
import bs4
from bs4 import BeautifulSoup #pip install bs4
from fake_useragent import UserAgent  #pip install fake-useragent
#pip install lxml
import urllib
import re
import datetime

def get_click_num(res_num): #获得点击量，如果可以异步就好啦
  ua = UserAgent()
  url1='http://www.sdust.edu.cn/system/resource/code/news/click/dynclicks.jsp?clickid={click_id}&owner={own}&clicktype=wbnews'.format(click_id=res_num[1],own=res_num[0])
  headers={'User-Agent':ua.random}
  res = requests.get(url1,headers=headers)
  return res.text

def get_title_on_news_main(url:str):
  ua = UserAgent()
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
  
  return [202,3,title.get_text(),publish_time_dt,publish_click_num]
  
# get_title_on_news(url='http://www.sdust.edu.cn/info/1034/15717.htm')

#错误防止报错
def  get_title_on_news(url:str):
  att = 0
  while att<=4:
    try:
      return  get_title_on_news_main(url)
    except Exception as e:
      dayi_err_info = [501,'[dayi-error]未知错误,获得页面时失败:{} 尝试重试次数:{}'.format(str(e),att)]
      print(dayi_err_info)
      att+=1
  return [501,'[dayi-error]未知错误,获得页面图片时失败 尝试重试次数:{} url:{}'.format(att,url)]
  

print(get_title_on_news('https://www.sdust.edu.cn/info/1034/15737.htm'))