#要闻传真，嘿嘿嘿，总算写完了全部的接口了，开整！
#因为几乎所有的接口都已经写了，这里甚至不需要手动进行处理什么东西
import lib.dayi_sqlalchemy as dayidb #导入数据库
db = dayidb.db() #初始化数据库，已经都自动初始化啦
from urllib.parse import urlparse #用这个解析url比较安全

from data.news_sdust import * #爬虫相关的库

f = open('test-out.debug','w',encoding='utf-8') #调试信息的输出

# ----------for debug quickly-----------#
#写入对象到内存
# import sys, shelve #debug
# file = shelve.open("list_news.dat.debug")
# file['debug-list-news']=list_news
# ----------for debug quickly-----------#
def debug_dump(list_news):
  import sys, shelve #debug
  file = shelve.open("list_news.dat.debug")
  data_key = 'data-key-ovo'
  file[data_key]=list_news
  file.close()

def debug_load():
  import sys, shelve #debug
  file = shelve.open("list_news.dat.debug")
  data_key = 'data-key-ovo'
  return file[data_key]


cnt_pages = -1

def do_something(i):
  global cnt_pages
  now_url = i[4]
  now_title = i[2]
  now_datetime = i[3]
  # print(now_url)
  list_page_only_text = get_pages_only_text(now_url) # [202, 2, 'text', '12月15日']
  list_page_only_text_str = get_pages_only_text(now_url)[3]
  now_click_num = get_title_on_news(now_url)[4]  #[202, 3, '校党委理论', datetime.datetime(2022, 12, 16, 0, 0), '844']
  list_pics = get_pages_pic(now_url)
  for j in list_pics: #[202, 2, 'pic', 'https://ta.sdust.edu.cn/__local/2/D9/3D/B62E635229FAD159BD3B74F8CA6_EFF684AB_2BB65.jpg'
    pic_url = j[3] 
    pic_uuid = db.insert_pic_db(pic_url)
    _,media_type=os.path.splitext(urlparse(pic_url).path)
    rr = get_and_download(pic_url,'./data/news_sdust/data/pic/'+now_datetime.strftime("%Y/%m/"),'{}{}'.format(pic_uuid,media_type))
    if rr[0]!=201:
      print(rr)

  db.insert_content_db(now_title, now_datetime, now_click_num, list_page_only_text_str, now_url)

def do_something_protect(i):
  # print('完成下载:{} 点击率:{} {now_cnt}/{all_cnt}'.format(now_title,now_click_num,now_cnt=cnt_now,all_cnt=cnt_pages))
  att=0
  while att<=10:
    try:
      do_something(i)
      break
    except Exception as e:
      print('[dayi-error]未知错误 e:{} retrying:{}/10'.format(str(e),att))
      att+=1  
  return 


def rec_now_line(cnt_now):#断点续传
  file_now_line=open('now_line_data.debug','w')
  file_now_line.write(str(cnt_now))
  file_now_line.close()
  return int(cnt_now)
def get_now_line():
  file_now_line=open('now_line_data.debug','r')
  cnt = int(file_now_line.read())
  file_now_line.close()
  return cnt


from sqlalchemy import create_engine



def main():
  list_news = get_all_news()
  # list_news = debug_load() #从缓存文件中读入

  f.write(str(list_news)) 
  debug_dump(list_news)

  global cnt_pages
  cnt_pages =len(list_news)
  cnt_now_last = get_now_line()#断点续传
  cnt_now=0

  from multiprocessing import Pool
  

    # return list(pbar(pool.imap(do_something_protect,list_news)))
  # do_something(list_news[1])

  from multiprocessing.dummy import Pool
  pool=Pool(32)
  text_list=pool.map(do_something_protect#进行多线程的目标函数名，没有()
                   ,list_news#传入数据的列表
                   )

  # for i in list_news: # i = [202, 3, '校党委理论学习中心组开展2022集体学习(new)', datetime.d0, 'https://www.sdust.htm']
  #   if cnt_now<=cnt_now_last:
  #     print('[dayi-info]skiping:{}'.format(i))
  #     cnt_now+=1
  #     continue
  #   att=0
  #   while att<=5:
  #     try:
  #       do_something(i,cnt_now)
  #       db.commit_db()
  #       cnt_now+=1
  #       rec_now_line(cnt_now)
  #       break
  #     except Exception as e:
  #       print('[dayi-error]未知错误 e:{} att:{}'.format(str(e),att))
  #     att+=1  
  return

main()
db.commit_db()