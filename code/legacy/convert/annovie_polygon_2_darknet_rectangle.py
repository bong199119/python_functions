import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import argparse

### 변수 설명 ###
### path : annovie(개별 polygon)파일이 들어있는 폴더 path ###
### output_path : darknet xml파일을 받을 폴더 path ###

### 사용예시 ###
### python annovie_polygon_2_darknet_rectangle.py <path> <output_path> ###

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def make_xml_list(path):
    list_file = os.listdir(path)
    list_xml = [file for file in list_file if file.endswith('xml')]
    return list_xml

def parse_annovie_xml(path, xml):
    dict_for_rectengle = {}
    dict_for_header = {}
    list_names = []
    list_ids = []
    list_point_set = []
    file = open(os.path.join(path, xml), 'rt', encoding='UTF8')
    tree = ET.parse(file)
    root = tree.getroot()

    text_folder = root.findtext('folder')
    text_filename = root.findtext('filename')
    text_path = root.findtext('path')

    list_size = root.findall('size')
    text_width = list_size[0].findtext('width')
    text_height = list_size[0].findtext('height')
    text_depth = list_size[0].findtext('depth')
    dict_for_header['folder'] = text_folder
    dict_for_header['filename'] = text_filename
    dict_for_header['width'] = text_width
    dict_for_header['height'] = text_height
    dict_for_header['depth'] = text_depth

    list_object = root.findall('object')
    for object_ in list_object:
        text_name = object_.findtext('name')
        text_id = object_.findtext('id')
        list_points = object_.findall('points')
        text_xpoints = list_points[0].findall('x')
        text_ypoints = list_points[0].findall('y')
        list_xpoints = []
        list_ypoints = []
        for i, text_xpoint in enumerate(text_xpoints):
            list_xpoints.append(float(text_xpoint.text))
            list_ypoints.append(float(text_ypoints[i].text))

        max_xpoints = max(list_xpoints)
        min_xpoints = min(list_xpoints)
        max_ypoints = max(list_ypoints)
        min_ypoints = min(list_ypoints)

        list_names.append(text_name)
        list_point_set.append([max_xpoints, min_xpoints, max_ypoints, min_ypoints])

    return list_names, list_point_set, dict_for_header

def make_darknet_xml(list_names, list_point_set, dict_for_header, output_path):
    
    text_folder = dict_for_header['folder']
    text_filename = dict_for_header['filename'][:-4]
    text_width = dict_for_header['width']
    text_height = dict_for_header['height']
    text_depth = dict_for_header['depth']

    element_filename = text_filename + '.jpg'
    element_path = './'+element_filename

    root = Element('annotation')
    SubElement(root, 'folder').text = text_folder
    SubElement(root, 'filename').text = element_filename
    SubElement(root, 'path').text = element_path
    source = SubElement(root, 'source')
    SubElement(source, 'database').text = 'Unknown'

    size = SubElement(root, 'size')
    SubElement(size, 'width').text = text_width
    SubElement(size, 'height').text = text_height
    SubElement(size, 'depth').text = text_depth
    SubElement(root, 'segmented').text = '0'

    for i, list_name in enumerate(list_names):
        obj = SubElement(root, 'object')
        SubElement(obj, 'name').text = list_name
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = '0'
        bndbox = SubElement(obj, 'bndbox')
        
        xmin = list_point_set[i][1]
        ymin = list_point_set[i][3]
        xmax = list_point_set[i][0]
        ymax = list_point_set[i][2]
        
        if xmin < 0 :
            xmin = 0
        if ymin < 0 :
            ymin = 0
        if xmax > float(text_width):
            xmax = float(text_width)
        if ymax > float(text_height):
            ymax = float(text_height)
        
        SubElement(bndbox, 'xmin').text = str(xmin)
        SubElement(bndbox, 'ymin').text = str(ymin)
        SubElement(bndbox, 'xmax').text = str(xmax)
        SubElement(bndbox, 'ymax').text = str(ymax)
        
    indent(root)
    tree = ElementTree(root)
    tree.write(output_path + '/' + text_filename +'.xml')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('output_path')    
    args = parser.parse_args()

    path = args.path
    output_path = args.output_path

    list_xml = make_xml_list(path)

    for xml in list_xml:
        list_names, list_point_set, dict_for_header = parse_annovie_xml(path, xml)
        make_darknet_xml(list_names, list_point_set,  dict_for_header, output_path)

if __name__ == "__main__":
    main()