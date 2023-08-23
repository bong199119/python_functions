import os
import shutil
import numpy as np

path = r'Z:\preprocessing\data\bleeding\yolo_format\2022_gachon_Bleeding'
path_to = r'Z:\preprocessing\dataset\bleeding\yolo_format'

def make_train_test_list(list_):
    list_train = []
    list_test = []

    len_list = len(list_)
    len_train = int(len_list*0.8)
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

os.makedirs(os.path.join(path_to, 'train/images'), exist_ok=True)
os.makedirs(os.path.join(path_to, 'train/labels'), exist_ok=True)
os.makedirs(os.path.join(path_to, 'val/images'), exist_ok=True)
os.makedirs(os.path.join(path_to, 'val/labels'), exist_ok=True)

path_train_img = os.path.join(path_to, 'train/images')
path_train_labels = os.path.join(path_to, 'train/labels')
path_val_img = os.path.join(path_to, 'val/images')
path_val_labels = os.path.join(path_to, 'val/labels')

list_png = [file_ for file_ in os.listdir(path) if file_.endswith('png')]
list_train, list_test = make_train_test_list(list_png)

for png_ele in list_train:
    path_png = os.path.join(path, png_ele)
    path_text = path_png[:-3] + 'txt'

    if os.path.isfile(path_png) and os.path.isfile(path_text):
        shutil.copy(path_png, os.path.join(path_train_img, png_ele))
        shutil.copy(path_text, os.path.join(path_train_labels, png_ele)[:-3] + 'txt')
        print(path_png)
        print(path_text)
            
for png_ele in list_test:
    path_png = os.path.join(path, png_ele)
    path_text = path_png[:-3] + 'txt'

    if os.path.isfile(path_png) and os.path.isfile(path_text):
        shutil.copy(path_png, os.path.join(path_val_img, png_ele))
        shutil.copy(path_text, os.path.join(path_val_labels, png_ele)[:-3] + 'txt')
        print(path_png)
        print(path_text)
        
