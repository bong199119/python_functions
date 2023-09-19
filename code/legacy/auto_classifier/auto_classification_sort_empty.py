#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys , numpy as np
import xml.etree.ElementTree as ET
import shutil
import argparse

# In[ ]:


#root_path = 'D:/class/'
#path_class_txt = "C:/Users/mteg/Desktop/class.txt" # 클래스,path적혀있는 텍스트파일 경로 
# 옮길 폴더명 # 만들폴더명 # class.txt위치


# In[ ]:

def get_path_class_list(path_class_txt):
    #f = open(path_class_txt)
    #path = ""

    #lines = f.readlines()
    #for line in lines:
        #if 'path' in line:
            #line_split = line.split()
            #path = line_split[-1]

    f = open(path_class_txt)
    class_semi_list = []
    class_list = []
    lines = f.readlines()
    for line in lines:
        parts = line.split("\'")
        if parts[0][-1] == '\n':
            parts = parts[0][:-1] 
            class_list.append(parts)
        else:
            class_list.append(parts[0])
        
    f.close

#     class_name_num = 0
#     for i in range(len(class_semi_list)):
#         if 'class name' in class_semi_list[i]:
#             class_name_num = i
#         if ("\n" not in class_semi_list[i]) and (class_name_num < i) and not(any(sym in class_semi_list[i] for sym in "!@#$%^&*\[\]\{\}\~\`\\\'\?\/\>\<\.\,\-\_\+\=\)\(")) and class_semi_list[i] != ('' or  ' '):
#             class_list.append(class_semi_list[i])
            
    return class_list



def make_folds(class_list, root_path):
    class_dir = []
    for class_ in class_list:
        class_dir_element = (root_path+'/'+class_)
        if not(os.path.isdir(class_dir_element)):
                os.makedirs(os.path.join(class_dir_element))
        class_dir.append(class_dir_element)

    if not(os.path.isdir(root_path+'/'+"xml_class_count")):
                os.makedirs(os.path.join(root_path+'/'+"xml_class_count"))

#     if not(os.path.isdir(root_path+'/'+"xml_class_count/"+"xml_class_count")):
#                 os.makedirs(os.path.join(root_path+'/'+"xml_class_count/"+"xml_class_count"))
    return class_dir



def make_var_list(class_list):
    class_count = []
    class_img_count = []
    class_semi_count = []

    for class_ in class_list:
        class_split = class_.split()

        class_count_part = ''
        for i in range(len(class_split)):
                class_count_part += class_split[i]
                if i != (len(class_split)-1):
                    class_count_part += '_'

        class_count_part_count = class_count_part + '_count'
        class_count_part_img_count = class_count_part + '_img_count'
        class_count_part_semi_count = class_count_part + '_semi_count'

        class_count.append(class_count_part_count)
        class_img_count.append(class_count_part_img_count)
        class_semi_count.append(class_count_part_semi_count)
        
    return class_count, class_img_count, class_semi_count

def make_dic_count(class_count, class_img_count, class_semi_count):
    dic_class_count = {}
    dic_class_img_count = {}
    dic_class_semi_count = {}
    
    for class_ in class_count:
        dic_class_count[class_] = 0
        
    for class_ in class_img_count:
        dic_class_img_count[class_] = 0
        
    for class_ in class_semi_count:
        dic_class_semi_count[class_] = 0
        
    return dic_class_count, dic_class_img_count, dic_class_semi_count

def make_xml_list(path):
    file_list = os.listdir(path)
    xml_list = []
    for file in file_list:
            if file[-3:] == 'xml':
                xml_list.append(file)
    return xml_list



def classify_and_copy_xml_img(xml_list, root_path, path, class_list, class_dir, class_count, class_semi_count,class_img_count,dic_class_count, dic_class_img_count, dic_class_semi_count):
    
    xml_list.sort()
    file_count = 0
    f = open(root_path+'/'+"xml_class_count/"+ 'xml_class_count' +".txt", 'w')
    f.write(',file name  ,object name  ,object count\n')
    empty_list = []
    for i in range(len(xml_list)):
        tree = ET.parse(path+"/"+xml_list[i])
        root = tree.getroot()
        path_root = root.findall("object")
        path_root_class_list = []
        
        if path_root == []:
            empty_list.append(xml_list[i])
        
        for p in range(len(class_list)):
            dic_class_semi_count[class_semi_count[p]] = 0

        for root in path_root:
            word = root.findtext("name")
            for j in range(len(class_list)):
                if word == class_list[j]:
                    dic_class_count[class_count[j]] += 1
                    dic_class_semi_count[class_semi_count[j]] += 1
                    shutil.copy2((path+"/"+xml_list[i]),(class_dir[j]))
                    if os.path.isfile(path+"/"+xml_list[i][:-3]+'png'):
                        shutil.copy2((path+"/"+xml_list[i][:-3]+'png'),(class_dir[j]))
                    elif os.path.isfile(path+"/"+xml_list[i][:-3]+'jpg'):
                        shutil.copy2((path+"/"+xml_list[i][:-3]+'jpg'),(class_dir[j]))
                        
                        
            path_root_class_list.append(word)
            
        for j in range(len(class_list)):
            if dic_class_semi_count[class_semi_count[j]] != 0:
                f.write(','+xml_list[i]+' '*3+','+class_list[j]+' '*3 +','+str(dic_class_semi_count[class_semi_count[j]])+'\n')
        f.write('\n')
