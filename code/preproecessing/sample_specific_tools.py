# dissector classid : 5

import os
import time
import shutil

path = r''
path_xmlfolder = r''
path_to = r''


list_folder = [list_ for list_ in os.listdir(path) if os.path.isdir(os.path.join(path,list_))]
print(list_folder)

for folder_ in list_folder:
    path_folder = os.path.join(path, folder_)
    path_xmlfolder_folder = os.path.join(path_xmlfolder, folder_)
    list_txt = [file_ for file_ in os.listdir(path_folder) if file_.endswith('txt')]
    for txt_ in list_txt:
        print(txt_)
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

                
