import json
import sqlite3
import os
conn = sqlite3.connect('CONP.db')
#conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()
#conn.execute("PRAGMA foreign_keys = 1")
cursor.execute("DROP TABLE IF EXISTS input_files")
try:
    cursor.execute("""CREATE TABLE input_files (
        infile_name TEXT,
        infile_hash TEXT ,
        exeRecord_id INTEGER
                    )""")
    conn.commit()
except sqlite3.OperationalError:
    print("sqlite3 OperationalError")
  #ID INTEGER PRIMARY KEY AUTOINCREMENT,


cursor.execute("DROP TABLE IF EXISTS exe_records")
try:
    cursor.execute("""CREATE TABLE exe_records (

        ID INTEGER PRIMARY KEY ,
        pipeline_name TEXT,
        pipeline_DOI TEXT ,
        exit_code INTEGER,
        error_message TEXT,
        shell_command TEXT,
        stdout TEXT,            
        stdrr TEXT
       
                    )""")
    conn.commit()
except sqlite3.OperationalError:
    print("sqlite3 OperationalError")
#verbose INTEGER,
# FOREIGN KEY (ID) REFERENCES input_files(exeRecord_id)

#with open('Dipy-Deterministic-Tracking_2019-07-28T015253.320751.json') as exeRec:
  #  contents = json.load(exeRec)
def iterator(contents,exe_id):
    pipeline_name = ""
    pipeline_DOI = ""
    exit_code = 1
    error_message = ""
    shell_command = ""
    stdout = ""
    stderr = ""
    for key, value in contents.items():
        if key == "summary":
            pipeline_name = contents["summary"]["name"]
            pipeline_DOI = contents["summary"]["descriptor-doi"]
        elif key == "public-invocation":
            getInputFiles(contents["public-invocation"],exe_id)
        elif key == "public-output":
            for nestedKey,nestedValue in contents["public-output"].items():
                #print(nestedKey, " : ", nestedValue)
                if nestedKey == "stdout":
                    stdout = nestedValue
                    #print(" --stdout-- :",nestedValue)
                elif nestedKey == "stderr":
                    stderr = nestedValue
                    #print(" --stderr-- :", nestedValue)
                elif nestedKey == "exit-code":
                    exit_code = nestedValue
                    #print(" --exit-code-- :", nestedValue)
                elif nestedKey == "error-message":
                    error_message = nestedValue
                    #print(" --error-message-- :", nestedValue)
                elif nestedKey == "shell-command":
                    shell_command = nestedValue
                    #print(" --shell-command-- :", nestedValue)

    cursor.execute("INSERT INTO exe_records VALUES (?,?,?,?,?,?,?,?);",(exe_id,pipeline_name,pipeline_DOI,exit_code,error_message,shell_command,stdout,stderr))
    conn.commit()

def getInputFiles(invoked,exe_id):
    file_name = ""
    file_hash = ""
    if type(invoked) == type(dict()):
        if "file-name" in invoked.keys() and "md5sum" in invoked.keys():
            file_name = invoked["file-name"]
            file_hash = invoked["md5sum"]
            cursor.execute("INSERT INTO input_files VALUES (?,?,?);",(file_name,file_hash,exe_id,))
            conn.commit()
            #print("file-name" ,invoked["file-name"])
            #print("md5sum", invoked["md5sum"])
        elif "file-name" in invoked.keys() and "hash" in invoked.keys():
            file_name = invoked["file-name"]
            file_hash = invoked["md5sum"]
            cursor.execute("INSERT INTO input_files VALUES (?,?,?);", ( file_name, file_hash,exe_id))
            conn.commit()
            #print("file-name" ,invoked["file-name"])
            #print("hash", invoked["hash"])
        else:
            for key, value in invoked.items():
                if key == "verbose":
                    print("--verbose--",str(value))
                elif type(value) == type(dict()):
                    getInputFiles(value,exe_id)
                elif type(value) == type(list()):
                    for val in value:
                        if type(val) == type(dict()):
                            getInputFiles(val,exe_id)


exe_id = 0
json_files = [i for i in os.listdir(os.getcwd()+"/exe_records") if i.endswith("json")]
for exeRecord in json_files:

    with open(os.getcwd()+"/exe_records/"+exeRecord) as exeRec:
        contents = json.load(exeRec)
        exe_id = exe_id + 1
        iterator(contents,exe_id)


#invoked = contents["public-invocation"]
#getInputFiles(invoked)

# else:
#     print(str(key) + '->' + str(value))
#     if type(value) == type(dict()):
#         iterator(value)
#     elif type(value) == type(list()):
#         for val in value:
#             if type(val) == type(dict()):
#                 iterator(val)

