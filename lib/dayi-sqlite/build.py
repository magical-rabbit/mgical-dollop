import sqlite3
__dayi_debug__ = True

class dayi_db:
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
    dbpath = self.dbpath
    
    if __dayi_debug__: print([203,'[dayi-warning]Will delete database:'+dbpath])
    try:
      import os
      os.remove(self.dbpath)
      if __dayi_debug__: print([203,'[dayi-warning]Deleted database:'+dbpath])
    except Exception as e:
      if __dayi_debug__:print([401,'[dayi-error]数据库删除失败:'+str(e)])
      
  
  def build_tables(self):
    table_create_content_list="""
      CREATE TABLE IF NOT EXISTS content_list(
      "id" INTEGER NOT NULL,
      "content_title" text,
      "content_publish_time" TEXT,
      "content_publish_time_unix" TEXT,
      "content_with_pic" TEXT,
      "content_only_text" TEXT,
      "content_only_pic" TEXT,
      "content_url" TEXT,
      "content_all" TEXT,
      "json" TEXT,
      PRIMARY KEY ("id")
      );
    """

    table_create_media_list="""
      CREATE TABLE IF NOT EXISTS list (
        "id" INTEGER NOT NULL,
        "media_url" TEXT,
        "media_local_path" TEXT,
        "media_type" TEXT,
        "media_file_size" TEXT,
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
        "province" TEXT,
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

db = dayi_db()
