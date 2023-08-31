import os
import json
import pandas as pd
from datetime import datetime

now = datetime.now()
print('start time : ', now.strftime('%Y-%m-%d %H:%M:%S')) 

path = r'D:\project\구문검사결과지\test'
path_to = r'D:\project\구문검사결과지\results'
csvanme = r'results.csv'

df_total = pd.DataFrame(columns=['파일명', '오류 위치','검사 항목','검사 조건','오류 값','오류 메시지'])
list_filename = []
list_errorposition = []
list_testele = []
list_testcondition = []
list_errorvalue = []
list_errormessage = []

list_json = os.listdir(path)

totalcount_errorele = 0
totalcount_errorfile = 0
totalcount_file = len(list_json)
totalcount_ele = 0

for json_ in list_json:
    path_json = os.path.join(path, json_)

    with open(path_json, "r", encoding='UTF8') as json_ele:
        dict_jsoncontents = json.load(json_ele)

    count_errorele = 0
    count_ele = 0

    #####################################
    ###          images 검사          ###
    #####################################

    # /images/id 검사
    if dict_jsoncontents['images']['id'] == '':
        list_filename.append(json_)
        list_errorposition.append('/images/id')
        list_testele.append('필수여부')
        list_testcondition.append(' ')
        list_errorvalue.append(' ')
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1
        
    # /images/width 검사
    if dict_jsoncontents['images']['width'] == '' :
        list_filename.append(json_)
        list_errorposition.append('/images/width')
        list_testele.append('최소값')
        list_testcondition.append('400')
        list_errorvalue.append(dict_jsoncontents['images']['width'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1

    elif int(dict_jsoncontents['images']['width']) < 400 :
        list_filename.append(json_)
        list_errorposition.append('/images/width')
        list_testele.append('최소값')
        list_testcondition.append('400')
        list_errorvalue.append(dict_jsoncontents['images']['width'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1

    else:
        count_ele += 1
    
    # /images/height 검사
    if dict_jsoncontents['images']['height'] == '' :
        list_filename.append(json_)
        list_errorposition.append('/images/height')
        list_testele.append('최소값')
        list_testcondition.append('400')
        list_errorvalue.append(dict_jsoncontents['images']['height'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1

    elif int(dict_jsoncontents['images']['height']) < 400 :
        list_filename.append(json_)
        list_errorposition.append('/images/height')
        list_testele.append('최소값')
        list_testcondition.append('400')
        list_errorvalue.append(dict_jsoncontents['images']['height'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1

    else:
        count_ele += 1

    # /images/filename 검사
    if dict_jsoncontents['images']['filename'] == '':
        list_filename.append(json_)
        list_errorposition.append('/images/filename')
        list_testele.append('필수여부')
        list_testcondition.append(' ')
        list_errorvalue.append(' ')
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    # /images/volume 검사
    if 'volume' in  dict_jsoncontents['images'].keys():
        count_ele += 1

    #####################################
    ###          metas 검사           ###
    #####################################

    # /metas/id 검사
    if 'id' in dict_jsoncontents['metas'].keys():
        count_ele += 1

    # /metas/age 검사
    if dict_jsoncontents['metas']['age'] == '':
        list_filename.append(json_)
        list_errorposition.append('/metas/age')
        list_testele.append('필수여부')
        list_testcondition.append(' ')
        list_errorvalue.append(' ')
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    # /metas/gender 검사
    if dict_jsoncontents['metas']['gender'] not in ['M', 'F']:
        list_filename.append(json_)
        list_errorposition.append('/metas/gender')
        list_testele.append('유효값')
        list_testcondition.append("\"M\",\"F\"")
        list_errorvalue.append(dict_jsoncontents['metas']['gender'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    # /metas/phase 검사
    if dict_jsoncontents['metas']['phase'] not in ['Velum', 'OTE']:
        list_filename.append(json_)
        list_errorposition.append('/metas/phase')
        list_testele.append('유효값')
        list_testcondition.append("\"Velum\",\"OTE\"")
        list_errorvalue.append(dict_jsoncontents['metas']['phase'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    # /metas/position 검사
    if dict_jsoncontents['metas']['position'] not in ['awake', 'supine','lateral','resupine']:
        list_filename.append(json_)
        list_errorposition.append('/metas/position')
        list_testele.append('유효값')
        list_testcondition.append("\"awake\",\"supine\",\"lateral\",\"resupine\"")
        list_errorvalue.append(dict_jsoncontents['metas']['position'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    # /metas/SpO2 검사
    if dict_jsoncontents['metas']['SpO2'] == '':
        list_filename.append(json_)
        list_errorposition.append('/metas/SpO2')
        list_testele.append('필수여부')
        list_testcondition.append(' ')
        list_errorvalue.append(' ')
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    # /metas/AHI 검사
    if dict_jsoncontents['metas']['AHI'] == '':
        list_filename.append(json_)
        list_errorposition.append('/metas/AHI')
        list_testele.append('필수여부')
        list_testcondition.append(' ')
        list_errorvalue.append(' ')
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    # /metas/bmi 검사
    if 'bmi' in dict_jsoncontents['metas'].keys():
        count_ele += 1

    # /metas/position 검사
    if dict_jsoncontents['metas']['obstruction'] not in ['no', 'partial','complete']:
        list_filename.append(json_)
        list_errorposition.append('/metas/obstruction')
        list_testele.append('유효값')
        list_testcondition.append("\"no\",\"partial\",\"complete\"")
        list_errorvalue.append(dict_jsoncontents['metas']['obstruction'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    # /metas/cause 검사
    if dict_jsoncontents['metas']['cause'] not in ['no', 'Velum','Tongue_Base','Epiglottis']:
        list_filename.append(json_)
        list_errorposition.append('/metas/cause')
        list_testele.append('유효값')
        list_testcondition.append("\"no\",\"Velum\",\"Tongue_Base\",\"Epiglottis\"")
        list_errorvalue.append(dict_jsoncontents['metas']['cause'])
        list_errormessage.append('_')
        count_errorele +=1
        count_ele += 1
    else:
        count_ele += 1

    #####################################
    ###        annoatation 검사       ###
    #####################################

    for annotation_ele in dict_jsoncontents['annotations']:
        
        # /annotation/id 검사
        if annotation_ele['id'] == '':
            list_filename.append(json_)
            list_errorposition.append('/annotations/id')
            list_testele.append('필수여부')
            list_testcondition.append(' ')
            list_errorvalue.append(' ')
            list_errormessage.append('_')
            count_errorele +=1
            count_ele += 1
        else:
            count_ele += 1

        # /annotation/image_id 검사
        if annotation_ele['image_id'] == '':
            list_filename.append(json_)
            list_errorposition.append('/annotations/image_id')
            list_testele.append('필수여부')
            list_testcondition.append(' ')
            list_errorvalue.append(' ')
            list_errormessage.append('_')
            count_errorele +=1
            count_ele += 1
        else:
            count_ele += 1

        # /annotation/category_id 검사
        if annotation_ele['category_id'] not in ['6000', '6001','6002','6003','6004','6005']:
            list_filename.append(json_)
            list_errorposition.append('/annotations/category_id')
            list_testele.append('유효값')
            list_testcondition.append("\"6000\",\"6001\",\"6002\",\"6003\",\"6004\",\"6005\"")
            list_errorvalue.append(annotation_ele['category_id'])
            list_errormessage.append('_')
            count_errorele +=1
            count_ele += 1
        else:
            count_ele += 1

        # /annotation/category_name 검사
        if annotation_ele['category_name'] not in ['Velum', 'Airway1','Posterior_lateral_wall','Tongue_Base','Epiglottis','Airway2']:
            list_filename.append(json_)
            list_errorposition.append('/annotations/category_name')
            list_testele.append('유효값')
            list_testcondition.append("\"Velum\",\"Airway1\",\"Posterior_lateral_wall\",\"Tongue_Base\",\"Epiglottis\",\"Airway2\"")
            list_errorvalue.append(annotation_ele['category_name'])
            list_errormessage.append('_')
            count_errorele +=1
            count_ele += 1
        else:
            count_ele += 1

        # /annotation/type 검사
        if annotation_ele['type'] not in ['poly']:
            list_filename.append(json_)
            list_errorposition.append('/annotations/type')
            list_testele.append('유효값')
            list_testcondition.append("\"poly\"")
            list_errorvalue.append(annotation_ele['type'])
            list_errormessage.append('_')
            count_errorele +=1
            count_ele += 1
        else:
            count_ele += 1

        # /annotation/color 검사
        if annotation_ele['color'] == '':
            list_filename.append(json_)
            list_errorposition.append('/annotations/color')
            list_testele.append('필수여부')
            list_testcondition.append(' ')
            list_errorvalue.append(' ')
            list_errormessage.append('_')
            count_errorele +=1
            count_ele += 1
        else:
            count_ele += 1

        # /annotation/points 검사
        if annotation_ele['points'] == []:
            list_filename.append(json_)
            list_errorposition.append('/annotations/points')
            list_testele.append('필수여부')
            list_testcondition.append(' ')
            list_errorvalue.append(' ')
            list_errormessage.append('_')
            count_errorele +=1
            count_ele += 1
        else:
            count_ele += 1

            for points_ele in annotation_ele['points']:

                # /annotation/points/[] 검사
                if points_ele == []:
                    list_filename.append(json_)
                    list_errorposition.append('/annotations/points/[]')
                    list_testele.append('필수여부')
                    list_testcondition.append(' ')
                    list_errorvalue.append(' ')
                    list_errormessage.append('_')
                    count_errorele +=1
                    count_ele += 1
                else:
                    count_ele += 1                     
    
    totalcount_errorele += count_errorele
    totalcount_ele += count_ele

    if count_errorele > 0 :
        totalcount_errorfile += 1

df_total['파일명'] = list_filename
df_total['오류 위치'] = list_errorposition
df_total['검사 항목'] = list_testele
df_total['검사 조건'] = list_testcondition
df_total['오류 값'] = list_errorvalue
df_total['오류 메시지'] = list_errormessage

path_results = os.path.join(path_to, csvanme)
df_total.to_csv(path_results, encoding = 'cp949', index = False)

print('정확도(파일): ', round(((totalcount_file-totalcount_errorfile)/totalcount_file)*100,2),'%')
print('정확도(항목): ', round(((totalcount_ele-totalcount_errorele)/totalcount_ele)*100,2),'%')
print('오류 건수(파일): ', totalcount_errorfile)
print('오류 건수(항목): ', totalcount_errorele)
print('전체 건수(파일): ', totalcount_file)
print('전체 건수(항목): ', totalcount_ele)

now = datetime.now()
print('end time : ', now.strftime('%Y-%m-%d %H:%M:%S')) 