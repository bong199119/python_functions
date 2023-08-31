import os
import cv2
import json
import numpy as np

def cordinate_annovie2cv2polylines(annovie_points):
    list_cordinate = []
    for points in annovie_points:
        x = points['x']
        y = points['y']
        list_cordinate.append([x, y])

    list_cordinate = np.array(list_cordinate, dtype=np.int32)
    return list_cordinate

def hex2RGB(color_hex):
    color_hex = color_hex.lstrip('#')
    color_RGB = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    return color_RGB

# for find extension
tuple_extention_forimg = tuple(['png', 'jpg'])
path = r'D:\code\image_combine\origin-overlapping pair sample'
paht_to_save = r'D:\code\image_combine\origin-overlapping pair sample save'
alpha = 0.8 # 높을수록 라벨링 투명도가 높음

list_images = [file for file in  os.listdir(path) if file.endswith(tuple_extention_forimg)]
os.makedirs(paht_to_save, exist_ok=True)

for image in list_images:
    path_image = os.path.join(path, image)
    paht_to_save_image = os.path.join(paht_to_save, image)
    try:
        path_json = os.path.join(path, image[:-3]+'json')
        with open(path_json, "r", encoding = 'utf-8') as _json:
            json_forimg = json.load(_json)

    except:
        print(f'there is no json for {image}')
    
    annotations = json_forimg['annotations']
    img_read = cv2.imread(path_image, cv2.IMREAD_COLOR)
    img_origin = cv2.imread(path_image, cv2.IMREAD_COLOR)
    for annotation in annotations:

        cordinate_annotation = annotation['points']
        color_annotation = annotation['color']
        cordinate_forcv2 = cordinate_annovie2cv2polylines(cordinate_annotation)
        color_RGB = hex2RGB(color_annotation)

        img_read = cv2.fillPoly(img_read, [cordinate_forcv2], color_RGB)
        # cv2.imshow('cv2.addWeighted', img_read)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    dst  = cv2.addWeighted(img_origin, alpha, img_read, (1-alpha), 0) 
    dst_added = cv2.hconcat([img_origin,dst])
    cv2.imwrite(paht_to_save_image, dst_added)