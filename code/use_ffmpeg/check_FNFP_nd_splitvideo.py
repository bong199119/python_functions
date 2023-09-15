import os
import pandas as pd
import numpy as np

def list_appear_total(list_pred, list_gt):
    array_pred = np.array(list_pred)
    array_gt = np.array(list_gt)
    
    list_sum = list(array_gt)
    
    list_ = list_sum
    
    return list_

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

def list_appear(list_pred, list_gt):
    array_pred = np.array(list_pred)
    array_gt = np.array(list_gt)
    
    array_sum = array_pred + array_gt
    list_sum = list(array_sum)
    
    list_ = [1 if ele == 2 else 0 for ele in list_sum]
    
    return list_

def list_FN(list_pred, list_gt):
    array_pred = np.array(list_pred)
    array_gt = np.array(list_gt)
    
    array_sum = array_pred + array_gt*3
    list_sum = list(array_sum)
    
    list_ = [1 if ele == 3 else 0 for ele in list_sum]
    
    return list_

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
'''

def sample_from_packaging_hms_list(list_hmspkg, due_time): # due_time : FP, FN 지속시간
    sample_hms_list = []

    for hmspck in list_hmspkg:
        first_hms = hmspck.split('~')[0][:-1]
        second_hms = hmspck.split('~')[1][1:]
        
        first_sec = hms_to_sec(first_hms)
        second_sec = hms_to_sec(second_hms)
        if (second_sec - first_sec) >= due_time:
            sample_hms_list.append(hmspck)

    return sample_hms_list

video_name = ''
path_GT_csv = rf''
path_pred_csv = rf''
path_video = rf''
path_clip = r''

###### config
fps = 30
fram_gap = 30
dict_column_index = {}
dict_column_index_FN = {}
due_time = 2
tool_name = ''

path_gtfile = path_GT_csv
path_predfile = path_pred_csv

df_gt = pd.read_csv(path_gtfile)
df_pred = pd.read_csv(path_predfile)

df_pred.drop(labels=['Frame'], axis=1, inplace=True)

for column_ in df_pred.columns:
    if column_ in df_gt.columns:
        dict_column_index[column_] = list_mismatch(df_pred[column_], df_gt[column_])     
        dict_column_index_FN[column_] = list_FN(df_pred[column_], df_gt[column_])                                       
        
### FN, FP
dict_hms = {}
dict_hms_final = {}
for column_ in dict_column_index:
    dict_hms[column_] = []
    for index, ele in enumerate(dict_column_index[column_]):
        if ele == 1:
            hms = frame_to_hms(index)
            dict_hms[column_].append(hms)
            
    hms_list_packaged = packaging_hms_list(dict_hms[column_])

    # due_time 이상되는 구간만 샘플
    smaple_hms_list_packaged = sample_from_packaging_hms_list(hms_list_packaged, due_time)
    dict_hms_final[column_] = smaple_hms_list_packaged

### FN, FP
dict_hms_FN = {}
dict_hms_final_FN = {}
for column_ in dict_column_index_FN:
    dict_hms_FN[column_] = []
    for index, ele in enumerate(dict_column_index_FN[column_]):
        if ele == 1:
            hms = frame_to_hms(index)
            dict_hms_FN[column_].append(hms)
            
    hms_list_packaged_FN = packaging_hms_list(dict_hms_FN[column_])

    # due_time 이상되는 구간만 샘플
    smaple_hms_list_packaged_FN = sample_from_packaging_hms_list(hms_list_packaged_FN, due_time)
    dict_hms_final_FN[column_] = smaple_hms_list_packaged_FN


# mismatch
print(dict_hms_final[tool_name])
print('False 샘플개수 : ', len(dict_hms_final[tool_name]), '개')
print()
print(dict_hms_final_FN[tool_name])
print('FN 샘플개수 : ', len(dict_hms_final_FN[tool_name]), '개')