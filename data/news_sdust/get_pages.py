#获得页面的数据
#感谢:https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
#接口说明: 仅获取内容信息，因为部分内容还没有写，也就是说，目前部分只可以获得纯文字内容
#接口1调用: def get_pages_only_text(url:str):  url 为网址内容 (返回的只有文字内容)
#接口1返回: return [202,2,'text',news_only_text] （范围的类型如下）
#接口2调用: def get_pages_pic(url:str): 
#接口2返回: [[202, 2, 'pic', 'https://ta.sdust.edu.cn/__local/2/D9/3D/B62E635229FAD159BD3B74F8CA6_EFF684AB_2BB65.jpg', 'https://ta.sdust.edu.cn/info/1025/36630.htm']]
#如果接口返回502，说明出现了问题

# url1 = 'https://ta.sdust.edu.cn/info/1025/36630.htm'
# url2 = 'http://news.sdust.edu.cn/info/1117/77548.htm'

import requests
import bs4
from bs4 import BeautifulSoup #pip install bs4
from fake_useragent import UserAgent  #pip install fake-useragent
#pip install lxml
import urllib


#
# import sys
# sys.path.append("../../") #for debug
# import lib.dayi_sqlite as dayidb
# db = dayidb.db()




def fix_url(orgin_url,url_need_fix):#URL自动补全
  #print(fix_url('http://news.sdust.edu.cn/info/1160/77593.htm','/__local/C/CC/6B/A7534B3E2A44181553A7F6B68B8_E99B0979_18B74.jpg'))
  url_str= urllib.parse.urljoin(orgin_url,url_need_fix) #修复url
  return url_str

ua = UserAgent()

def get_pages_only_text(url:str):
  try:
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
    return [202,2,'text',news_only_text]
  except Exception as e:
    return [501,'[dayi-error]获得文字信息出现错误:{} url:{}'.format(str(e),url)]
  

def get_pages(url:str):
  headers={'User-Agent':ua.random} #随机生成UA
  res = requests.get(url,headers=headers)#发送请求
  res.encoding = 'utf-8' #编码格式
  soup = BeautifulSoup(res.text, 'html.parser')
  news_con = soup.find('div',class_ ='v_news_content')
  # news_title = soup.find('div',class_='d-newsxq-tit').text
  # print("标题:[{}]".format(news_title))
  ls = []
  for i in news_con: #图片添加到目录
    if i == '\n': #不优雅的去除多余的内容
      continue
    if i.find("img") !=None: #寻找图片
      img1 = i.find('img')
      img_=img1.attrs['src']
      pic_url = fix_url(url,img_)
      #db.insert_pic_db(pic_url)
      print(pic_url)
      

    print(i.get_text())
    # print(i)
  
def get_pages_pic_main(url:str):
  ls_res = []
  headers={'User-Agent':ua.random} #随机生成UA
  res = requests.get(url,headers=headers)#发送请求
  res.encoding = 'utf-8' #编码格式
  soup = BeautifulSoup(res.text, 'html.parser')
  news_con = soup.find('div',class_ ='v_news_content')
  
  for i in news_con: #图片添加到目录
    if i == '\n': #不优雅的去除多余的
      continue
    if i.find("img") !=None: #寻找图片
      img1 = i.find('img')
      img_=img1.attrs['src']
      pic_url = fix_url(url,img_) #图片的链接
      from_url = url
      #db.insert_pic_db(pic_url)
      ls_tmp = [202,2,'pic',pic_url,from_url]
      #print(pic_url)
      ls_res.append(ls_tmp)
  return ls_res

def get_pages_pic(url:str):
  att = 0
  while att<=4:
    try:
      return get_pages_pic_main(url)
    except Exception as e:
      dayi_err_info = [501,'[dayi-error]未知错误,获得页面图片时失败:{} 尝试重试次数:{}'.format(str(e),att)]
      print(dayi_err_info)
      att+=1
  return [501,'[dayi-error]未知错误,获得页面图片时失败:{} 尝试重试次数:{}'.format(str(e),att)]
    



# print(get_pages_pic(url=url1))

