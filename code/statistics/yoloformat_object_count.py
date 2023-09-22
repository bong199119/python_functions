import os

path = r'Z:\preprocessing\model_test\dataset'
list_folder = [
    # 'model_test_1stdataset',
    # 'model_test_2nddataset',
    # 'model_test_3rddataset',
    # 'model_test_4thdataset',
    'model_test_5thdataset',
]
dict_mapping = {
    '0':'object1',
    '1':'object2',
    '2':'object3',
    '3':'object4',
    '4':'object5',
    '5':'object6',
    '6':'object7',
    '7':'object8',
    '8':'object9',
    '9':'object10',
    '10':'object11',
    '11':'object12',
}
dict_tool_count = {}

for folder_ in list_folder:
    path_folder = os.path.join(path, folder_)
    path_train_label = os.path.join(path_folder, 'yolo_format', 'train', 'labels')
    path_val_label = os.path.join(path_folder, 'yolo_format', 'val', 'labels')
    
    list_train_label = os.listdir(path_train_label)    
    list_val_label = os.listdir(path_val_label)    

    # train label read and count
    for train_label in list_train_label:
        print(train_label)
        train_label_txt = os.path.join(path_train_label, train_label)
        with open(train_label_txt, "r") as text_:
            for line in text_:
                cls = line.split(' ')[0]
                if cls not in dict_tool_count:
                    dict_tool_count[cls] = 1
                else:
                    dict_tool_count[cls] += 1
                    print(f'{cls} + 1')

    # test label read and count
    for val_label in list_val_label:
        print(val_label)
        val_label_txt = os.path.join(path_val_label, val_label)
        with open(val_label_txt, "r") as text_:
            for line in text_:
                cls = line.split(' ')[0]
                if cls not in dict_tool_count:
                    dict_tool_count[cls] = 1
                else:
                    dict_tool_count[cls] += 1
                    print(f'{cls} + 1')

    total_count = 0
    for tool_ in dict_tool_count:
        print(f'{dict_mapping[tool_]} count : {dict_tool_count[tool_]}')
        total_count += dict_tool_count[tool_]

    print(f'total count : {total_count}')
