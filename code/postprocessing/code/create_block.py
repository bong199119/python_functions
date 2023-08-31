import os
import pandas as pd
import numpy as np

def create_block(df, window_size_for_makeblock):
    window_size = window_size_for_makeblock
    list_window = []

    df_csv_origin = df
    df_csv = df_csv_origin.drop(['frame_no','phase'], axis = 1)

    for column in df_csv.columns:
        print(column)
        origin_array = np.array(df_csv[column])
        for idx, ele in enumerate(origin_array):
            if idx+window_size < len(origin_array):
                for i in range(window_size, 1, -1):
                    list_window = origin_array[idx : idx+i]
                    if list_window[0] == 1 and list_window[-1] == 1:
                        if list(np.ones(len(list_window))) == list(origin_array[idx : idx+i]):
                            break
                        origin_array[idx : idx+i] = np.array([list_window[0]]*i)
                    else:
                        continue

                list_window = origin_array[idx : idx+window_size]
                if list_window[0] == 0 and list_window[-1] == 0:
                    origin_array[idx : idx+i] = np.array([list_window[0]]*i)                

            # window size가 df 끝행에 도달하면
            elif idx+window_size == len(origin_array):
                for i in range(window_size-1, 1, -1):
                    list_window = origin_array[idx+i : idx+window_size]
                    if list_window[0] == 0 and list_window[-1] == 0:
                        origin_array[idx+i : idx+window_size] = np.array([list_window[0]]*len(list_window))

        df_csv[column] = origin_array

    df_csv.insert(0, 'frame_no', df_csv_origin['frame_no'])
    df_csv['phase'] = df_csv_origin['phase']

    return df_csv