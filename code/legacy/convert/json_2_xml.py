#!/usr/bin/env python
# coding: utf-8

# In[195]:


import os
import xml.etree.ElementTree as ET
import json
from xml.etree.ElementTree import Element, SubElement
import numpy as np


# In[114]:


root = 'C:\\Users\\mteg\\Desktop\\aaaa0012_2020042503'


# In[115]:


output = 'C:\\Users\\mteg\\Desktop\\new'


# In[117]:


def make_list_json(root):
    file_list = os.listdir(root)
    
    list_json = []
    for file in file_list:
        if file[-4:] == 'json':
            list_json.append(file)
            
    return list_json


# In[196]:


def open_json(root, filename):
    try: 
        with open(root+'/'+filename, encoding = 'UTF-8') as json_file:
                    json_data = json.load(json_file)
                
    except:
        print('디코드에러. 빈파일인지 확인하세요.')
        return 0
    
    return json_data


# In[228]:


def min_max_extraction(json_data, i):
    x_location = []
    y_location = []
    location_list = []
    
    if json_data['shapes'] != [] :
        for location in json_data['shapes'][i]['points']:
            x_location.append(location[0])
            y_location.append(location[1])

        x_min = str(np.min(x_location))
        x_max = str(np.max(x_location))
        y_min = str(np.min(y_location))
        y_max = str(np.max(y_location))

        location_list.append([x_min, x_max, y_min, y_max])
        return location_list
    
    else:
        return 1


# In[225]:


def change2_pascal_voc(output, filename, json_data):
    root = Element('annotation')
    SubElement(root, 'folder').text = 'custom'
    SubElement(root, 'filename').text = filename[:-4] + 'png'
    SubElement(root, 'path').text = 'C:\\Users\\mteg\\Desktop\\aaaa0012_2020042503' + '/' +  filename[:-4] + 'png'
    source = SubElement(root, 'source')
    SubElement(source, 'database').text = 'Unknown'

    size = SubElement(root, 'size')
    SubElement(size, 'width').text = str(json_data['imageWidth'])
    SubElement(size, 'height').text = str(json_data['imageHeight'])
    SubElement(size, 'depth').text = '3'

    SubElement(root, 'segmented').text = '0'
    for i in range(len(json_data['shapes'])):
        location_list = min_max_extraction(json_data, i)
        if location_list != 1:
            obj = SubElement(root, 'object')
            SubElement(obj, 'name').text = json_data['shapes'][i]['label']
            SubElement(obj, 'pose').text = 'Unspecified'
            SubElement(obj, 'truncated').text = '0'
            SubElement(obj, 'difficult').text = '0'
            bbox = SubElement(obj, 'bndbox')
            SubElement(bbox, 'xmin').text = location_list[0][0]
            SubElement(bbox, 'ymin').text = location_list[0][2]
            SubElement(bbox, 'xmax').text = location_list[0][1]
            SubElement(bbox, 'ymax').text = location_list[0][3]                                                        
            tree = ElementTree(root)
            tree.write(output + '/' + filename[:-4] +'xml')


# In[229]:


def main():
    list_json = make_list_json(root)
    for filename in list_json:
        json_data = open_json(root, filename)
        if json_data != 0:
                change2_pascal_voc(output, filename, json_data)
    print('done!')


# In[242]:


main()


# In[ ]:




