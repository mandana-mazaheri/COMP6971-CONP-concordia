import os
import sqlite3
import json


# getting dats file from projects
root =os.getcwd()+"/conp-dataset/projects"
list_of_datasets = os.listdir(root)
list_of_dats =[]
description_dic = {}
type_dic ={}
keyword_dic={}
for files in list_of_datasets:
    if(str(files)!= ".touchfile"):
         curr_root = root + '/'+ str(files)
         if(os.listdir(curr_root).__contains__('DATS.json')):
             for i in os.listdir(curr_root):
                if(i=="DATS.json"):
                    with open(curr_root+'/'+i,'r',encoding='utf-8') as f:
                        data = json.load(f)
                        for key in data:
                            title=None
                            if(key=='title'):
                                title = data[key]
                                break
                        for key in data:
                            if (key == 'description'):
                                description_dic[title] = data[key]
                            if(key == 'types'):
                                type_dic[title] = data[key]
                            if(key == 'keywords'):
                                keyword_dic[title] = data[key] 
                                
         else:
            for i in os.listdir(curr_root):
                tem_root = curr_root +'/'+str(i)
                if(os.listdir(tem_root).__contains__('DATS.json')):
                    for j in os.listdir(tem_root):
                        if(j=="DATS.json"):
                            with open(tem_root+'/'+j,'r',encoding='utf-8') as f:
                                data = json.load(f)
                                for key in data:
                                    title=None
                                    if(key=='title'):
                                        title = data[key]
                                        break
                                for key in data:
                                    if (key == 'description'):
                                        description_dic[title] = data[key]
                                    if(key == 'types'):
                                        type_dic[title] = data[key]
                                    if(key == 'keywords'):
                                        keyword_dic[title] = data[key] 
print(len(description_dic))
print(len(type_dic))
print(len(keyword_dic))


#function
def extraction(given):
    to_return=None
    for each in given:
        if(isinstance(given[each],dict)):
            tem_dic = given[each]
            for key in tem_dic:
                to_return = tem_dic[key]
        else:
            for i in given:
                to_return = given[i]
    return to_return




final_type_dic={}
def combine (types,keywords):
    for each in types:
        final_list=[]
        for i in types[each]:
            to_insert = extraction(i)
            if not (final_list.__contains__(to_insert)):
                final_list.append(extraction(i))

        for i in keywords[each]:
            to_insert = extraction(i)
            if not (final_list.__contains__(to_insert)):
                final_list.append(extraction(i))
        final_type_dic[each] = final_list



combine (type_dic,keyword_dic)



conn = sqlite3.connect('CONP.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS dats_table")
cursor.execute("""CREATE TABLE dats_table (
    dataset_name text PRIMARYKEY,
    DATS_type text,
    DATS_description text
)""")
try:
    for each in description_dic:
        tem_types=None
        tem_des =None
        for i in final_type_dic[each]:
            if (tem_types==None):
                if(i!='' and i.find("http")==-1):
                    tem_types = i
            else:
                if(i!='' and i.find("http")==-1):
                    tem_types = tem_types +','+i
        tem_des = description_dic[each]
        record = [(each),(tem_types),(tem_des),]
        cursor.execute('INSERT INTO dats_table VALUES(?,?,?);',record)
        conn.commit()
except sqlite3.Error as error:
    print("recored error: ",error)
finally:
    if(conn):
        conn.close()

