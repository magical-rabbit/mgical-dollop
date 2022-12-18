#要闻传真，嘿嘿嘿，总算写完了全部的接口了，开整！
#因为几乎所有的接口都已经写了，这里甚至不需要手动进行处理什么东西
import lib.dayi_sqlite as dayidb #导入数据库
db = dayidb.db() #初始化数据库，已经都自动初始化啦

from data.news_sdust import * #爬虫相关的库

f = open('test-out.debug','w',encoding='utf-8') #调试信息的输出

def main():
  list_news = get_all_news()
  f.write(str(list_news))
  
  for i in list_news:
    now_url = i[3]
    now_title = i[2]
    list_page_only_text = get_pages_only_text()
  
  return

main()