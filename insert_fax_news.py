#要闻传真，嘿嘿嘿，总算写完了全部的接口了，开整！
#因为几乎所有的接口都已经写了，这里甚至不需要手动进行处理什么东西
import lib.dayi_sqlite as dayidb #导入数据库
db = dayidb.db() #初始化数据库，已经都自动初始化啦

from data.news_sdust import * #爬虫相关的库

f = open('test-out.debug','w')

def main():
  list_news = get_all_news()
  print(list_news)
  return

main()