# 새로 추출한 이미지 중 기존 데이터셋에(annovie format) 포함되지 않은 이미지 복사(특정 도구, 파일이름기반)
import os
import shutil

path_origin = r'' # 기존 데이터셋(annovie format) 위치
path_extract = r'' # 새로 추출한 이미지셋 위치
path_to = r'' # 기존 데이터셋에 포함되지 않은 추출한 이미지를 복사할 경로(목적지)

list_originDS_image = os.listdir(path_origin)
list_extractDS_folder = os.listdir(path_extract)

for extract_folder in list_extractDS_folder:
    path_extract_folder = os.path.join(path_extract, extract_folder)
    list_extractDS_image = os.listdir(path_extract_folder)
    for extract_image in list_extractDS_image:
        path_extract_image = os.path.join(path_extract_folder, extract_image)
        path_to_extract_image = os.path.join(path_to, extract_image)
        if extract_image.split('_')[-1][0] == '1': # dissector : 0, obturator : 10
            if extract_image not in list_originDS_image:
                shutil.copy(path_extract_image, path_to_extract_image)
                print(extract_image)




