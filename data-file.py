import os
import sqlite3
import csv
root = os.getcwd()+"/conp-dataset/projects"

HASH_KEYWORDS = ["/MD5E-"]
#HASH_KEYWORDS = ["/MD5E-", "/URL"]
conn = sqlite3.connect('CONP.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS data_files")
cursor.execute("""CREATE TABLE data_files (
         
        dataset_fileHash text PRIMARY KEY,
        Dataset text,
        File_Name text,
        Hash_Function text,
        Hsah_Value text ,
        Commmit_Number text
        
            )""")
#comment after first time-----------
    
for path, subdirs, files in os.walk(root):
    for name in files:
        list_to_insert = []    
            
        with open(os.path.join(path, name),'r') as file:    
            try:    
                file_content = file.read()    
                for hash_key in HASH_KEYWORDS:    
                    if hash_key in file_content:    
                        #print (os.path.join(path, name))
                        path_fileName = os.path.join(path, name)    
                        dataset_name = (path_fileName.split("/projects\\")[1]).split("\\")[0]

                        #print("Dataset Name:    "+dataset_name)
                        file_name = (path_fileName.split("/projects\\")[1]).split("\\")[-1]    
                        #print("File Name:    "+file_name)
                            
                        #print(file_content)
                        string_lists = file_content.split("/")    
                        #print(string_lists)
                        if dataset_name and file_name:
                            for string in string_lists:
                                if hash_key.replace('/','') in string:
                                    #print(string)
                                    string = string.replace('--', '-')
                                    sub_strings = string.split("-")
                                    #print(sub_strings)
                                    hash_function = sub_strings[0]
                                    #print("Fnction : " + hash_function)

                                    hash_value = sub_strings[2].split('.')[0]
                                    #print("Hash Value : " + hash_value)
                                    latest_commit = sub_strings[1]
                                    if not latest_commit:
                                        latest_commit = ""

                                    #print("Commit : " + latest_commit)
                                    try:
                                        dataset_fileHash = dataset_name +"_"+hash_value
                                        cursor.execute("INSERT INTO data_files VALUES (?,?,?,?,?,?);",(dataset_fileHash,dataset_name,file_name,hash_function,hash_value,latest_commit))
                                        conn.commit()
                                    except sqlite3.IntegrityError:
                                        print("duplicated file in dataset: ",dataset_name, "\n file name: " ,file_name )
                                    
                                    break

            #cursor.execute('insert into sometable values (?,?,?)', (a, b, c))
            except UnicodeDecodeError:    
                #print ("Could not open/read file:",name)    
                pass
all_data = cursor.execute("select * from data_files")
print(all_data.description)
# with open("data_file.csv", "w") as csv_data_file:
#     csv_writer = csv.writer(csv_data_file)
#     csv_writer.writerow(['Dataset','File_Name','Hash_Function','Hsah_Value','Commmit_Number'])
#     csv_writer.writerows(all_data)
#for row in cursor.execute('SELECT * FROM data_files ORDER BY Hsah_Value'):
        #print(row)
conn.close()
            
    #writer.close()
            


    
  