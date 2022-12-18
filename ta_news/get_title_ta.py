import requests
from bs4 import BeautifulSoup
import datetime

#page获取第n页的标题,发布时间,点击量
#page=2
#if page==1:
#    ur='https://ta.sdust.edu.cn/xwggkx/xqxw.htm'
#else:
#    ur='https://ta.sdust.edu.cn/xwggkx/xqxw/{}.htm'.format(408-page+1)




#获取2022年全部
for i in range(1,18):
    page=i
    if page==1:
        ur='https://ta.sdust.edu.cn/xwggkx/xqxw.htm'
    else:
        ur='https://ta.sdust.edu.cn/xwggkx/xqxw/{}.htm'.format(408-page+1)
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
    if page==1:
        f=open('./data.txt','w')
    else:
        f=open('./data.txt','a')
    for j in range(0,10):
        url=urllist[j]
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46'}
        r=requests.get(url,headers=headers)
        r.encoding='utf-8'
        soup=BeautifulSoup(r.text,'html.parser')
        if page==3 and j==2:
            continue
        #就这一篇文章跟他妈别的文章格格不入，爷他妈不爬你了，tmd。
            title=soup.select('body > div.particulars-text.w-1200 > div.particulars-content > form > p.title')[0].string
            publish=soup.select('body > div.particulars-text.w-1200 > div.particulars-content > form > p.time')[0].string
        else:
            title=soup.select('body > div.TE > div.TE_box1.clearfix > div.TEB1_right > div.TEB1_right_con > div > form > div.d-newsxq-tit > h5')[0].string
            publish=soup.select('body > div.TE > div.TE_box1.clearfix > div.TEB1_right > div.TEB1_right_con > div > form > div.d-newsxq-tit > ul > li:nth-of-type(1) > p')[0].string

        click=soup.select('body > div.TE > div.TE_box1.clearfix > div.TEB1_right > div.TEB1_right_con > div > form > div.d-newsxq-tit > ul > li:nth-of-type(2) > p > span > script')[0].string
        x=click.split()
        clickurl = 'https://ta.sdust.edu.cn/system/resource/code/news/click/dynclicks.jsp?clickid={}&owner={}&clicktype=wbnews'.format(x[2][0:-1], x[1][0:-1])
        res=requests.get(clickurl).text

        print('标题:{}\t{}\t点击量:{}\t'.format(title,publish,res))
        f.write('标题:{}\t{}\t点击量:{}\t\n'.format(title,publish,res))
    f.close()