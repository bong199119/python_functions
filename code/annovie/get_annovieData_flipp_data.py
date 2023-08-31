import os
import xml.etree.ElementTree as ET
import cv2

path = r'E:\test' # image(.png) 와 xml파일이 같이 들어있는 푤더
path_flipped = r'E:\test_flipped' # 결과물(flipped image, flipped xml)을 출력할 폴더
list_xml = [file for file in os.listdir(path) if file.endswith('xml')]
list_png = [file for file in os.listdir(path) if file.endswith('png')]

print(len(list_xml))
print(len(list_png))

# png flipp
for png_each in list_png:
    path_png_each = os.path.join(path, png_each)
    path_png_each_flipped = os.path.join(path_flipped, 'flipped_'+png_each)
    img_bgr = cv2.imread(path_png_each)
    img_rgb_flipped = cv2.flip(img_bgr, 1)
    cv2.imwrite(path_png_each_flipped,img_rgb_flipped)
    
# xml x points flip
for xml_each in list_xml:
    path_xml_each = os.path.join(path, xml_each)
    path_xml_each_flipped = os.path.join(path_flipped, 'flipped_'+xml_each)

    tree=ET.parse(path_xml_each)
    root = tree.getroot()
    root_size = root.findall("size")
    width = int(root_size[0].findtext("width"))

    objects = root.findall("object")
    for object_each in objects:
        points = object_each.findall("points")
        points_x = points[0].findall("x")
        for point_x in points_x:
            point_x.text = str(float(width) - float(point_x.text))

    tree.write(path_xml_each_flipped)