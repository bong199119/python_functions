import os

path = r''
list_labels = [file_ for file_ in os.listdir(path) if file_.endswith('txt')]
list_id_forremove = ['12', '13']

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