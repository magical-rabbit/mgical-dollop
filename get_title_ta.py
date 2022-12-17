import requests
from bs4 import BeautifulSoup
import datetime

#page1获取第一页的新闻
ur='https://ta.sdust.edu.cn/xwggkx/xqxw.htm'
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46'}
r=requests.get(ur,headers=header)
r.encoding='utf-8'
soup=BeautifulSoup(r.text,'html.parser')
urllist=[]
for i in range(0,10):
    pagelist=soup.select('#line_u11_{} > a'.format(i))[0].get('href')
    reurl='https://ta.sdust.edu.cn/{}'.format(pagelist)
    urllist.append(reurl)

#获取标题，发布时间，点击量
for i in range(0,10):
    url=urllist[i]
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46'}
    r=requests.get(url,headers=headers)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'html.parser')
    title=soup.select('body > div.TE > div.TE_box1.clearfix > div.TEB1_right > div.TEB1_right_con > div > form > div.d-newsxq-tit > h5')[0].string
    publish=soup.select('body > div.TE > div.TE_box1.clearfix > div.TEB1_right > div.TEB1_right_con > div > form > div.d-newsxq-tit > ul > li:nth-of-type(1) > p')[0].string

    click=soup.select('body > div.TE > div.TE_box1.clearfix > div.TEB1_right > div.TEB1_right_con > div > form > div.d-newsxq-tit > ul > li:nth-of-type(2) > p > span > script')[0].string
    x=click.split()
    clickurl = 'https://ta.sdust.edu.cn/system/resource/code/news/click/dynclicks.jsp?clickid={}&owner={}&clicktype=wbnews'.format(x[2][0:-1], x[1][0:-1])
    res=requests.get(clickurl).text


    print('标题:{}{}点击量:{}\t'.format(title,publish,res))
