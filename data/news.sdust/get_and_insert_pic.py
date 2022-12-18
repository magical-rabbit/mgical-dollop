# 用于获得图片信息的函数，并且插入到数据库

# 没写完
test_url = 'https://ta.sdust.edu.cn/__local/E/CD/7F/A6575D5E4528C31029D3DB1BA44_0E66939E_150A1.jpg'

import aiohttp
import asyncio


async def async_main():
  print('ovo')
  async with aiohttp.ClientSession() as session:
    async with session.get(test_url) as response:
      print("Status:", response.status)
      print("Content-type:", response.headers['content-type'])
      data = await response
      
def get_and_insert_database(url):
  loop = asyncio.get_event_loop()
  loop.run_until_complete(async_main())
  get_and_insert_database(test_url)