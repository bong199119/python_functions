import os
import xml.etree.ElementTree as ET

path_xmlfolder = r"D:\project\python_functions\data\dissector_1"
modified = 'test'

xml_list = [file_ for file_ in os.listdir(path_xmlfolder) if file_.endswith('xml')]

for xml_ in xml_list:
    path_xml = os.path.join(path_xmlfolder, xml_)
    targetXML = open(path_xml, 'rt', encoding='UTF8')
    
    tree = ET.parse(targetXML)
    root = tree.getroot()
    object_tags = root.findall("object")
    for object_tag in object_tags:
        object_name_tag = object_tag.findall('name')

        print(xml_, object_name_tag)
        object_name = object_name_tag[0].text 

        if object_name == 'Dissector':
            object_name_tag[0].text = modified  #수정
      
    tree.write(path_xml)
