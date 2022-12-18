#要闻传真，嘿嘿嘿，总算写完了全部的接口了，开整！
#因为几乎所有的接口都已经写了，这里甚至不需要手动进行处理什么东西
import lib.dayi_sqlite as dayidb #导入数据库
db = dayidb.db() #初始化数据库，已经都自动初始化啦

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

async def do_something(i,cnt_now):
  global cnt_pages
  now_url = i[4]
  now_title = i[2]
  now_datetime = i[3]
  # print(now_url)
  list_page_only_text = get_pages_only_text(now_url) # [202, 2, 'text', '12月15日']
  list_page_only_text_str = get_pages_only_text(now_url)[3]
  now_click_num = get_title_on_news(now_url)[4]  #[202, 3, '校党委理论', datetime.datetime(2022, 12, 16, 0, 0), '844']
  db.insert_content_db(now_title, now_datetime, now_click_num, list_page_only_text_str, now_url)
  print('完成下载:{} 点击率:{} {now_cnt}/{all_cnt}'.format(now_title,now_click_num,now_cnt=cnt_now,all_cnt=cnt_pages))
  

def main():
  # list_news = get_all_news()
  list_news = debug_load()

  f.write(str(list_news)) 
  debug_dump(list_news)

  global cnt_pages
  cnt_pages =len(list_news)
  cnt_now=0

  for i in list_news: # i = [202, 3, '校党委理论学习中心组开展2022集体学习(new)', datetime.d0, 'https://www.sdust.htm']
    att=0
    while att<=5:
      try:
        asyncio.run(do_something(i,cnt_now))
        db.commit_db()
        cnt_now+=1
        break
      except Exception as e:
        print('[dayi-error]未知错误 e:{} att:{}'.format(str(e),att))
      att+=1  
  return

main()
db.commit_db()