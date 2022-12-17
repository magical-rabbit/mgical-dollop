# 要闻传真的获取
import requests #pip install requests
from bs4 import BeautifulSoup #pip install bs4
from fake_useragent import UserAgent  #pip install fake-useragent
import re #模糊匹配
import urllib #自动补全网址

dayi_debug=1

ua = UserAgent() #生成UA

url = 'http://news.sdust.edu.cn/ywcz.htm'
url_auto = 'http://news.sdust.edu.cn/' #补全用的

def get_pages():
  url1='http://news.sdust.edu.cn/ywcz.htm'
  attempt=0
  headers={'User-Agent':ua.random} #随机生成UA
  res = requests.get(url1,headers=headers)
  res.encoding = 'utf-8'
  soup = BeautifulSoup(res.text, 'html.parser')
  ans = soup.find('div',class_='pb_sys_common pb_sys_normal pb_sys_style1') #找到页码的class
  res = ans.find('span',class_='p_t',text=re.compile("[0-9]/[0-9]")).text.split('/')[1]
  return int(res)

def get_top_news():
  headers={'User-Agent':ua.random} #随机生成UA

  res = requests.get(url,headers=headers) #生成headers
  # res.raise_for_status() #test res get
  res.encoding = 'utf-8'
  soup = BeautifulSoup(res.text, 'html.parser')
  ans = soup.find_all('tr',id=re.compile("line_u4_*"))#模糊匹配line_u4_*
  # print(set(ans))
  # ans = set(ans)
  for i in ans:
    # print("-------------------------")
    t = i.find_all('td')
    title = t[0]
    date  = t[1]
    url  = title.a.attrs['href']
    title_str=t[0].text
    date_str=t[1].text
    url_str = str(url)

    # if re.search("http",url_str)==None: #如果没有找到http，自动补全网址
    import urllib
    url_str=urllib.parse.urljoin(url_auto,url_str)

    str1="{title_str} {date_str} {url}".format(title_str=title_str,date_str=date_str,url=url_str)
    print(str1)
    # print("-------------------------")
  # ans = soup.find('tbody')
  # print(ans)

def get_news(url_org):
  headers={'User-Agent':ua.random} #随机生成UA
  
  if dayi_debug :print("geting url:{}".format(url_org))
  
  attempt = 0
  while attempt<=4:
    try:
      res = requests.get(url_org,headers=headers) #生成headers
      res.encoding = 'utf-8' #设置编码格式
      
      if res.status_code!=200: #如果不是200返回值报错。
        print([401,"[dayi-err]NOT 200 STATUS,but {},retrying...{}".format(res.status_code,attempt)])
        attempt+=1
        continue
      
      #开始解析
      soup = BeautifulSoup(res.text, 'html.parser')
      ans = soup.find_all('tr',id=re.compile("line_u4_*"))#模糊匹配line_u4_*
      for i in ans:
        # print("-------------------------")
        t = i.find_all('td')
        title = t[0]
        date  = t[1]
        url  = title.a.attrs['href']
        title_str=t[0].text
        date_str=t[1].text
        url_str = str(url)
        
        url_str= urllib.parse.urljoin(url_org,url_str) #修复url
        str1="{title_str} {date_str} {url}".format(title_str=title_str,date_str=date_str,url=url_str)
        print(str1)
      break#退出尝试循环
    except Exception as e:
      print([501,'[dayi-err]python error:{},unknown'.format(str(e))])
      attempt+=1
      pass


pages_cnt = get_pages()
for i in range(pages_cnt):
  url = 'http://news.sdust.edu.cn/ywcz/{}.htm'.format(i)
  print("------第{}页_start-------".format(i))
  get_news(url)
  print("------第{}页_end-------".format(i))
  
print(get_pages())