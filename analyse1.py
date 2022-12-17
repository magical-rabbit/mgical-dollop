import json #解析json
import os #文件操作等
from lib import dayi_lib


days = dayi_lib.get_days()
str_days = dayi_lib.get_day_str(days)

while(True):
  if dayi_lib.is_end(days):break #到今天就结束了
  file_path = './data/covid-19/data/{}.json'.format(str_days)
  days=dayi_lib.get_next_day(days)#获得下一天
  str_days=dayi_lib.get_day_str(days)
  if os.path.exists(file_path):
    #找到了文件，开玩
    # print("ovo"+file_path)
    f = open(file_path)#开文件
    json1 = json.loads(f.read())
    f.close()#记得关文件
    for i in json1['features']:
      if i['properties']['省份']=='山东省':
        # print(i['properties'])
        print("{:2} {}".format(str_days,i['properties']['累计确诊']))

# f = open('./data/data/{}.json'.format(str_days))

# json1 = json.loads(f.read())
# for i in json1['features']:
#   # print(i['properties'])
#   if i['properties']['省份']=='山东省':
#     print(i['properties'])