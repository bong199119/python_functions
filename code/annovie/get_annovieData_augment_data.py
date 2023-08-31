import os
import xml.etree.ElementTree as ET
import cv2
import random
import shutil
import numpy as np
import argparse



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", dest="path") # 변환대상 데이터 경로
    parser.add_argument("--path_augmented", dest="path_augmented") # 변환데이터 저장 경로

    args = parser.parse_args()
    path = args.path
    path_augmented = args.path_augmented

    # path = r'D:\project\voucher\youn\sample_data' # image(.png) 와 xml파일이 같이 들어있는 푤더
    # path_augmented = r'D:\project\voucher\youn\results' # 결과물(flipped image, flipped xml)을 출력할 폴더
    list_xml = [file for file in os.listdir(path) if file.endswith('xml')]
    list_png = [file for file in os.listdir(path) if file.endswith('png')]

    print(len(list_xml))
    print(len(list_png))

    dx = 5
    dy = 0
    mtrx = np.float32([[1, 0, dx],
                    [0, 1, dy]])  

    # img 제작
    aug_count = 0
    for png_each in list_png:
        if aug_count < 1000:
            path_png_each = os.path.join(path, png_each)
            path_png_each_augmented = os.path.join(path_augmented, 'augmented_' + png_each)
            img = cv2.imread(path_png_each)
            rows,cols = img.shape[0:2] 
            img_flipped = cv2.warpAffine(img, mtrx, (cols, rows))   
            # img_flipped = cv2.resize(img_flipped, (1920,1080))
            cv2.imwrite(path_png_each_augmented, img_flipped)
            print(path_png_each_augmented)
            
        else:
            break
        aug_count += 1

    # xml 제작
    aug_count = 0
    for xml_each in list_xml:
        if aug_count < 1000:
            path_xml_each = os.path.join(path, xml_each)
            path_xml_each_flipped = os.path.join(path_augmented, 'augmented_'+ xml_each)

            tree=ET.parse(path_xml_each)
            root = tree.getroot()
            objects = root.findall("object")

            for object_each in objects:
                points = object_each.findall("points")
                points_x = points[0].findall("x")
                points_y = points[0].findall("y")
                for point_x in points_x:
                    rand_int = random.randint(3,4)
                    plus_or_not = rand_int%2
                    
                    # 짝수면 +
                    if plus_or_not == 0:
                        point_x.text = str(float(point_x.text) + 1 + random.random())

                    # 홀수면 -
                    else:
                        point_x.text = str(float(point_x.text) - 1 - random.random())

                for point_y in points_y:
                    rand_int = random.randint(3,4)
                    plus_or_not = rand_int%2
                    if plus_or_not == 0:
                        point_y.text = str(float(point_y.text) + 1 + random.random())
                    else:
                        point_y.text = str(float(point_y.text) - 1 - random.random())
                    
            tree.write(path_xml_each_flipped)
            print(path_xml_each_flipped)

        else:
            break
        aug_count += 1


if __name__ == "__main__":
    main()

exit()