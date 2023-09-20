import random
import os
import json
import xml.etree.ElementTree as ET
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
import argparse


def read_categories(class_names_path): # json파일내의 categories항목 작성하기 위해 class파악
    dict_class = {}

    f = open(class_names_path)
    lines = f.readlines()
    f.close()
    
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
        if lines[i] not in dict_class:
            dict_class[lines[i]] = i+1 # class id는 1부터
            i += 1
                
    return dict_class


def create_image_annotaion(list_xml, dict_xml_img, path):
    id = 0
    images =[]
    
    for file_xml in list_xml:
        
        file = open(os.path.join(path,file_xml),'rt', encoding='UTF8')
        tree = ET.parse(file)
        root = tree.getroot()
        root_size = root.findall("size")
        width = int(root_size[0].findtext("width"))
        height = int(root_size[0].findtext("height"))
        
        image ={
            # 'file_name':file_xml[:-3]+'jpg',
            'file_name': dict_xml_img[file_xml],
            'width' : width,
            'height': height,
            'id': id
        }
        
        id += 1
        images.append(image)

    return images


def create_annotation(list_xml, dict_class, path):
    
    annotations = []
    is_crowd = 0
    image_id = 0
    annotation_id = 0
    
    for file_xml in list_xml:
        
        
        file = open(os.path.join(path, file_xml),'rt', encoding='UTF8')
        tree = ET.parse(file)
        root = tree.getroot()
        root_obj = root.findall("object")
        
        
        for obj in root_obj:
            segmentations= []
            name = obj.findtext('name')
            root_Point = obj.findall('points')
            root_x_point = root_Point[0].findall('x')
            root_y_point = root_Point[0].findall('y')
            segmentation = []
            list_x = []
            list_y = []
            
            for point_x, point_y in zip(root_x_point, root_y_point): 
                X = float(point_x.text)
                Y = float(point_y.text)
                segmentation.append(X)
                segmentation.append(Y)
                list_x.append(X)
                list_y.append(Y)            
            xmax = np.array(list_x).max()
            xmin = np.array(list_x).min()
            ymax = np.array(list_y).max()
            ymin = np.array(list_y).min()
            
            segmentations.append(segmentation)
            area = PolyArea(list_x,list_y)
            
            width = xmax - xmin
            height = ymax - ymin
            bbox = (xmin, ymin, width, height)

            if name in dict_class:
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

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

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
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('class_names_path')
    parser.add_argument('train_root')
    parser.add_argument('valid_root')
    parser.add_argument('train_output_path')
    parser.add_argument('valid_output_path')
    args = parser.parse_args()

    class_names_path = args.class_names_path
    train_root = args.train_root
    valid_root = args.valid_root
    train_output_path = args.train_output_path
    valid_output_path = args.valid_output_path


    train_folder = os.listdir(train_root)
    valid_folder = os.listdir(valid_root)

    dict_xml_img = {}
    list_train_xml = []
    list_valid_xml = []
    list_train_img = []
    list_valid_img = []

    for file in train_folder:
        if file.endswith('xml'):
            list_train_xml.append(file)
        elif not file.endswith('xml'):
            list_train_img.append(file)
            
    for file in valid_folder:
        if file.endswith('xml'):
            list_valid_xml.append(file)
        elif not file.endswith('xml'):
            list_valid_img.append(file)


    for file in train_folder:
        if file.endswith('xml') and file not in dict_xml_img:
            dict_xml_img[file] = ''
            for img in list_train_img:
                if file[:-3] == img[:-3]:
                    dict_xml_img[file] = img

    for file in valid_folder:
        if file.endswith('xml') and file not in dict_xml_img:
            dict_xml_img[file] = ''
            for img in list_valid_img:
                if file[:-3] == img[:-3]:
                    dict_xml_img[file] = img

    dict_class = read_categories(class_names_path)
    train_images = create_image_annotaion(list_train_xml, dict_xml_img, train_root)
    valid_images = create_image_annotaion(list_valid_xml, dict_xml_img, valid_root)
    
    train_annotations = create_annotation(list_train_xml, dict_class, train_root)
    valid_annotations = create_annotation(list_valid_xml, dict_class, valid_root)

    make_annotation_file(train_annotations, train_images, dict_class, train_output_path)
    make_annotation_file(valid_annotations, valid_images, dict_class, valid_output_path)


if __name__ == "__main__":
    main()