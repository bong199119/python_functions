import cv2
import os
import numpy as np
import PIL
from PIL import Image
import tqdm
import time
import shutil


time_start =  time.time()
path = r'D:\project\image_similarity\image'
list_images = os.listdir(path)
list_sameImage = []
dict_image_load = {}
for image in tqdm.tqdm(list_images):
    path_image = os.path.join(path, image)
    img_1 = Image.open(path_image)
    image_read = np.array(img_1)
    dict_image_load[image] = image_read

print('finish load data')
for im1 in dict_image_load:
    for im2 in dict_image_load:
        try:
            if (dict_image_load[im1] == dict_image_load[im2]).all() and (im1 != im2):
                print('같은 이미지 pair',im1, im2)
                if [im1, im2] not in list_sameImage and [im2, im1] not in list_sameImage:
                    list_sameImage.append([im1, im2])
        except:
            print(im1, im2)

time_end =  time.time()
print(list_sameImage)
print(time_end - time_start)


os.mkdir(os.path.join(path, 'sameImage'))

for sameImage in list_sameImage:
    for sI in sameImage:
        filename = sI.split('\\')[-1]
        shutil.move(os.path.join(path, filename), os.path.join(os.path.join(path, 'sameImage'),filename))


f = open(os.path.join(path, 'list_sameImage.txt'), 'w', encoding = 'utf-8')

for sameImage in list_sameImage:
    
    f.write(str("['이미지','이미지']: "))
    f.write(str(sameImage))
    f.write(str('\n'))

f.close()