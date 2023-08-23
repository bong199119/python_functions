import os

path = r'Z:\preprocessing\data\yolo_format\SNUH_DC16_KSH0_LDG0_0031'

list_img = [png_ for png_ in os.listdir(path) if png_.endswith('png')]

for img_ in list_img:
    txtfile = img_[:-3] + 'txt'
    path_txtfile = os.path.join(path, txtfile)
    path_img = os.path.join(path, img_)
    if not os.path.isfile(path_txtfile):
        os.remove(path_img)