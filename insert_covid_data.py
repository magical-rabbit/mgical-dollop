#导入模块
import json,os
import sys 
sys.path.append("..") #回退目录

import lib.dayi_sqlite as dayi_db #导入模块
import lib.dayi_lib as dayi_lib

# from lib import dayi_lib #常用的分析模块


db = dayi_db.db()

def gen_covid_data_DB():
  days = dayi_lib.get_days()
  str_days = dayi_lib.get_day_str(days)
  
  while(True):
    if dayi_lib.is_end(days):break #到今天就结束了
    file_path = './data/covid-19/data/{}.json'.format(str_days)
    days=dayi_lib.get_next_day(days)#获得下一天
    str_days=dayi_lib.get_day_str(days)
    # print(file_path)
    # print(os.getcwd())
    if os.path.exists(file_path):
      #找到了文件，开玩
      # print("ovo"+file_path)
      f = open(file_path)#开文件
      json1 = json.loads(f.read())
      f.close()#记得关文件
      for i in json1['features']:
        insert_db_datetime = days
        insert_db_province_name = i['properties']['省份']
        insert_db_province_code = i['properties']['编码']
        insert_db_sure_add = i['properties']['新增确诊']
        insert_db_sure_all = i['properties']['累计确诊']
        insert_db_die_add  = i['properties']['新增死亡']
        insert_db_die_all =  i['properties']['累计死亡']
        
        # print(i['properties'])
        db.insert_covid_date(date=insert_db_datetime,province_code=insert_db_province_code,province_name=insert_db_province_name,sure_add=insert_db_sure_add,sure_all=insert_db_sure_all,die_add=insert_db_die_add,die_all=insert_db_die_all)
        
        if i['properties']['省份']=='山东省':
          # print(i['properties'])
          print("{:2} {}".format(str_days,i['properties']['累计确诊']))
  return

gen_covid_data_DB() #插入到数据库中
          
          