# 
#                     shutil.copy2((path+"/"+xml_list[i]),(root_path+'/'+"xml_class_count"))
#                     if os.path.isfile(path+"/"+xml_list[i][:-3]+'png'):
#                         shutil.copy2((path+"/"+xml_list[i][:-3]+'png'),(root_path+'/'+"xml_class_count"))
#                     elif os.path.isfile(path+"/"+xml_list[i][:-3]+'jpg'):
#                         shutil.copy2((path+"/"+xml_list[i][:-3]+'jpg'),(root_path+'/'+"xml_class_count"))

            

        for k in range(len(class_list)):
            dic_class_semi_count[class_semi_count[k]] = 1 if (dic_class_semi_count[class_semi_count[k]] > 0) else 0

        for y in range(len(class_list)):
            dic_class_img_count[class_img_count[y]] += dic_class_semi_count[class_semi_count[y]]

        file_count +=1
        print(file_count ,path_root_class_list,'in',path+"/"+xml_list[i])
    f.close()
    f= open(root_path+'/'+"xml_class_count/"+ 'xml_class_count' +".txt",'r')
    contents = f.readlines()
    f.close()
    
    print("")
    print(("{}에서 분류한 데이터수 = ").format(path), file_count)

    for t in range(len(class_list)):
        print(('라벨링한 {}의 개수 = {} / {}의 이미지 개수 = {}').format(class_list[t],dic_class_count[class_count[t]],class_list[t],dic_class_img_count[class_img_count[t]]))
    
     
    class_list_len=[]
    for v in class_list:
        class_list_len.append(len(v))
        
    class_list_len_max = max(class_list_len)
    
    
    # 통합카운트를 통합폴더(xml_class_count)에 텍스트파일로 저장    
    
    data = (','+('%-{}s').format(class_list_len_max+3) % "object name"+ ','+ ('%-{}s').format(class_list_len_max+3) % "image count" +','+('%-{}s').format(class_list_len_max*2) % ("object count{}\n").format(" "*class_list_len_max*2))
    contents.insert(0, data)
    
    k = 1 # contents.insert사용시 다중인덱스 부여하는 용도로 사용
    for i in range(len(class_list)):
         
        if dic_class_img_count[class_img_count[i]] != 0: # 사용된 클래스만 
            data = (','+('%-{}s').format(class_list_len_max+3) % class_list[i]+','+('%-{}s').format(class_list_len_max+3) % str(dic_class_img_count[class_img_count[i]])+','+('%-{}s').format(class_list_len_max*2) % str(dic_class_count[class_count[i]])+'\n')
            contents.insert(k, data)
            k += 1
            
    count_class = 0       
    for i in range(len(class_list)):
        if dic_class_img_count[class_img_count[i]] != 0:
            count_class += 1
    
    total_object_count = 0
    for j in range(len(class_list)):
        total_object_count += dic_class_count[class_count[j]]
        
        
        
    data = (',classes count: '+str(count_class)+' '*3+',total image count: '+str(file_count)+' '*3+',total object count: '+str(total_object_count)+'\n\n\n')
    contents.insert(k, data)
    k += 1
    
    
    for empty in empty_list:
        data = (',empty_files : ,'+ empty+'\n')
        contents.insert(k, data)
        k += 1
        
    f = open(root_path+'/'+"xml_class_count/"+ 'xml_class_count' +".txt", "w")
    contents = "".join(contents)
    f.write(contents)           
    f.close()



