import os
os.system("git pull")
os.system("git add .")
import datetime
dt = datetime.datetime.now()
dt_str = dt.strftime("%y年%m月%d日%H:%M:%S 要闻传真的首页忘了获取")

os2 = 'git commit -m "{}" '.format(dt_str)
print(os2)

os.system(os2)
os.system("git push")