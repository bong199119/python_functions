import os

def rename_obj(path, list_id_forrename, targetid): # 
    list_labels = [file_ for file_ in os.listdir(path) if file_.endswith('txt')]

    for label_ in list_labels:
        path_label = os.path.join(path, label_)
        with open(path_label, "r") as f:
            lines = f.readlines()
        f.close()

        with open(path_label, "w") as f:
            for line in lines:
                class_id = line.split(' ')[0]
                linestr = ''
                for line_ele in line.split(' ')[1:]:
                    linestr+=line_ele

                if class_id not in list_id_forrename: 
                    f.write(line)

                elif class_id in list_id_forrename: 
                    linestr = targetid + ' ' + linestr
                    f.write(linestr)
                    print(line, ' -> ', linestr)

        f.close()
        print(path_label)

def del_obj(path, list_id_forremove): # 
    list_labels = [file_ for file_ in os.listdir(path) if file_.endswith('txt')]

    for label_ in list_labels:
        path_label = os.path.join(path, label_)
        with open(path_label, "r") as f:
            lines = f.readlines()
        f.close()

        with open(path_label, "w") as f:
            for line in lines:
                class_id = line.split(' ')[0]
                if class_id not in list_id_forremove:     # <= 이 문자열만 골라서 삭제
                    f.write(line)
                    
        f.close()
        print(path_label)

path = r''
targetid = '5'
list_id_forrename = ['12','13']
rename_obj(path, list_id_forrename, targetid)