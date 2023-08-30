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