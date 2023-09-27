def sec_to_hms(sec):
    h = int(sec//3600)
    sec = sec-h*3600
    m = int(sec//60)
    sec = sec-m*60

    if len(str(h)) == 1:
        h_str = '0'+str(h)
    else:
        h_str = str(h)
    if len(str(m)) == 1:
        m_str = '0'+str(m)
    else:
        m_str = str(m)
    # if len(str(sec)) != 4:
    #     s_str = '0'+str(sec)
    # else:
    #     s_str = str(sec)
    if len(str(sec)) == 1:
        s_str = '0'+str(sec)
    else:
        s_str = str(sec)

    hms = h_str +':'+m_str+':'+s_str
    return hms

fps = 30
fram_gap = 30
def frame_to_hms(idx):
    sec = idx * (fram_gap/fps)
    sec = round(sec)

    h = int(sec//3600)
    sec = sec-h*3600
    m = int(sec//60)
    sec = sec-m*60

    if len(str(h)) == 1:
        h_str = '0'+str(h)
    else:
        h_str = str(h)
    if len(str(m)) == 1:
        m_str = '0'+str(m)
    else:
        m_str = str(m)
    # if len(str(sec)) != 4:
    #     s_str = '0'+str(sec)
    # else:
    #     s_str = str(sec)
    if len(str(sec)) == 1:
        s_str = '0'+str(sec)
    else:
        s_str = str(sec)

    hms = h_str +':'+m_str+':'+s_str
    return hms

def hms_to_sec(hms):
    h = int(hms.split(':')[0])
    m = int(hms.split(':')[1])
    s = int(hms.split(':')[2])

    if h < 0:
        raise Exception('not available number for h')
    
    if (len(hms.split(':')[1]) != 2) or (m < 0) or (m > 60):
        raise Exception('not available number for m')
    
    if (len(hms.split(':')[2]) != 2) or (s < 0) or (s > 60):
        raise Exception('not available number for s')
    
    sec = (h * 3600) + (m * 60) + s
    return sec

####
import math
####
def get_samplesize(n, z_score, stddev, margin):

    if n > 0:
        sample_size_s = ((z_score*z_score)*stddev*(1-stddev))/(margin * margin)
        sample_size = sample_size_s / (1 + (sample_size_s / n))
        sample_size = math.ceil(sample_size)

    else:
        sample_size = 0

    return sample_size

####
import numpy as np
z_score = 1.96 # 신뢰도 95%
stddev = 0.5 # 표준편차 0.5 -> 표본의 크기를 보장하는 좋은 방법
margin = 0.05 # 오차 5%
'''
list_parameter : 모수크기 -> int
list_sample : 표본크기 -> int
'''
####
def get_sample(list_parameter):
    sample_size = get_samplesize(len(list_parameter), z_score, stddev, margin)
    list_sample = np.random.choice(list_parameter, sample_size, replace=False) # 샘플사이즈만큼 비복원추출
    list_sample.sort()
    return list_sample

'''
hms_list : ['hms','hms', ... ,'hms']
hms_list_packaged : ['hms ~ hms', ... ,'hms ~ hms']
'''
def packaging_hms_list(hms_list):
    sec_list = []
    for hms_ele in hms_list:
        sec = hms_to_sec(hms_ele)
        sec_list.append(sec)

    before_sec = ''
    list_stack = []
    hms_list_packaged = []
    for idx, sec_ele in enumerate(sec_list):
        if before_sec == '':
            before_sec = sec_ele
            list_stack.append(before_sec)

        else:
            if before_sec+1 == sec_ele:
                list_stack.append(sec_ele)
                
            if (before_sec+1 != sec_ele) or (idx == len(sec_list)-1):
                hms_list_packaged.append(f'{sec_to_hms(list_stack[0])} ~ {sec_to_hms(list_stack[-1])}')
                list_stack = [sec_ele]

            before_sec = sec_ele

    return hms_list_packaged

'''
list_hmspkg : ['hms ~ hms', ... ,'hms ~ hms']
list_secpkg : ['sec ~ sec', ... ,'sec ~ sec']
'''
def hmspkg_to_secpkg(list_hmspkg):
    list_secpkg = []
    for hmspck in list_hmspkg:
        first_hms = hmspck.split('~')[0][:-1]
        second_hms = hmspck.split('~')[1][1:]
        
        first_sec = hms_to_sec(first_hms)
        second_sec = hms_to_sec(second_hms)
        
        list_secpkg.append(str(first_sec) + ' ~ ' + str(second_sec))
    
    return list_secpkg   

def hms_to_hmsWC(hms):
    h = hms.split(':')[0]
    m = hms.split(':')[1]
    s = hms.split(':')[2]

    hmswc = h+m+s
    return hmswc

def hms_to_duetime(hmspck):
    first_hms = hmspck.split('~')[0][:-1]
    second_hms = hmspck.split('~')[1][1:]
    
    first_sec = hms_to_sec(first_hms)
    second_sec = hms_to_sec(second_hms)

    duetime = second_sec - first_sec
    
    return duetime   

# dataFrame lambda apply
import pandas as pd
import os
train = pd.read_csv('D:\project\python_functions\data\train.csv')

def change_videopath(path_origin):
  file_name = path_origin.split('/')[-1]
  path_trainfolder = 'D:\project\python_functions\data\train'
  path_new = os.path.join(path_trainfolder, file_name)
  return path_new

train['video_path'] = train.apply(lambda x: change_videopath(x['video_path']),axis=1)

####
import numpy as np
'''
list_ : list for split
train_size : 0.5 =< train_size < 1
'''
####
def make_train_test_list(list_, train_size):
    list_train = []
    list_test = []

    if train_size >= 1 or train_size < 0.5:
        return 

    len_list = len(list_)
    len_train = int(len_list*train_size)
    len_test = len_list - len_train

    test_indices = np.random.choice(range(0, len_list), len_test, replace=False)
    train_indices = []
    for index_ in range(len_list):
        if index_ not in test_indices:
            train_indices.append(index_)

    test_indices_array = np.array(test_indices)
    train_indices_array = np.array(train_indices)

    for test_index in test_indices_array:
        test_ele = list_[test_index]
        list_test.append(test_ele)

    for train_index in train_indices_array:
        train_ele = list_[train_index]
        list_train.append(train_ele)

    return list_train, list_test


####
import numpy as np
'''
list_pred : prediction list made by 0 or 1
list_gt : gt list made by 0 or 1 

list_ : list made by 0 or 1 if mismatch pred, gt in same frame 1, elif match 0

0 : no detection
1 : detection 
'''
####
def list_mismatch(list_pred, list_gt):
    array_pred = np.array(list_pred)
    array_gt = np.array(list_gt)
    
    array_sum = array_pred + array_gt
    list_sum = list(array_sum)
    
    list_ = [ele if ele == 1 else 0 for ele in list_sum]
    
    return list_

def list_match(list_pred, list_gt):
    array_pred = np.array(list_pred)
    array_gt = np.array(list_gt)
    
    array_sum = array_pred + array_gt
    list_sum = list(array_sum)
    
    list_ = [1 if ele != 1 else 0 for ele in list_sum]
    
    return list_

def list_appear_total(list_pred, list_gt):
    array_pred = np.array(list_pred)
    array_gt = np.array(list_gt)
    
    list_sum = list(array_gt)
    
    list_ = list_sum
    
    return list_

def list_appear(list_pred, list_gt):
    array_pred = np.array(list_pred)
    array_gt = np.array(list_gt)
    
    array_sum = array_pred + array_gt
    list_sum = list(array_sum)
    
    list_ = [1 if ele == 2 else 0 for ele in list_sum]
    
    return list_

# bubble sort
def sort_by_imgnamenumsize(list_, sepsign, indexofnum):
    for i in range(len(list_) - 1, 0, -1):
        for j in range(i):
            if list_[j].split(sepsign)[indexofnum][:-4] > list_[j + 1].split(sepsign)[indexofnum][:-4]:
                list_[j], list_[j + 1] = list_[j + 1], list_[j]

    return list_

def make_08d(idx):
    idx_08d = (8-len(str(idx)))*'0'+str(idx)
    return idx_08d

######################################################
###########  other library or usefull code ###########
######################################################

####
import time
'''

'''
####
time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


# 특정 도구(classid) 샘플 복사(이미지, xml, text)
####
import os
import time
import shutil
####

path = r''
path_xmlfolder = r''
path_to = r''

list_folder = [list_ for list_ in os.listdir(path) if os.path.isdir(os.path.join(path,list_))]

for folder_ in list_folder:
    path_folder = os.path.join(path, folder_)
    path_xmlfolder_folder = os.path.join(path_xmlfolder, folder_)
    list_txt = [file_ for file_ in os.listdir(path_folder) if file_.endswith('txt')]
    for txt_ in list_txt:
        path_folder_txt = os.path.join(path_folder, txt_)
        path_folder_png = path_folder_txt[:-3] + 'png'
        path_xmlfolder_folder_xml = os.path.join(path_xmlfolder_folder, txt_[:-3] + 'xml')

        to_path_folder_png = os.path.join(path_to, txt_[:-3] + 'png')
        to_path_folder_xml = os.path.join(path_to, txt_[:-3] + 'xml')

        with open(path_folder_txt, "r") as f:
            for line in f:
                class_id = line.split(' ')[0]
                if class_id == '5':
                    shutil.copy(path_folder_png, to_path_folder_png)
                    shutil.copy(path_xmlfolder_folder_xml, to_path_folder_xml)

                