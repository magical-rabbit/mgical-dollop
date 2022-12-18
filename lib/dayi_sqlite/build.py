import sqlite3
import datetime,time
import uuid #用于插入媒体的时候判断唯一的信息

import os #解析文件名（手动解析也是可以的，但是 str(media_url).split('.')[-1].lower() 感觉肯定会有问题）
from urllib.parse import urlparse #用这个解析url比较安全

__dayi_debug__ = True
__dayi_rm_db__ = False

class dayi_db_ovo:
  def __init__(self,dbpath='./dayi-db.db'):
    self.dbpath = dbpath
    
    self.__del_data_base__() #删除数据库，调试用。
    
    self.__enter__(dbpath=dbpath)
  
  def __enter__(self,dbpath='./dayi-db.db'):
    if __dayi_debug__:print([201,'[dayi-info]数据库目录:'+dbpath])
    
    try:
      self.init_con(dbpath=dbpath)
      if __dayi_debug__:print([201,'[dayi-info]初始化连接成功'])
    except Exception as e:
      if __dayi_debug__:print([401,'[dayi-error]初始化连接失败:'+str(e)])
      
    try:
      self.build_tables()
      if __dayi_debug__:print([201,'[dayi-info]数据表创建成功'])
    except Exception as e:
      if __dayi_debug__:print([401,'[dayi-error]数据表创建失败:'+str(e)])
      
    return self
  def __exit__(self, exc_type, exc_val, exc_tb):
    print("[ovo?]")
    self.conn.close()

  def init_con(self,dbpath):
    path = dbpath
    self.conn = sqlite3.connect(path)
    self.cur = self.conn.cursor()
    return self.conn
  
  def __del_data_base__(self):
    
    if __dayi_rm_db__ == False: #不删除数据库
      if __dayi_debug__:
        print([101,'[dayi-info]不进行删除数据库'])
      return [101,'[dayi-info]不进行删除数据库']
  
    dbpath = self.dbpath #获得数据库目录
    
    if __dayi_debug__: print([203,'[dayi-warning]Will delete database:'+dbpath])
    try:
      import os
      os.remove(self.dbpath)
      if __dayi_debug__: print([203,'[dayi-warning]Deleted database:'+dbpath])
    except Exception as e:
      if __dayi_debug__:print([401,'[dayi-error]数据库删除失败:'+str(e)])
  
  def sql_command(self,sql_text):
    self.cur.execute(sql_text)
    ans = self.conn.commit()
    return ans 
  
  def build_tables(self):
    table_create_content_list="""
      CREATE TABLE IF NOT EXISTS content_list(
      "id" INTEGER NOT NULL,
      "content_title" text,
      "content_publish_time" TEXT,
      "content_publish_time_unix" TEXT,
      "content_clicks_num" TEXT,
      "content_only_text" TEXT,
      "content_only_pic" TEXT,
      "content_url" TEXT,
      "content_all" TEXT,
      "json" TEXT,
      PRIMARY KEY ("id")
      );
    """

    table_create_media_list="""
      CREATE TABLE IF NOT EXISTS media_list (
        "id" INTEGER NOT NULL,
        "media_date_str" TEXT,
        "media_uuid" TEXT,
        "media_url" TEXT,
        "media_local_path" TEXT,
        "media_type" TEXT,
        "media_file_size" TEXT,
        "media_is_downloaded" TEXT,
        "json" TEXT,
        PRIMARY KEY ("id")
      );
    """
    
    table_covid_data_list="""
      CREATE TABLE IF NOT EXISTS covid_19_data (
        "id" INTEGER NOT NULL,
        "date" TEXT,
        "date_unix" interger,
        "province_code" TEXT,
        "province_name" TEXT,
        "seem_add" TEXT,
        "seem_all" TEXT,
        "sure_add" TEXT,
        "sure_all" TEXT,
        "die_add" TEXT,
        "die_all" TEXT,
        "json" TEXT,
        PRIMARY KEY ("id")
      );
    """
    
    self.cur.execute(table_create_content_list)
    self.cur.execute(table_create_media_list)
    self.cur.execute(table_covid_data_list)
    
    self.conn.commit()#保存数据库
    return
  
  def insert_covid_date(self,date:datetime,province_name,province_code,sure_add,sure_all,die_add,die_all):
    table_name = 'covid_19_data' #表名
    date_unix = time.mktime(date.timetuple()) #unix time
    date_str = date.strftime("%Y%m%d") #20220101
    
    # print(date_unix)
    sql_command="insert or ignore into {table_name} (date,date_unix,province_name,province_code,sure_add,sure_all,die_add,die_all) values ('{date_str}','{date_unix}','{province_name}','{province_code}','{sure_add}','{sure_all}','{die_add}','{die_all}');".format(table_name=table_name,date_str=date_str,date_unix=date_unix,province_code=province_code,province_name=province_name,sure_add=sure_add,sure_all=sure_all,die_add=die_add,die_all=die_all)
    
    # print(sql_command)
    
    self.cur.execute(sql_command)
    self.conn.commit()
  
  def insert_pic_db(self, media_url, media_local_path='./data/news.sdust/data/pic/', media_type='jpg', date: datetime=datetime.datetime(2022,1,1)):
    """图片插入
    "media_url" TEXT, 图片URL
    "media_local_path" TEXT 图片的本地存储路径,仅目录,图片名字用UUID生成
    "media_type" TEXT, 图片的类型
    "media_file_size" TEXT, 图片的大小
    "media_uuid" TEXT, 图片UUID
    "media_is_downloaded" TEXT, 图片是否已经下载
    "media_date_str" TEXT, 图片的日期
    Args:
        参数其实只有url有用
    """
    
    table_name='media_list' #表名
    media_uuid=uuid.uuid1() #生成UUID
    date_str = date.strftime("%Y%m%d")
    date_str_month = date.strftime("%m")
    date_str_year  = date.strftime("%Y")
    
    _,media_type=os.path.splitext(urlparse(media_url).path) #这样相对安全一点
    # media_type=str(media_url).split('.')[-1].lower() #这样写其实不是很好 #获得扩展名
    
    media_local_path_with_file_name = media_local_path+'{}/{}/'.format(date_str_year,date_str_month)+str(media_uuid)+media_type #获得本地路径
    print(media_local_path_with_file_name)
    sql_command= "insert or ignore into {table_name} (media_uuid,media_url,media_local_path,media_type,media_is_downloaded,media_date_str) values ('{media_uuid}','{media_url}','{media_local_path}','{media_type}','{media_is_downloaded}','{media_date_str}')".format(table_name=table_name,media_uuid=media_uuid,media_local_path=media_local_path_with_file_name,media_type=media_type.split('.')[-1],media_url=media_url,media_is_downloaded=0,media_date_str=date_str)
    # print(sql_command)
    self.cur.execute(sql_command)
    # self.conn.commit() #IO太慢啦
    return media_uuid
  def insert_content_db(self,content_title,date:datetime,content_clicks_num,content_only_text,content_url,content_only_pic='',content_all=''):
    """插入图片的信息到数据库中,请注意,此方法需要手动进行更新数据库
      CREATE TABLE IF NOT EXISTS content_list(
      "id" INTEGER NOT NULL,
      "content_title" text,
      "content_publish_time" TEXT,
      "content_publish_time_unix" TEXT,
      "content_clicks_num" TEXT,
      "content_only_text" TEXT,
      "content_only_pic" TEXT,
      "content_url" TEXT,
      "content_all" TEXT,
      "json" TEXT,
      PRIMARY KEY ("id")
      );
    """
    table_name='content_list' #表名
    date_unix = time.mktime(date.timetuple()) #unix time
    date_str = date.strftime("%Y%m%d") #20220101
    
    sql_command= "insert or ignore into {table_name} (content_title,content_publish_time,content_publish_time_unix,content_clicks_num,content_only_text,content_only_pic,content_url,content_all) values ('{content_title}','{content_publish_time}','{content_publish_time_unix}','{content_clicks_num}','{content_only_text}','{content_only_pic}','{content_url}','{content_all}')".format(content_title=content_title,content_publish_time=date_str,content_publish_time_unix=date_unix,content_clicks_num=content_clicks_num,content_only_text=content_only_text,content_only_pic=content_only_pic,content_url=content_url,content_all=content_all,table_name=table_name)
    # print(sql_command)
    self.cur.execute(sql_command)
    
  def commit_db(self): #保存数据库，因为IO太慢了，得分开
    self.conn.commit()
    return

    
    

# db = dayi_db_ovo()
# db.insert_pic_db("http://iuqiweuoqwe.qeryuiqewirqe.cc/rq134132.png12.21.33")

# print(db.sql_command(sql_text="Select * from covid_19_data"))

# dt = datetime.datetime(2022,1,1)
# db.insert_covid_date(dt,"山东省","37000000",sure_add=1,sure_all=10,die_all=0,die_add=0)

# db.insert_content_db("标题",dt,"2333","猴子开飞机",'http://monkey',"http://pic_monkey")
# db.conn.commit()