def count_object(path, root_path, class_list, class_count, class_semi_count, class_img_count, class_fold, class_fold_list,dic_class_count, dic_class_img_count, dic_class_semi_count):
    
    index = 0
    for s in range(len(class_list)):
        if class_list[s] == class_fold:
            index = s
    
    for p in range(len(class_list)):
            dic_class_count[class_count[p]] = 0
            
    for p in range(len(class_list)):
            dic_class_img_count[class_img_count[p]] = 0
    
    file_list = os.listdir(root_path+'/'+class_fold)
    xml_list = []
    for file in file_list:
            if file[-3:] == 'xml':
                xml_list.append(file)
                
    xml_list.sort()
    # 파일은 한번만 열고 쓰고싶은것 다쓴후에 마지막에 한번만 닫는다. 
    f = open(root_path+'/'+"xml_class_count/"+ class_fold +".txt", 'w')
    file_count = 0
    for i in range(len(xml_list)):
        tree = ET.parse(path+"/"+xml_list[i])
        root = tree.getroot()
        path_root = root.findall("object")
        path_root_class_list = []

        for p in range(len(class_list)):
            dic_class_semi_count[class_semi_count[p]] = 0

        for root in path_root:
            word = root.findtext("name")
            for j in range(len(class_list)):
                if word == class_list[j]:
                    dic_class_count[class_count[j]] += 1
                    dic_class_semi_count[class_semi_count[j]] += 1

            path_root_class_list.append(word)
        
        # 파일열어서 파일이름.png or jpg object_count 쓰기
        
        data = (',{}   ,object_count = {}\n').format(xml_list[i], dic_class_semi_count[class_semi_count[index]]) 
        f.write(data)
        dic_class_semi_count[class_semi_count[index]] = 1 if (dic_class_semi_count[class_semi_count[index]] > 0) else 0

#         for y in range(len(class_list)):
        dic_class_img_count[class_img_count[index]] += dic_class_semi_count[class_semi_count[index]]

        file_count +=1
#         print(file_count ,path_root_class_list,'in',path+"/"+xml_list[i])

#     print((',이미지 개수 = {}  ,object 개수 = {}').format(dic_class_img_count[class_img_count[index]], dic_class_count[class_count[index]]))    
    
    # 각 폴더별 오브젝트 카운트해서 텍스트파일로 저장
#     f = open(root_path+'/'+class_fold + "/"+class_fold+ "/"+class_fold+".txt", 'w')
#     data ="데이터수 = " + str(file_count)+'\n'
#     f.write(data)
    
#     for i in range(len(class_list)):
#         data = ('라벨링한 {}의 개수 = {} / {}의 이미지 개수 = {}\n').format(class_list[i],dic_class_count[class_count[i]],class_list[i],dic_class_img_count[class_img_count[i]] ) 
#         f.write(data)

#     f.close()
    
    f.close()
    # 각 폴더별 오브젝트 카운트해서 통합폴더(xml_class_count)에 텍스트파일로 저장    
    f= open(root_path+'/'+"xml_class_count/"+ class_fold +".txt",'r')
    contents = f.readlines()
    f.close()
    
    data = (',이미지 개수 = {}  ,object 개수 ={}\n\n').format(dic_class_img_count[class_img_count[index]], dic_class_count[class_count[index]]) 
    contents.insert(0, data)
    f = open(root_path+'/'+"xml_class_count/"+ class_fold +".txt", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()
    
    return print('done')

def main():
   parser = argparse.ArgumentParser()
   parser.add_argument('path')
   parser.add_argument('path_class_txt')
   parser.add_argument('root_path')
   args = parser.parse_args()
   
   path = args.path
   path_class_txt = args.path_class_txt 
   root_path = args.root_path
   
# In[ ]:
   class_list = get_path_class_list(path_class_txt)
   class_dir = make_folds(class_list, root_path)
   class_count, class_img_count, class_semi_count=make_var_list(class_list)
   dic_class_count, dic_class_img_count, dic_class_semi_count =  make_dic_count(class_count, class_img_count, class_semi_count)
# In[ ]:


   mod = sys.modules[__name__]

   for i in range(len(class_count)):
       setattr(mod, class_count[i],0)
       setattr(mod, class_img_count[i],0)
       setattr(mod, class_semi_count[i],0)  
    
   #vars_ = globals() # 만들어진 변수가 딕셔너리형태로 globals에 들어있음  # globals은 변수를 만들때마다 길이가 변하므로 vars_에 복사해서 사용


# In[ ]:


   xml_list = make_xml_list(path)


# In[ ]:


   classify_and_copy_xml_img(xml_list, root_path, path, class_list, class_dir, class_count, class_semi_count,class_img_count, dic_class_count, dic_class_img_count, dic_class_semi_count )


# In[ ]:


   class_fold_list = os.listdir(root_path)

   for class_fold in class_fold_list:
       if class_fold != 'xml_class_count':
           count_object(path, root_path, class_list, class_count,class_semi_count, class_img_count,class_fold, class_fold_list,dic_class_count, dic_class_img_count, dic_class_semi_count)
        

# In[ ]:

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




