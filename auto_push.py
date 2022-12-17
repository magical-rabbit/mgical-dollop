import os
os.system("git add .")
import datetime
dt = datetime.datetime.now()
dt_str = dt.strftime("%y:%m:%d-%H:%M:%S")

os2 = 'git commit -m "{}" '.format(dt_str)
print(os2)

os.system(os2)
os.system("git push")
# print(dt_str)
# os.system

# git add .
# git commit -m "%time%"
# git push