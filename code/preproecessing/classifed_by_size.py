import os
import argparse
import matplotlib.pyplot as plt
import shutil

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    args = parser.parse_args()
    path = args.path

    list_xml = [file for file in os.listdir(path) if file.endswith('xml')]
    list_img = [file for file in os.listdir(path) if file.endswith('jpg') or file.endswith('JPG') or file.endswith('png') or file.endswith('PNG')]

    list_uniquesize = []
    for img in list_img:
        img_read = plt.imread(os.path.join(path, img))
        h, w, c = img_read.shape
        if (str(w)+'_'+str(h)) not in list_uniquesize:
            unique_size = str(w)+'_'+str(h)
            list_uniquesize.append(unique_size)
            try:
                os.mkdir(os.path.join(path, unique_size))
            except:
                pass

        shutil.copy(os.path.join(path, img),os.path.join(os.path.join(path, unique_size),img))  
        shutil.copy(os.path.join(path, img)[:-3]+'xml', os.path.join(os.path.join(path, unique_size),img[:-3]+'xml'))
    
    
            
if __name__ == "__main__":
    main()


                

