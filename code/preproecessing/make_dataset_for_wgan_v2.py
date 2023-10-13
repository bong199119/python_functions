import os
import xml.etree.ElementTree as ET

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import ImageColor,Image, ExifTags
from random import shuffle

root_folder=""
destination_folder=""
classes=os.listdir(root_folder)

os.makedirs(os.path.join(destination_folder,"trainA"),exist_ok=True)
os.makedirs(os.path.join(destination_folder,"trainB"),exist_ok=True)
os.makedirs(os.path.join(destination_folder,"testA"),exist_ok=True)
os.makedirs(os.path.join(destination_folder,"testB"),exist_ok=True)

for folder in classes:
    if folder =="original":continue
    if folder =="wgan":continue
    if folder =="nisan":continue
    print(folder)
    # folder="TQIP_06_라벨링데이터"
    folder_path=os.path.join(root_folder,folder)
    files=os.listdir(folder_path)
    total_files=[]
    for file in files:
        extension = file.split(".")[-1]
        if extension == 'xml':continue
        if extension == "json":continue
        if extension == "db":continue
        total_files.append(file)
    total=len(total_files)

    shuffle(total_files)
    # print(total_files)


    # print(train)
    train=total_files[0:int(total*0.8)]
    test=total_files[int(total*0.8):]
    # val=total_files[int(total*0.9):]
    # print(folder,total)
    # print(len(train))
    # print(len(test))
    # print(len(val))
    counter=0
    for file in train:
        extension=file.split(".")[-1]
        filename=file[:-4]
        # if extension !='xml':

        # print(file,filename)
        if filename=="Thumbs":continue
        tree=ET.parse(folder_path+"\\"+filename+".xml")
        root = tree.getroot()
        root_size=root.findall("size")

        img_real = Image.open(folder_path+"\\"+file)
        img_real.load()
        width,height=img_real.size
        # width=int(root_size[0].findtext("width"))
        # height=int(root_size[0].findtext("height"))
        depth=int(root_size[0].findtext("depth"))
        mask = np.zeros((height, width,depth), dtype=np.uint8)
        shapes=root_size=root.findall("object")
        # print(root_size)
        if shapes == []:continue
        # print(shapes)
        for shape in shapes:
            name=shape.findtext("name")
            clr = shape.findtext("clr")
            type=shape.findtext("type")
            # print(name,type)
            # if name in disease:
            clr=shape.findtext("clr")
            # print(clr)
            if len(clr) == 9:
                clr = clr[0] + clr[3:]
            # else:continue
            # clr="#80ff00"
            points=shape.findall("points")
            data_x=points[0].findall("x")
            data_y=points[0].findall("y")


            r=[]
            c=[]
            for point_x, point_y in zip(data_x,data_y):
                r.append((int(float(point_x.text)),int(float(point_y.text))))
                # c.append(height-float(point_y.text))
                # print("y= "+point_y.text)
            # print(clr)
            # rr,cc=polygon(r,c,mask.shape)

            RGB=ImageColor.getcolor(clr,"RGB")
            if type=="poly":
                cv2.fillPoly(mask,[np.asarray(r)],RGB,cv2.LINE_AA)
            # print(r)
            elif type=="rect":
                # print(r)
                cv2.rectangle(mask,np.asarray(r)[0],(np.asarray(r)[0][0]+np.asarray(r)[1][0],np.asarray(r)[0][1]+np.asarray(r)[1][1]),RGB,cv2.FILLED)

        small_mask=cv2.resize(mask,(384,256))
        small_img_real=cv2.resize(np.asarray(img_real),(384,256))


        hsv = cv2.cvtColor(small_mask, cv2.COLOR_BGR2HSV)
        s=hsv[:,:,1]

        nzCount = cv2.countNonZero(s)
        if nzCount<800:continue
 
        small_img_real=Image.fromarray(small_img_real).save(destination_folder+"\\trainA\\"+filename+".png",format="png")
        small_mask=Image.fromarray(small_mask).save(destination_folder+"\\trainB\\"+filename+".png",format="png")

    for file in test:
        extension=file.split(".")[-1]
        # filename=file.split(".")[0]
        filename=file[:-4]
        # if extension !='xml':
        # print(file)

        tree=ET.parse(root_folder+"/"+folder+"/"+filename+".xml")
        root = tree.getroot()
        root_size=root.findall("size")

        img_real = Image.open(root_folder+"/"+folder+"/"+file)
        img_real.load()
        width,height=img_real.size
        depth=int(root_size[0].findtext("depth"))
        mask = np.zeros((height, width,depth), dtype=np.uint8)
        shapes=root_size=root.findall("object")
        # print(root_size)
        if shapes == []:continue
        for shape in shapes:
            name = shape.findtext("name")
            clr = shape.findtext("clr")
            type=shape.findtext("type")

            if len(clr) == 9:
                clr = clr[0] + clr[3:]
            # else: continue
            # clr = "#80ff00"
            points=shape.findall("points")
            data_x=points[0].findall("x")
            data_y=points[0].findall("y")


            r=[]
            c=[]
            for point_x, point_y in zip(data_x,data_y):
                r.append((int(float(point_x.text)),int(float(point_y.text))))

            RGB=ImageColor.getcolor(clr,"RGB")
            if type == "poly":
                cv2.fillPoly(mask, [np.asarray(r)], RGB, cv2.LINE_AA)
                # print(r)
            elif type == "rect":
                # print(r)
                cv2.rectangle(mask, np.asarray(r)[0],
                              (np.asarray(r)[0][0] + np.asarray(r)[1][0], np.asarray(r)[0][1] + np.asarray(r)[1][1]),
                              RGB, cv2.FILLED)
        # print(mask.shape)

        small_mask=cv2.resize(mask,(384,256))
        hsv = cv2.cvtColor(small_mask, cv2.COLOR_BGR2HSV)
        s = hsv[:, :, 1]

        nzCount = cv2.countNonZero(s)
        if nzCount < 800: continue

        small_img_real=cv2.resize(np.asarray(img_real),(384,256))

        # print(file)
        small_img_real=Image.fromarray(small_img_real).save(destination_folder+"/testA/"+filename+".png",format="png")
        small_mask=Image.fromarray(small_mask).save(destination_folder+"/testB/"+filename+".png",format="png")

    # break
