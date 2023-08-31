import os
import pandas as pd
import time
import numpy as np

dict_matrix = {}
total_count_overlap_FP = 0
total_count_overlap_TN = 0
total_count_overlap_FN = 0
total_count_overlap_TP = 0

path = r'D:\project\quality_inspection\NIA3\ldg0\data\cholec80format\gt'
# path = r'D:\project\데이터 시각화 및 통계\compare_csv_GT_nd_pred\NIA3\ldg0\data\model_version1.1.6_koreatoolmodel\test\gt_for_pred'

list_csv = os.listdir(path)

tool_be_compared = 'Dissector (kelly) (AESCULAP) (DSTL-KLAE)'
tool_compare_1 = 'Graspers (curved) (KARL STORZ) (GRSL-CIKS)'
tool_compare_2 = 'Liver'
tool_compare_3 = 'Gallbladder'

list_combination1 = [tool_compare_1, tool_compare_2]
list_combination2 = [tool_compare_1, tool_compare_3]
list_combination3 = [tool_compare_2, tool_compare_3]
list_combination4 = [tool_compare_1, tool_compare_2, tool_compare_3]
list_combination = [list_combination1, list_combination2, list_combination3, list_combination4]

for csv_ele in list_csv:
    path_csv_ele = os.path.join(path, csv_ele)
    df_gt = pd.read_csv(path_csv_ele)

    list_columns = list(df_gt.columns)
    list_tool_be_compared = list(df_gt[tool_be_compared])
    np_tool_be_compared = np.array(list_tool_be_compared)

    for combination_ele in list_combination:
        combination_name = ''
        for combi_ele in combination_ele:
            combination_name += combi_ele

        if len(combination_ele) == 2:
            list_tool_compare1 = list(df_gt[combination_ele[0]])
            list_tool_compare2 = list(df_gt[combination_ele[1]])

            np_tool_compare1 = np.array(list_tool_compare1)
            np_tool_compare2 = np.array(list_tool_compare2)

            np_count_combine = np_tool_compare1+np_tool_compare2 # 겹치는 부분 2로 치환
            np_count_overlap = np_tool_be_compared*5 + np_count_combine 

            list_count_overlap = list(np_count_overlap)
            count_overlap_TP = list_count_overlap.count(7)
            count_overlap_TN = list_count_overlap.count(0) + list_count_overlap.count(1)
            count_overlap_FP = list_count_overlap.count(2)
            count_overlap_FN = list_count_overlap.count(5) + list_count_overlap.count(6)
        
            if combination_name not in dict_matrix:
                dict_matrix[combination_name] = {'total_count_overlap_FP' : count_overlap_FP,
                                        'total_count_overlap_TN' : count_overlap_TN,
                                        'total_count_overlap_FN' : count_overlap_FN,
                                        'total_count_overlap_TP' : count_overlap_TP,
                                        }
            
            else:
                dict_matrix[combination_name]['total_count_overlap_FP'] += count_overlap_FP
                dict_matrix[combination_name]['total_count_overlap_TN'] += count_overlap_TN
                dict_matrix[combination_name]['total_count_overlap_FN'] += count_overlap_FN
                dict_matrix[combination_name]['total_count_overlap_TP'] += count_overlap_TP


        elif len(combination_ele) == 3:
            list_tool_compare1 = list(df_gt[combination_ele[0]])
            list_tool_compare2 = list(df_gt[combination_ele[1]])
            list_tool_compare3 = list(df_gt[combination_ele[2]])

            np_tool_compare1 = np.array(list_tool_compare1)
            np_tool_compare2 = np.array(list_tool_compare2)
            np_tool_compare3 = np.array(list_tool_compare3)

            np_count_combine = np_tool_compare1+np_tool_compare2+list_tool_compare3 # 겹치는 부분 3으로 치환
            np_count_overlap = np_tool_be_compared*5 + np_count_combine 

            list_count_overlap = list(np_count_overlap)
            count_overlap_TP = list_count_overlap.count(8)
            count_overlap_TN = list_count_overlap.count(0) + list_count_overlap.count(1) + list_count_overlap.count(2)
            count_overlap_FP = list_count_overlap.count(3)
            count_overlap_FN = list_count_overlap.count(5) + list_count_overlap.count(6) + list_count_overlap.count(7)
        
            if combination_name not in dict_matrix:
                dict_matrix[combination_name] = {'total_count_overlap_FP' : count_overlap_FP,
                                        'total_count_overlap_TN' : count_overlap_TN,
                                        'total_count_overlap_FN' : count_overlap_FN,
                                        'total_count_overlap_TP' : count_overlap_TP,
                                        }
            
            else:
                dict_matrix[combination_name]['total_count_overlap_FP'] += count_overlap_FP
                dict_matrix[combination_name]['total_count_overlap_TN'] += count_overlap_TN
                dict_matrix[combination_name]['total_count_overlap_FN'] += count_overlap_FN
                dict_matrix[combination_name]['total_count_overlap_TP'] += count_overlap_TP

list_column = []
list_FP = []
list_TN = []
list_FN = []
list_TP = []

list_acc = []
list_precision = []
list_recall = []
list_f1 = []

for column in dict_matrix:
    list_column.append(column)
    list_FP.append(dict_matrix[column]['total_count_overlap_FP'])
    list_TN.append(dict_matrix[column]['total_count_overlap_TN'])
    list_FN.append(dict_matrix[column]['total_count_overlap_FN'])
    list_TP.append(dict_matrix[column]['total_count_overlap_TP'])

    total_count_overlap_FP = dict_matrix[column]['total_count_overlap_FP']
    total_count_overlap_TN = dict_matrix[column]['total_count_overlap_TN']
    total_count_overlap_FN = dict_matrix[column]['total_count_overlap_FN']
    total_count_overlap_TP = dict_matrix[column]['total_count_overlap_TP']

    overlap_acc = (total_count_overlap_TP + total_count_overlap_TN)/(total_count_overlap_TP + total_count_overlap_TN + total_count_overlap_FP + total_count_overlap_FN)

    if (total_count_overlap_TP + total_count_overlap_FP) != 0:
        overlap_precision = round(total_count_overlap_TP/(total_count_overlap_TP + total_count_overlap_FP),2)
    else:
        overlap_precision = ''

    if (total_count_overlap_TP + total_count_overlap_FN) != 0:
        overlap_recall = round(total_count_overlap_TP/(total_count_overlap_TP + total_count_overlap_FN),2)
    else:
        overlap_recall = ''

    if overlap_precision != '' and overlap_recall != '' and (overlap_precision + overlap_recall) != 0:
        overlap_f1 = round((2*overlap_precision*overlap_recall)/(overlap_precision + overlap_recall),2)
    else:
        overlap_f1 = ''

    list_acc.append(overlap_acc)
    list_precision.append(overlap_precision)
    list_recall.append(overlap_recall)
    list_f1.append(overlap_f1)

df_total = pd.DataFrame()

df_total['tool'] = list_column
df_total['overlap_FP'] = list_FP
df_total['overlap_TN'] = list_TN
df_total['overlap_FN'] = list_FN
df_total['overlap_TP'] = list_TP

df_total['overlap_acc'] = list_acc
df_total['overlap_precision'] = list_precision
df_total['overlap_recall'] = list_recall
df_total['overlap_f1'] = list_f1

path_to = r'D:\project\quality_inspection\NIA3\ldg0\results\overlap_matrix_gt_combine.csv'
df_total.to_csv(path_to)
