import os
import xml.etree.ElementTree as ET
import time
import pandas as pd

path = r'Z:\preprocessing\data'
list_folder = os.listdir(path)
for folder_ in list_folder:
    path_folder = os.path.join(path, folder_)
    list_img = [png_ for png_ in os.listdir(path_folder) if png_.endswith('png')]

    for img_ in list_img:
        xml_ = img_[:-3] + 'xml'
        path_xml = os.path.join(path_folder, xml_)
        path_img = os.path.join(path_folder, img_)

        if not os.path.isfile(path_xml):
            os.remove(path_img)

        else:
            file1 = open(path_xml, encoding='UTF8')
            tree1 = ET.parse(file1)
            root1 = tree1.getroot()
            root_obj1 = root1.findall('object')
            file1.close()
            
        if root_obj1 == []:
            print(path_xml)
            print(path_img)
            os.remove(path_xml)
            os.remove(path_img)
