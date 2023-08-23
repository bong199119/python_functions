import os
import xml.etree.ElementTree as ET
import time
import pandas as pd


path = r'Z:\preprocessing\data\annovie_format'
# path = r'Z:\preprocessing\data\test_format\test'
path_to = r'Z:\preprocessing\data\labelimg_format'

list_folder = os.listdir(path)
for folder_ in list_folder:
    path_folder = os.path.join(path, folder_)
    path_to_folder = os.path.join(path_to, folder_)

    if not os.path.isdir(path_to_folder):
        os.mkdir(path_to_folder)

    list_img = [png_ for png_ in os.listdir(path_folder) if png_.endswith('png')]

    for img_ in list_img:
        xml_ = img_[:-3] + 'xml'
        path_xml = os.path.join(path_folder, xml_)
        path_to_xml = os.path.join(path_to_folder, xml_)
        path_img = os.path.join(path_folder, img_)

        file1 = open(path_xml, encoding='UTF8')
        tree1 = ET.parse(file1)
        root1 = tree1.getroot()
        name_folder = root1.findall('folder')[0].text
        name_filename = root1.findall('filename')[0].text
        name_path = root1.findall('path')[0].text
        info_size = root1.findall('size')

        size_width = info_size[0].findall('width')[0].text
        size_height = info_size[0].findall('height')[0].text
        size_depth = info_size[0].findall('depth')[0].text

        root_obj = root1.findall('object')

        dict_obj = {}
        for obj_ele in root_obj:
            obj_name = obj_ele.findall('name')[0].text
            obj_points = obj_ele.findall('points')

            x1 = obj_points[0].findall('x')[0].text
            y1 = obj_points[0].findall('y')[0].text
            x2 = obj_points[0].findall('x')[1].text
            y2 = obj_points[0].findall('y')[1].text

            # coordinate transform
            xmin = x1
            ymin = y1
            xmax = float(x1) + float(x2)
            ymax = float(y1) + float(y2)

            dict_obj[obj_ele] = {}
            dict_obj[obj_ele]['name'] = obj_name
            dict_obj[obj_ele]['xmin'] = xmin
            dict_obj[obj_ele]['ymin'] = ymin
            dict_obj[obj_ele]['xmax'] = xmax
            dict_obj[obj_ele]['ymax'] = ymax

        root_new = ET.Element('annotation')
        ET.SubElement(root_new, 'folder').text = name_folder
        ET.SubElement(root_new, 'filename').text = name_filename[:-3] + 'png'
        ET.SubElement(root_new, 'path').text = os.path.join(name_path,name_filename[:-3] + 'png')
        source = ET.SubElement(root_new, 'source')
        ET.SubElement(source, 'database').text = 'Unknown'

        size = ET.SubElement(root_new, 'size')
        ET.SubElement(size, 'width').text = str(size_width)
        ET.SubElement(size, 'height').text = str(size_height)
        ET.SubElement(size, 'depth').text = str(size_depth)

        ET.SubElement(root_new, 'segmented').text = '0'

        for obj_ele in root_obj:
            obj = ET.SubElement(root_new, 'object')
            ET.SubElement(obj, 'name').text = dict_obj[obj_ele]['name']
            ET.SubElement(obj, 'pose').text = 'Unspecified'
            ET.SubElement(obj, 'truncated').text = '0'
            ET.SubElement(obj, 'difficult').text = '0'
            bbox = ET.SubElement(obj, 'bndbox')
            ET.SubElement(bbox, 'xmin').text = str(dict_obj[obj_ele]['xmin'])
            ET.SubElement(bbox, 'ymin').text = str(dict_obj[obj_ele]['ymin'])
            ET.SubElement(bbox, 'xmax').text = str(dict_obj[obj_ele]['xmax'])
            ET.SubElement(bbox, 'ymax').text = str(dict_obj[obj_ele]['ymax'])

        tree = ET.ElementTree(root_new)
        print(path_to_xml)
        tree.write(path_to_xml)
