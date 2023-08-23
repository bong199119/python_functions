import os
import shutil

list_train = [
    'SNUH_DC16_KSH0_LDG0_0031',
    'SNUH_DC16_KSH0_LDG0_0032',
    'SNUH_DC16_KSH0_LDG0_0033',
    'SNUH_DC16_KSH0_LDG0_0034',
    'SNUH_DC16_KSH0_LDG0_0035',
    'SNUH_DC16_KSH0_LDG0_0036',
    'SNUH_DC16_KSH0_LDG0_0037',
    'SNUH_DC16_KSH0_LDG0_0038',
    'SNUH_DC16_KSH0_LDG0_0039',
    'SNUH_DC16_KSH0_LDG0_0040',
    'SNUH_DC16_KSH0_LDG0_0041',
    'SNUH_DC16_KSH0_LDG0_0046',
    'SNUH_DC16_KSH0_LDG0_0047',
    'SNUH_DC16_KSH0_LDG0_0048',
    'SNUH_DC16_KSH0_LDG0_0051',
    'SNUH_DC16_KSH0_LDG0_0054',
    'SNUH_DC16_KSH0_LDG0_0055',
    'SNUH_DC16_KSH0_LDG0_0056',
    'SNUH_DC16_KSH0_LDG0_0059',
    'SNUH_DC16_KSH0_LDG0_0060',
    'SNUH_DC16_KSH0_LDG0_0061',
    'SNUH_DC16_KSH0_LDG0_0062',
    'SNUH_DC16_KSH0_LDG0_0064',
    'SNUH_DC16_KSH0_LDG0_0065',
    'SNUH_DC16_KSH0_LDG0_0066',
    'SNUH_DC16_KSH0_LDG0_0067',
    'SNUH_DC16_KSH0_LDG0_0068',
    'SNUH_DC16_KSH0_LDG0_0069',
    'SNUH_DC16_KSH0_LDG0_0071',
    'SNUH_DC16_KSH0_LDG0_0072',
    'SNUH_DC16_KSH0_LDG0_0073',
    'SNUH_DC16_KSH0_LDG0_0075',
    'SNUH_DC16_KSH0_LDG0_0076',
    'SNUH_DC16_KSH0_LDG0_0077',
    'SNUH_DC16_KSH0_LDG0_0079',
    'SNUH_DC16_YHG0_LDG0_0001',
    'SNUH_DC16_YHG0_LDG0_0001',
    'SNUH_DC16_YHG0_LDG0_0002',
    'SNUH_DC16_YHG0_LDG0_0003',
    'SNUH_DC16_YHG0_LDG0_0004',
    'SNUH_DC16_YHG0_LDG0_0005',
    'SNUH_DC16_YHG0_LDG0_0006',
    'SNUH_DC16_YHG0_LDG0_0007',
    'SNUH_DC16_YHG0_LDG0_0008',
    'SNUH_DC16_YHG0_LDG0_0009',
    'SNUH_DC16_YHG0_LDG0_0010',
    'SNUH_DC16_YHG0_LDG0_0011',
    'SNUH_DC16_YHG0_LDG0_0012',
    'SNUH_DC16_YHG0_LDG0_0013',
    'SNUH_DC16_YHG0_LDG0_0014',
    'SNUH_DC16_YHG0_LDG0_0015',
    'SNUH_DC16_YHG0_LDG0_0016',    
]

list_val = [
    'SNUH_DC16_KSH0_LDG0_0042',
    'SNUH_DC16_KSH0_LDG0_0043',
    'SNUH_DC16_KSH0_LDG0_0045',
    'SNUH_DC16_KSH0_LDG0_0049',
    'SNUH_DC16_KSH0_LDG0_0053',
    'SNUH_DC16_KSH0_LDG0_0057',
    'SNUH_DC16_KSH0_LDG0_0058',
    'SNUH_DC16_KSH0_LDG0_0070',
    'SNUH_DC16_KSH0_LDG0_0074',
    'SNUH_DC16_KSH0_LDG0_0078',
    'SNUH_DC16_KSH0_LDG0_0080',
    'SNUH_DC16_YHG0_LDG0_0017',    
    'SNUH_DC16_YHG0_LDG0_0018',    
    'SNUH_DC16_YHG0_LDG0_0020',    
]

path = r'Z:\preprocessing\data\model_test_4thdata\yolo_format'
path_to = r'Z:\preprocessing\dataset\model_test_4thdataset\yolo_format'

os.makedirs(os.path.join(path_to, 'train/images'), exist_ok=True)
os.makedirs(os.path.join(path_to, 'train/labels'), exist_ok=True)
os.makedirs(os.path.join(path_to, 'val/images'), exist_ok=True)
os.makedirs(os.path.join(path_to, 'val/labels'), exist_ok=True)

path_train_img = os.path.join(path_to, 'train/images')
path_train_labels = os.path.join(path_to, 'train/labels')
path_val_img = os.path.join(path_to, 'val/images')
path_val_labels = os.path.join(path_to, 'val/labels')

list_folder = [folder_ for folder_ in os.listdir(path) if os.path.isdir(os.path.join(path, folder_))]

for folder_ in list_folder:
    path_folder = os.path.join(path, folder_)
    list_png = [file_ for file_ in os.listdir(path_folder) if file_.endswith('png')]
    
    print(list_train)
    if folder_ in list_train:
        for png_ele in list_png:
            path_png = os.path.join(path_folder, png_ele)
            path_text = path_png[:-3] + 'txt'

            if os.path.isfile(path_png) and os.path.isfile(path_text):
                shutil.copy(path_png, os.path.join(path_train_img, png_ele))
                shutil.copy(path_text, os.path.join(path_train_labels, png_ele)[:-3] + 'txt')
                print(path_png)
                print(path_text)
                
    if folder_ in list_val:
        for png_ele in list_png:
            path_png = os.path.join(path_folder, png_ele)
            path_text = path_png[:-3] + 'txt'

            if os.path.isfile(path_png) and os.path.isfile(path_text):
                shutil.copy(path_png, os.path.join(path_val_img, png_ele))
                shutil.copy(path_text, os.path.join(path_val_labels, png_ele)[:-3] + 'txt')
                print(path_png)
                print(path_text)
                
