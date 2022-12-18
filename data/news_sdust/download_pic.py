# 用于异步下载并保存文件
# 函数调用:
"""
get_and_download(url,file_save_path,file_name)
url : 下载链接
file_save_path : 文件下载目录
file_name : 文件名
"""
# 接口返回: [201,'[dayi-info]图片下载完成:{}{}'.format(file_save_path,file_name)]

# 没写完
# test_url = 'https://ta.sdust.edu.cn/__local/E/CD/7F/A6575D5E4528C31029D3DB1BA44_0E66939E_150A1.jpg'

import aiohttp
import asyncio
import os

async def async_get_and_save_pic(url,file_save_path,file_name):
  test_url = url
  file_all_path = file_save_path+file_name
  async with aiohttp.ClientSession() as session:
    async with session.get(test_url) as response:
      # print("Status:", response.status)
      # print("Content-type:", response.headers['content-type'])
      if not os.path.isdir(file_save_path):
        os.makedirs(file_save_path)
      with open(file_all_path, "wb") as f:
        data = await response.read()
        f.write(data)
      
def get_and_download(url,file_save_path,file_name):
  att = 0
  while att<=4:
    try:
      asyncio.run(async_get_and_save_pic(url,file_save_path=file_save_path,file_name=file_name))
      return [201,'[dayi-info]图片下载完成:{}{}'.format(file_save_path,file_name)]
    except Exception as e:
      att+=1
      return [501,'[dayi-error]未知错误:{}'.format(str(e))]
  return [503,'[dayi-error]图片下载失败,url:{}'.format(url)]
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())