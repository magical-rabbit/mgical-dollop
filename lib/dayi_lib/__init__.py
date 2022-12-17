print("[dayi-lib] writed by dayi!")
print("[dayi-lib] do u wanna build a snowman?")

import datetime
import lib.dayi_lib.ovo

def get_days():
  """获得第一次的天数
  Returns:
      datetime:返回日期变量
  """
  date = datetime.datetime(year=2020,month=1,day=3)#日期变量
  return date
def get_next_day(date:datetime):
  """获得下一次的天数
  Returns:
      datetime:返回下一次的日期变量
  """
  d1 = datetime.timedelta(days=1) #天数变化值
  return date+d1

def get_day_str(date:datetime):
  """获得字符串时间，提高写代码的幸福感

  Args:
      date (datetime): 日期格式

  Returns:
      str: 20190101这样的字符串
  """
  return date.strftime("%Y%m%d")

def is_end(date:datetime):
  """判断是否是当日

  Args:
      date (datetime): 当前的日期

  Returns:
      _type_: _description_
  """ 
  if date>=datetime.datetime.today():
    return True
  return False