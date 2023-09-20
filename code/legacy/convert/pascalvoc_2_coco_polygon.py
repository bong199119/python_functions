import random
import os
import json
import xml.etree.ElementTree as ET
import numpy as np
from shapely.geometry import Polygon, MultiPolygon

train_root = ''
valid_root = ''

train_folder = os.listdir(train_root)
valid_folder = os.listdir(valid_root)

# make xml list
list_train_xml = []
list_valid_xml = []

for file in train_folder:
    if file[-3:] == 'xml':
        list_train_xml.append(file)
        
for file in valid_folder:
    if file[-3:] == 'xml':
        list_valid_xml.append(file)

# 신발끈 이론 : 면적 계산
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

# dict_class 제작
def collect_categories(list_xml, path):
    dict_class = {}
    i = 1
    for file_xml in list_xml:
        file = open(os.path.join(path,file_xml), 'rt', encoding='UTF8')
        tree = ET.parse(file)
        root = tree.getroot()
        root_obj = root.findall("object")
        
        if root_obj != []:
            root_bnd  = root_obj[0].findtext('name')
            if root_bnd not in  dict_class:
                dict_class[root_bnd] = i
                i += 1

    return dict_class


# annotation 항목 제작
def create_image_annotaion(list_xml, path):
    id = 0
    images =[]
    
    for file_xml in list_xml:
        
        file = open(os.path.join(path,file_xml), 'rt', encoding='UTF8')
        tree = ET.parse(file)
        root = tree.getroot()
        root_size = root.findall("size")
        width = int(root_size[0].findtext("width"))
        height = int(root_size[0].findtext("height"))
        
        image ={
            'file_name':file_xml[:-3]+'png',
            'width' : width,
            'height': height,
            'id': id
        }
        
        id += 1
        images.append(image)

    return images

# 
def create_annotation(list_xml, dict_class, path):
    
    annotations = []
    is_crowd = 0
    image_id = 0
    annotation_id = 0
        
    
    for file_xml in list_xml:


        file = open(os.path.join(path, file_xml), 'rt', encoding='UTF8')
        tree = ET.parse(file)
        root = tree.getroot()
        root_obj = root.findall("object")

        for obj in root_obj:
            segmentations= []
            name = obj.findtext('name')
        #             root_segmentation = obj.findall('segmentation')
            root_Point = obj.findall('points')
            segmentation = []
            segmentation_x = []
            segmentation_y = []
            list_x = []
            list_y = []

            for Point in root_Point:            
                for xpoint in root_Point[0].findall('x'):
                    X = float(xpoint.text)
                    segmentation_x.append(X)
                    list_x.append(X)

                for ypoint in root_Point[0].findall('y'):
                    Y = float(ypoint.text)
                    segmentation_y.append(Y)
                    list_y.append(Y)
    
            for index, x in enumerate(segmentation_x):
                segmentation.append(x)
                segmentation.append(segmentation_y[index])
            
            xmax = np.array(list_x).max()
            xmin = np.array(list_x).min()
            ymax = np.array(list_y).max()
            ymin = np.array(list_y).min()

            segmentations.append(segmentation)
            area = PolyArea(list_x,list_y)

            width = xmax - xmin
            height = ymax - ymin
            bbox = (xmin, ymin, width, height)


            annotation = {
                'segmentation': segmentations,
                'iscrowd': is_crowd, 
                'image_id': image_id, 
                'category_id': dict_class[name],
                'id': annotation_id,
                'bbox': bbox,
                'area': area
            }

            annotations.append(annotation)
        image_id += 1

    return annotations

# 
def make_annotation_file(annotation, images, dict_class, output_path):
    
    annotations ={
        'annotations' : annotation,
        'images' : images,
    }
    
    annotations['categories'] = []
    
    for class_ in dict_class.keys():
        annot = {
            'id' : dict_class[class_],
            'name' : class_
        }
        annotations['categories'].append(annot)
    
    with open(output_path,'w',encoding = 'utf-8') as make_file:
        json.dump(annotations,make_file,ensure_ascii=False,indent="\t")
    

train_output_path = ''
valid_output_path = ''

dict_class = collect_categories(list_train_xml, train_root)

train_images = create_image_annotaion(list_train_xml, train_root)
valid_images = create_image_annotaion(list_valid_xml, valid_root)

train_annotations = create_annotation(list_train_xml, dict_class, train_root)
valid_annotations = create_annotation(list_valid_xml, dict_class, valid_root)

make_annotation_file(train_annotations, train_images, dict_class, train_output_path)
make_annotation_file(valid_annotations, valid_images, dict_class, valid_output_path)