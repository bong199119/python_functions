import os
import xml.etree.ElementTree as ET
import time
import pandas as pd
import shutil


# path = r'Z:\preprocessing\data\model_test_4thdata\annovie_format'
# path_to = r'Z:\preprocessing\data\model_test_4thdata\yolo_format'
path = r'Z:\preprocessing\data\bleeding\annovie_format'
path_to = r'Z:\preprocessing\data\bleeding\yolo_format'
path_classlist = os.path.join(path_to, 'classes.txt')

dict_classes = {}
index = 0
list_folder = os.listdir(path)

for folder_ in list_folder:
    path_folder = os.path.join(path, folder_)
    path_to_folder = os.path.join(path_to, folder_)

    if not os.path.isdir(path_to_folder):
        os.makedirs(path_to_folder)
    
    list_img = [png_ for png_ in os.listdir(path_folder) if png_.endswith('png')]

    for img_ in list_img:
        
        filename = img_[:-3]
        xml_ = filename+'xml'
        path_xml = os.path.join(path_folder, xml_)
        path_to_txt = os.path.join(path_to_folder, filename+'txt')
        path_img = os.path.join(path_folder, img_)
        path_to_img = os.path.join(path_to_folder, img_)

        print(path_xml)
        try :
            file1 = open(path_xml, encoding='UTF8')
            tree1 = ET.parse(file1)
            root1 = tree1.getroot()
            root_obj = root1.findall('object')
            info_size = root1.findall('size')

            size_width = float(info_size[0].findall('width')[0].text)
            size_height = float(info_size[0].findall('height')[0].text)
            size_depth = float(info_size[0].findall('depth')[0].text)

            dict_obj = {}
            if root_obj != []:
                for obj_ele in root_obj:
                    obj_name = obj_ele.findall('name')[0].text

                    if obj_name not in dict_classes:
                        dict_classes[obj_name] = index
                        index += 1

                    obj_points = obj_ele.findall('points')

                    x1 = obj_points[0].findall('x')[0].text
                    y1 = obj_points[0].findall('y')[0].text
                    x2 = obj_points[0].findall('x')[1].text
                    y2 = obj_points[0].findall('y')[1].text

                    # coordinate transform
                    xmin = float(x1)
                    ymin = float(y1)
                    xmax = float(x1) + float(x2)
                    ymax = float(y1) + float(y2)

                    x_center = (xmin + xmax) / 2
                    y_center = (ymin + ymax) / 2
                    object_width = xmax - xmin
                    object_height = ymax - ymin

                    x = x_center/size_width
                    y = y_center/size_height
                    w = object_width/size_width
                    h = object_height/size_height

                    dict_obj[obj_ele] = {}
                    dict_obj[obj_ele]['name'] = obj_name
                    dict_obj[obj_ele]['x'] = x
                    dict_obj[obj_ele]['y'] = y
                    dict_obj[obj_ele]['w'] = w
                    dict_obj[obj_ele]['h'] = h

                    f_txt = open(path_to_txt, 'w')
                    for obj_ele in dict_obj:
                        x = dict_obj[obj_ele]['x']
                        y = dict_obj[obj_ele]['y']
                        w = dict_obj[obj_ele]['w']
                        h = dict_obj[obj_ele]['h']
                        obj_name = dict_obj[obj_ele]['name']

                        f_txt.write(f'{dict_classes[obj_name]} {x} {y} {w} {h}')
                        f_txt.write('\n')
                    f_txt.close()
                    print(path_to_txt)

                shutil.copy(path_img, path_to_img)

        except:
            pass

print('dict_classes', dict_classes)
f = open(path_classlist, 'w')
for class_ in dict_classes:
    f.write(class_)
    f.write('\n')
f.close()