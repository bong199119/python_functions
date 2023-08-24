import cv2
import os
import numpy as np
import PIL
from PIL import Image
import tqdm
import time

time_start = time.time()
path = r'D:\project\image_similarity\images'
list_images = os.listdir(path)
list_sameImage = []
for image in tqdm.tqdm(list_images):
    path_image = os.path.join(path, image)
    # image_read = cv2.imread(path_image)
    img_1 = Image.open(path_image)
    image_read = np.array(img_1)
    for image_becompared in list_images:
        path_image_becompared = os.path.join(path, image_becompared)
        # image_becompared_read = cv2.imread(path_image_becompared)
        img_2 = Image.open(path_image_becompared)
        image_becompared_read = np.array(img_2)

        try:
            if (image_read == image_becompared_read).all() and (image != image_becompared):
                print('같은 이미지 pair',path_image, path_image_becompared)
                if [path_image, path_image_becompared] not in list_sameImage and [path_image_becompared, path_image] not in list_sameImage:
                    list_sameImage.append([path_image, path_image_becompared])

        except:
            print(image, image_becompared)
time_end = time.time()
print(time_end - time_start)
print(list_sameImage)
            

