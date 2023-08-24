import cv2
import os
import numpy as np
import PIL
from PIL import Image
import tqdm
import time
import shutil


time_start =  time.time()
path = r'D:\project\image_similarity\erro\Bulldogs'
list_images = os.listdir(path)
list_sameImage = []
dict_image_load = {}
data_sippet_num = 4 # 1000장일때 15권장
dict_data_sippet = {}
dict_image_load_compared = {}
list_weird_image = []

# list_images split by data_sippet_num:
for i in range(data_sippet_num):
    list_temp = list_images[round((len(list_images)/data_sippet_num)*i) : round((len(list_images)/data_sippet_num)*(i+1))]
    dict_data_sippet[i] = list_temp

print(dict_data_sippet)

f = open(os.path.join(path, 'list_sameImage.txt'), 'w', encoding = 'utf-8')
f_check = open(os.path.join(path, 'check image.txt'), 'w', encoding = 'utf-8')

for num_sippet in tqdm.tqdm(dict_data_sippet):
    dict_image_load.clear()
    dict_image_load = {}
    print('loading data sippet.. {}'.format(num_sippet))
    for image in tqdm.tqdm(dict_data_sippet[num_sippet]):
        path_image = os.path.join(path, image)
        try:
            img_1 = Image.open(path_image)
            image_read = np.array(img_1)
            dict_image_load[image] = image_read
        except Exception as e:
            list_weird_image.append(image)
            f_check.write(image) 
            f_check.write(' : ') 
            f_check.write(e)
            f_check.write('\n')

    # compare with same sippets
    print('comparing.. same sippets {}'.format(num_sippet))
    print(len(dict_image_load), len(dict_image_load))
    for im1 in tqdm.tqdm(dict_image_load):
        for im2 in dict_image_load:
            try:
                if (dict_image_load[im1] == dict_image_load[im2]).all() and (im1 != im2):
                    print('같은 이미지 pair 11',im1, im2)
                    if [im1, im2] not in list_sameImage and [im2, im1] not in list_sameImage:
                        f.write(str("['이미지','이미지']: "))
                        f.write(str(im1))
                        f.write('\t')
                        f.write(str(im2))
                        f.write(str('\n'))
                        list_sameImage.append([im1, im2])
            except:
                print('{}-{}'.format(num_sippet, num_sippet),im1, im2)

    # load for compare with other sippets
    if num_sippet < data_sippet_num:
        num_sippet_becompared = num_sippet+1
        print('loading compared data sippet.. {}-{}'.format(num_sippet, num_sippet_becompared))
        while num_sippet_becompared < data_sippet_num:
            dict_image_load_compared.clear()
            dict_image_load_compared = {}
            for image_compared in tqdm.tqdm(dict_data_sippet[num_sippet_becompared]):
                path_image = os.path.join(path, image_compared)
                try:
                    img_compared = Image.open(path_image)
                    img_compared_numpy = np.array(img_compared)
                    dict_image_load_compared[image_compared] = img_compared_numpy
                except Exception as e:
                    list_weird_image.append(image)
                    f_check.write(image) 
                    f_check.write(' : ') 
                    f_check.write(e)
                    f_check.write('\n')

            # compare with other sippets
            print('comparing.. with {}-{}'.format(num_sippet, num_sippet_becompared))
            for im1 in tqdm.tqdm(dict_image_load):
                for im2 in dict_image_load_compared:
                    try:
                        if (dict_image_load[im1] == dict_image_load_compared[im2]).all() and (im1 != im2):
                            print('같은 이미지 pair test',im1, im2)
                            if [im1, im2] not in list_sameImage and [im2, im1] not in list_sameImage:
                                list_sameImage.append([im1, im2])
                                f.write(str("['이미지','이미지']: "))
                                f.write(str(im1))
                                f.write('\t')
                                f.write(str(im2))
                                f.write(str('\n'))
                    except:
                        print('{}-{}'.format(num_sippet, num_sippet_becompared), im1, im2)
            num_sippet_becompared += 1

time_end =  time.time()
print(list_sameImage)
print(time_end - time_start)

if not os.path.isdir(os.path.join(path, 'sameImage')):
    os.mkdir(os.path.join(path, 'sameImage'))

f.close()
f_check.close()

for sameImage in list_sameImage:
    for sI in sameImage:
        filename = sI.split('\\')[-1]
        shutil.move(os.path.join(path, filename), os.path.join(os.path.join(path, 'sameImage'),filename))




