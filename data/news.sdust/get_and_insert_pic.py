# 用于获得图片信息的函数，并且插入到数据库

# 没写完
test_url = 'https://ta.sdust.edu.cn/__local/E/CD/7F/A6575D5E4528C31029D3DB1BA44_0E66939E_150A1.jpg'

import aiohttp
import asyncio
import os

file_save_path = './data/pic/test/'

async def async_get_and_save_pic(url,file_save_path,file_name):
  
  test_url = url
  file_all_path = file_save_path+file_name
  async with aiohttp.ClientSession() as session:
    async with session.get(test_url) as response:
      print("Status:", response.status)
      print("Content-type:", response.headers['content-type'])
      if not os.path.isdir(file_save_path):
        os.mkdir(file_save_path)
      with open(file_all_path, "wb") as f:
        data = await response.read()
        f.write(data)
      
def get_and_insert_database(url,file_name):
  try:
    asyncio.run(async_get_and_save_pic(url,file_save_path=file_save_path,file_name=file_name))
  except Exception as e:
    print(str(e))
  
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
 
get_and_insert_database(test_url,file_name='234.jpg')
get_and_insert_database(test_url,file_name='2367.jpg')
get_and_insert_database(test_url,file_name='231.jpg')
get_and_insert_database(test_url,file_name='23121.jpg')
get_and_insert_database(test_url,file_name='2321.jpg')
get_and_insert_database(test_url,file_name='23213413131.jpg')
get_and_insert_database(test_url,file_name='2321365531.jpg')
get_and_insert_database(test_url,file_name='2321576831.jpg')
get_and_insert_database(test_url,file_name='2432591431.jpg')