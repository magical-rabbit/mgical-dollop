#Get Data URL:https://2019ncov.chinacdc.cn/JKZX/yq_20221213.json

import requests
import datetime
# from bs4 import BeautifulSoup #pip install bs4
from fake_useragent import UserAgent  #pip install fake-useragent

import json
import os

if not os.path.exists('./data'): #自动建文件夹
  os.mkdir('./data')

d1 = datetime.timedelta(days=1) #天数变化值
date = datetime.datetime(year=2019,month=12,day=20)#日期变量

for i in range(999999):
  str_day=date.strftime("%Y%m%d")
  url_str='https://2019ncov.chinacdc.cn/JKZX/yq_{}.json'.format(str_day)#生成url
  ua = UserAgent()
  headers={'User-Agent':ua.random}
  attempt=0
  file_path = "./data/"+str_day+".json"
  date+=d1#天数加一天
  print(url_str)
  if date>=datetime.datetime.today():
    break
  if os.path.exists(file_path):
    if os.path.getsize(file_path)>=300*1024:
      print([202,"[dayi-info]Found download file,skip it"])
      continue
  
  
  while attempt<=4:
    try:
      res = requests.get(url_str,headers=headers)
      if res.status_code!=200:
        print([401,"[dayi-error]"+str_day+" error:{}".format(attempt)])#未找到资源
      if res.status_code==200:
        f=open(file_path,"w")
        j = json.loads(res.content) #读取json
        f.write(json.dumps(j)) #写入json格式
        f.close()
        break
    except :
      print([501,"[dayi-error]"+str_day+" error:{}".format(attempt)])#程序内部错误，各种原因都可能
      pass
    attempt+=1
  
  


# for i in range()