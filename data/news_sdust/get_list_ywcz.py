# 要闻传真的获取
# 该文件只能获得要闻的数据即 ： news.sdust.edu.cn/ywcz/
# 数据格式: [[202,3,title_str,date_datetime,url_str]]
# 数据样例: [[202, 3, '学校获评全国“ 四星易班工作站”', datetime.datetime(2022, 12, 6, 0, 0), 'http://www.sdust.edu.cn/info/1034/15628.htm'],[202,3,'balabal',...]]

import requests #pip install requests
from bs4 import BeautifulSoup #pip install bs4
from fake_useragent import UserAgent  #pip install fake-useragent
import re #模糊匹配
import urllib #自动补全网址
import datetime

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
      ls_res=[]
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
        # print(str1)
        ls_res.append([202,3,title_str,date_str,url_str])
      return ls_res
      break#退出尝试循环
    except Exception as e:
      print([501,'[dayi-err]python error:{},unknown'.format(str(e))])
      attempt+=1
      pass
  return None





f=open("debug_test.txt","w",encoding="utf-8")

def get_other_pages():
  res_ls = []
  for i in range(pages_cnt):
    exect_num = pages_cnt-i-1

    url = 'http://news.sdust.edu.cn/ywcz/{}.htm'.format(exect_num)
    # url2 = 'https://www.sdust.edu.cn/sylm/kdyw/{}.htm'.format(i)
    print("------第{}页_start-------".format(exect_num))
    f.write("------第{}页_start-------\n".format(exect_num))

    ls = get_news(url)
    if ls!=None:
      for j in ls:
        out_text = "{title_str} {date_str} {url}\n".format(title_str=j[2],date_str=j[3],url=j[4])
        f.write(out_text)
        publish_time =j[3] #2022-12-15
        publish_time_ls = re.findall(r"\d+\.?\d*",publish_time) #解析为[2022,12,15]
        publish_time_dt = datetime.datetime(year=int(publish_time_ls[0]),month=int(publish_time_ls[1]),day=int(publish_time_ls[2])) #修改为datetime
        j[3]=publish_time_dt #返回值重新修改
        res_ls.append(j)
        
    f.write("------第{}页_end-------\n".format(exect_num))
    print("------第{}页_end-------".format(exect_num))
  return res_ls

# 首页
def get_first_page():
  url_first = 'https://news.sdust.edu.cn/ywcz.htm' #第一页
  
  res_ls = [] #返回主要的数据
  
  # print("------第首页_start-------")
  f.write("------第首页_start-------\n")
  
  ls = get_news(url_first)
  if ls!=None:
    for j in ls:
      out_text = "{title_str} {date_str} {url}\n".format(title_str=j[2],date_str=j[3],url=j[4])
      
      publish_time =j[3] #2022-12-15
      publish_time_ls = re.findall(r"\d+\.?\d*",publish_time) #解析为[2022,12,15]
      publish_time_dt = datetime.datetime(year=int(publish_time_ls[0]),month=int(publish_time_ls[1]),day=int(publish_time_ls[2])) #修改为datetime
      j[3]=publish_time_dt #返回值重新修改
      
      res_ls.append(j) #保存数据
      f.write(out_text)
  f.write("------第首页_end-------\n")
  # print("------第首页_end-------")
  return res_ls 

pages_cnt = 10086 #总页数 

# get_first_page()
# print(get_other_pages())

# 要闻传真列表的全部获得
def get_all_news():
  global pages_cnt #设置全局变量
  pages_cnt = get_pages() #获得总页数
  ls_ans = []
  ls_first = get_first_page()
  ls_other = get_other_pages()
  ls_all = ls_first+ls_other
  print(ls_all)
  return ls_all

f = open('ls-all-list.debug','w',encoding='utf-8') #调试文件重定向
# ff=open('ls-all.debug','w',encoding='utf-8')
# ff.write(str(get_all_news()))
# ff.close()


# get_all_news()