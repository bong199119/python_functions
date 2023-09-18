import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
from PIL import ImageColor,Image, ExifTags
from random import shuffle

path_annovie_dataset = r''
path_u2net_dataset = r''
list_annovie_xml = [file_ for file_ in os.listdir(path_annovie_dataset) if file_.endswith('xml')]

path_to_img_foler = os.path.join(path_u2net_dataset, 'img')
path_to_mask_folder = os.path.join(path_u2net_dataset, 'mask')

os.makedirs(path_to_img_foler, exist_ok=True)
os.makedirs(path_to_mask_folder, exist_ok=True)

clr_dict = {
    "":"#ffffff" # object name : color 
}

for annovie_xml in list_annovie_xml:
    path_xml = os.path.join(path_annovie_dataset, annovie_xml)
    path_img = path_xml[:-3] + 'png'

    path_to_img = os.path.join(path_to_img_foler, annovie_xml[:-3] + 'png')
    path_to_mask = os.path.join(path_to_mask_folder, annovie_xml[:-3] + 'png')

    tree=ET.parse(path_xml)
    root = tree.getroot()
    root_size=root.findall("size")
    img_real = Image.open(path_img)
    img_real.load()
    width,height=img_real.size

    depth=int(3)
    mask = np.zeros((height, width, depth), dtype=np.uint8)
    shapes=root.findall("object")
    if shapes == []:continue

    for shape in shapes:
        name=shape.findtext("name")
        if name != '':continue # object name
        clr = shape.findtext("clr")
        type=shape.findtext("type")
        clr=shape.findtext("clr")
        if len(clr) == 9:
            clr = clr[0] + clr[3:]
        clr = clr_dict.get(name)
        points=shape.findall("points")
        data_x=points[0].findall("x")
        data_y=points[0].findall("y")

        r=[]
        c=[]
        for point_x, point_y in zip(data_x,data_y):
            r.append((int(float(point_x.text)),int(float(point_y.text))))

        RGB=ImageColor.getcolor(clr,"RGB")
        if type=="poly":
            cv2.fillPoly(mask,[np.asarray(r)],RGB,cv2.LINE_AA)
        elif type=="rect":
            cv2.rectangle(mask,np.asarray(r)[0],(np.asarray(r)[0][0]+np.asarray(r)[1][0],np.asarray(r)[0][1]+np.asarray(r)[1][1]),RGB,cv2.FILLED)

    small_mask=cv2.resize(mask,(384,256))
    small_img_real=cv2.resize(np.asarray(img_real),(384,256))
    hsv = cv2.cvtColor(small_mask, cv2.COLOR_BGR2HSV)
    small_img_real=Image.fromarray(small_img_real).save(path_to_img, format="png")
    small_mask=Image.fromarray(small_mask).save(path_to_mask, format="png")
    print(path_to_img)
    print(path_to_mask)
    