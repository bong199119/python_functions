#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree


# In[ ]:


def indent(elem, level=0): #자료 출처 https://goo.gl/J8VoDK
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


# In[ ]:


def parse_mtegxml(file_path, file_first_name):
    dict_for_PolyXml = {}
    list_for_PolyXml_temp = []
    xmldoc = minidom.parse(file_path)
    itemlists = xmldoc.getElementsByTagName('LabelItems')
    ListLabels = xmldoc.getElementsByTagName('ListLabels')
    
    width = ListLabels[0].getElementsByTagName('imgW')[0].firstChild.data
    height = ListLabels[0].getElementsByTagName('imgH')[0].firstChild.data
    
    dict_for_PolyXml['width'] = width
    dict_for_PolyXml['height'] = height
    
    for itemlist in itemlists:
        list_name = []
        list_IP_total = []
        if itemlist.getElementsByTagName('name')[0].getElementsByTagName('string') != []:
            index = file_first_name + '0'*(8-len(itemlist.getElementsByTagName('idx')[0].firstChild.data)) + str(int(itemlist.getElementsByTagName('idx')[0].firstChild.data)+2)+'.png'    
            
            for name in itemlist.getElementsByTagName('name')[0].getElementsByTagName('string'):
                list_name.append(name.firstChild.data)
                
            # shape == depth?    
            shape = itemlist.getElementsByTagName('shape')[0].getElementsByTagName('int')[0].firstChild.data
            
            for ArrayPoint in itemlist.getElementsByTagName('lp')[0].getElementsByTagName('ArrayOfPoint'):
                list_IP_temp = []
                for Point in ArrayPoint.getElementsByTagName('Point'):
                    list_IP_temp.append(Point.getElementsByTagName('X')[0].firstChild.data)
                    list_IP_temp.append(Point.getElementsByTagName('Y')[0].firstChild.data)
                list_IP_total.append(list_IP_temp)
                
            list_for_PolyXml_temp.append({'file_name':index,
                                         'name':list_name, 
                                         'IP':list_IP_total,
                                         'shape':shape})
    dict_for_PolyXml['index'] = list_for_PolyXml_temp
    
    return dict_for_PolyXml


# In[ ]:


def make_polyxml(dict_for_PolyXml, output_path):
    
    for PolyXml in dict_for_PolyXml['index']:
        
        root = Element('annotation')
        SubElement(root, 'folder').text = 'custom'
        SubElement(root, 'filename').text = PolyXml['file_name']
        SubElement(root, 'path').text = ''
        source = SubElement(root, 'source')
        SubElement(source, 'database').text = 'Unknown'

        size = SubElement(root, 'size')
        SubElement(size, 'width').text = dict_for_PolyXml['width']
        SubElement(size, 'height').text = dict_for_PolyXml['height']
        SubElement(size, 'depth').text = PolyXml['shape']

        SubElement(root, 'segmented').text = '0'
        for i in range(len(PolyXml['name'])):
            obj = SubElement(root, 'object')
            SubElement(obj, 'name').text = PolyXml['name'][i]
            SubElement(obj, 'pose').text = 'Unspecified'
            SubElement(obj, 'truncated').text = '0'
            SubElement(obj, 'difficult').text = '0'
            segmentation = SubElement(obj, 'segmentation')
            for k in range(int(len(PolyXml['IP'][i])/2)):
                Point = SubElement(segmentation, 'Point')
                SubElement(Point, 'X').text = PolyXml['IP'][i][k*2]
                SubElement(Point, 'Y').text = PolyXml['IP'][i][k*2+1]
            
            indent(root)
            tree = ElementTree(root)
            tree.write(output_path + '/' + PolyXml['file_name'][:-3] +'xml')
    

