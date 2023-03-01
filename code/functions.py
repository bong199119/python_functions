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