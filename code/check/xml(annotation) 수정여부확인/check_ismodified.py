import os
import xml.etree.ElementTree as ET
import time
import pandas as pd

path_1 = r'D:\code\xml수정여부확인\data\수정전'
path_2 = r'D:\code\xml수정여부확인\data\수정후'
path_to = r'D:\code\xml수정여부확인\code\test.csv'

list_path_1 = [xml_ for xml_ in os.listdir(path_1) if xml_.endswith('xml')]
# list_path_2 = [xml_ for xml_ in os.listdir(path_2) if xml_.endswith('xml')]

list_xmlname = []
list_ismodified = []

modified = ''
for xml_ in list_path_1:
    path_xml1 = os.path.join(path_1, xml_)
    path_xml2 = os.path.join(path_2, xml_)

    file1 = open(path_xml1, encoding='UTF8')
    if os.path.isfile(path_xml2):
        file2 = open(path_xml2, encoding='UTF8')
    else:
        print(path_xml2, ' not exist')
        pass
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    root_obj1 = root1.findall('object')
    root_obj2 = root2.findall('object')
    list_obj1 = []
    list_obj2 = []

    for obj_ in root_obj1:
        list_tmp = []
        name = obj_.findall('name')
        list_tmp.append(name[0].text)

        points = obj_.findall('points')
        list_x = points[0].findall('x')
        list_y = points[0].findall('y')

        for point_x in list_x:
            list_tmp.append(point_x.text)

        for point_y in list_y:
            list_tmp.append(point_y.text)
            
        list_obj1.append(list_tmp)

    for obj_ in root_obj2:
        list_tmp = []
        name = obj_.findall('name')
        list_tmp.append(name[0].text)

        points = obj_.findall('points')
        list_x = points[0].findall('x')
        list_y = points[0].findall('y')

        for point_x in list_x:
            list_tmp.append(point_x.text)

        for point_y in list_y:
            list_tmp.append(point_y.text)
            
        list_obj2.append(list_tmp)

    # list_obj1, list_obj2 비교
    if list_obj1 == list_obj2: # 수정이 전혀 없는 경우
        modified = 'no'

    elif len(list_obj1) == len(list_obj2): # annotation 정보는 동일하나, 순서가 바뀐경우 실질적 수정이라고 생각하지 않음
        for idx in range(len(list_obj1)):
            if list_obj1[idx] in list_obj2:
                list_obj2.remove(list_obj1[idx])
            else:
                modified = 'yes'
                break

        if len(list_obj2) == 0:
            modified = 'no'

    else: # 수정된 경우
        modified = 'yes'

    print(xml_, ' modified : ',modified)
    list_xmlname.append(xml_)
    list_ismodified.append(modified)


df = pd.DataFrame(columns = ['xmlname','ismodified'])
df['xmlname'] = list_xmlname
df['ismodified'] = list_ismodified
df.to_csv(path_to)