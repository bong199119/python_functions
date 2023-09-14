import os
import win32file
import win32api
import win32con
import datetime
import time

# Specify the path of the file whose creation time needs to be changed
file_path = r'D:\code\setfiletime\test'


new_time = datetime.datetime(2000, 3, 17, 12, 0, 0) #년월일 시분초
new_time = str(new_time)
d = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
print(time.mktime(d.timetuple()))


# print(new_time)
from win32_setfiletime import setctime, setmtime, setatime

setctime(file_path, time.mktime(d.timetuple()))
setmtime(file_path, 1561675987.509)
setatime(file_path, 1561675987.509)