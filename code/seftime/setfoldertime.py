from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_WRITE, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, FILE_SHARE_WRITE

import os
import shutil
import pywintypes


source_dir_path = r"D:\code\setfiletime"
destination_dir_path = r"D:\code\target"

creation_times = [(d, pywintypes.Time(os.path.getctime(os.path.join(source_dir_path, d)))) for d in os.listdir(source_dir_path)]

for filename, ctime in creation_times:
    src = os.path.join(source_dir_path, filename)
    target = os.path.join(destination_dir_path, filename)
    shutil.copy(src, target)

    fh = CreateFile(target, GENERIC_WRITE, FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, 0)
    print(fh, ctime, ctime, ctime)
    SetFileTime(fh, ctime, ctime, ctime)    
    CloseHandle(fh)

# path_to_file = r'D:\code\setfiletime\test'

# import os

# access_time = 1561675987.509
# modification_time = 1561675987.509

# os.utime(path_to_file, (access_time, modification_time))