for xml in list_xml:
    dict_name_points = {}
    list_point_set = []
    file = open(os.path.join(path_input, xml), 'rt', encoding='UTF8')
    tree = ET.parse(file)
    root = tree.getroot()

    list_object = root.findall('object')
    for object_ in list_object:
        text_name = object_.findtext('name')
        text_id = object_.findtext('id')
        list_points = object_.findall('points')
        text_xpoints = list_points[0].findall('x')
        text_ypoints = list_points[0].findall('y')
        list_xpoints = []
        list_ypoints = []
        for i, text_xpoint in enumerate(text_xpoints):
            list_xpoints.append(float(text_xpoint.text))
            list_ypoints.append(float(text_ypoints[i].text))

        points_zip = zip(list_xpoints,list_ypoints)
        list_points_tuple = []
        for points in points_zip:
            list_points_tuple.append(points)
    
    frame_number = xml[:-4][-8:]
    frame_number = '0'*(8-len(str(int(frame_number))))+str(int(frame_number)-9)
    new_xml = xml[:-13] + '-'+ frame_number + '.xml'        
        
    image = Image.open(os.path.join(path_img_input,new_xml[:-3]+'jpg'))
    img1 = ImageDraw.Draw(image)  
    img1.polygon(list_points_tuple, fill = (0,255,255,0), outline ="blue") 
    numpy_image = np.array(image)
    plt.imshow(numpy_image)
    plt.show()