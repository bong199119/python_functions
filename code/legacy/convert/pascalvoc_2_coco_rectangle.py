import random
import os
import json
import xml.etree.ElementTree as ET

train_root = ''
valid_root = ''

train_folder = os.listdir('')
valid_folder = os.listdir('')

list_train_xml = []
list_valid_xml = []

for file in train_folder:
    if file[-3:] == 'xml':
        list_train_xml.append(file)
        
for file in valid_folder:
    if file[-3:] == 'xml':
        list_valid_xml.append(file)

def collect_categories(list_xml, path):
    dict_class = {}
    i = 1
    for file_xml in list_xml:
        file = open(os.path.join(path,file_xml))
        tree = ET.parse(file)
        root = tree.getroot()
        root_obj = root.findall("object")
        
        if root_obj != []:
            root_bnd  = root_obj[0].findtext('name')
            if root_bnd not in  dict_class:
#                 dict_class.append(root_bnd)
                dict_class[root_bnd] = i
                i += 1

    return dict_class

def create_image_annotaion(list_xml, path):
    id = 0
    images =[]
    
    for file_xml in list_xml:
        file = open(os.path.join(path,file_xml))
        tree = ET.parse(file)
        root = tree.getroot()
        root_size = root.findall("size")
        
        width = float(root_size[0].findtext("width"))
        height = float(root_size[0].findtext("height"))
        
        image ={
            'file_name':file_xml[:-3]+'jpg',
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
        
        
        file = open(os.path.join(path, file_xml))
        tree = ET.parse(file)
        root = tree.getroot()
        root_obj = root.findall("object")
        
        for obj in root_obj:
            segmentations= []
            name = obj.findtext('name')
            root_bndbox = obj.findall('bndbox')
            xmin = float(root_bndbox[0].findtext('xmin'))
            ymin = float(root_bndbox[0].findtext('ymin'))
            xmax = float(root_bndbox[0].findtext('xmax'))
            ymax = float(root_bndbox[0].findtext('ymax'))
            
            segmentation = [xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]
            segmentations.append(segmentation)

            width = xmax - xmin
            height = ymax - ymin
            bbox = (xmin, ymin, width, height)

            area = width*height

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