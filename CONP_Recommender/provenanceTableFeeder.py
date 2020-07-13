import json
import sys
import platform
import os
import os.path
from os import path
import sqlite3
import csv



class provenanceTableFeeder(object):


    def fillProvenanceTable(self):
        '''
        osType = platform.system()
        cachePath = None
        if osType == 'Windows':
            cachePath = os.getenv('APPDATA')
        elif osType == 'Linux':
            cachePath = "~/.cache"
        '''
        cachePath = os.path.expanduser('~')

        if not os.path.exists(os.path.join(cachePath, "CONP_Recommender")):
            os.mkdir(os.path.join(cachePath, "CONP_Recommender"))

        cachePath = os.path.join(cachePath, "CONP_Recommender")
        self.conn = sqlite3.connect( os.path.join(cachePath, 'CONP.db'))

        #conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()
        #conn.execute("PRAGMA foreign_keys = 1")
        SIMONPath = os.path.join(os.path.dirname(__file__),'CONP_simon.db')
        #print(SIMONPath)
        self.cursor.execute("ATTACH \'"+  SIMONPath +"\' AS CONP_simon")

        self.cursor.execute("INSERT INTO data_files(Dataset, File_Name,Hash_Function,Hsah_Value,Commmit_Number) SELECT Dataset, File_Name,Hash_Function,Hsah_Value,Commmit_Number FROM CONP_simon.data_files")
        self.cursor.execute("DROP TABLE IF EXISTS input_files")
        try:
            self.cursor.execute("""CREATE TABLE input_files (
                infile_name TEXT,
                infile_hash TEXT ,
                exeRecord_id INTEGER
                            )""")
            self.conn.commit()
        except sqlite3.OperationalError:
            print("sqlite3 OperationalError")
          #ID INTEGER PRIMARY KEY AUTOINCREMENT,


        self.cursor.execute("DROP TABLE IF EXISTS exe_records")
        try:
            self.cursor.execute("""CREATE TABLE exe_records (

                ID INTEGER PRIMARY KEY ,
                pipeline_name TEXT,
                pipeline_DOI TEXT ,
                exit_code TEXT,
                error_message TEXT,
                shell_command TEXT,
                stdout TEXT,            
                stdrr TEXT
               
                            )""")
            self.conn.commit()
        except sqlite3.OperationalError:
            print("sqlite3 OperationalError")

        exe_id = 0
        """********************"""
        '''
        osType = platform.system()
        provenancePath = None
        if osType == 'Windows': 
            provenancePath = os.path.join(os.getenv('HOMEDRIVE'),os.getenv('HOMEPATH'))
        elif osType == 'Linux':
            provenancePath = "~/.cache"
        '''
        provenancePath = os.path.expanduser('~')
        provenancePath = os.path.join(provenancePath,'.cache','boutiques','data')

        #print(provenancePath)
        #json_files = [i for i in os.listdir(os.getcwd()+"/exe_records") if i.endswith("json")]
        if os.path.exists(provenancePath) :
            json_files = [i for i in os.listdir(provenancePath) if i.endswith("json")]
            for exeRecord in json_files:
                #print()
                with open(os.path.join(provenancePath,exeRecord)) as exeRec :
                #with open(os.getcwd()+"/exe_records/"+exeRecord) as exeRec:
                    contents = json.load(exeRec)
                    exe_id = exe_id + 1
                    self.iterator(contents,exe_id)

        else:
            print("no provenance has been pulled")

    def iterator(self,contents,exe_id):
        pipeline_name = ""
        pipeline_DOI = ""
        exit_code = ""
        error_message = ""
        shell_command = ""
        stdout = ""
        stderr = ""
        for key, value in contents.items():
            if key == "summary":
                pipeline_name = contents["summary"]["name"]
                pipeline_DOI = contents["summary"]["descriptor-doi"]
                if "/" in pipeline_DOI:
                    pipeline_DOI = pipeline_DOI.split("/")[1]
            elif key == "public-invocation":
                file_hash_list = []
                self.recurse_keys(contents["public-invocation"],file_hash_list)
                self.fillFileTable(file_hash_list,exe_id)
                #self.getInputFiles(contents["public-invocation"],exe_id)
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
                        exit_code = str(nestedValue)
                        #print(exe_id,"  exit code: ",exit_code)
                        #print(" --exit-code-- :", nestedValue)
                    elif nestedKey == "error-message":
                        error_message = nestedValue
                        #print(" --error-message-- :", nestedValue)
                    elif nestedKey == "shell-command":
                        shell_command = nestedValue
                        #print(" --shell-command-- :", nestedValue)

        self.cursor.execute("INSERT INTO exe_records VALUES (?,?,?,?,?,?,?,?);",(exe_id,pipeline_name,pipeline_DOI,exit_code,error_message,shell_command,stdout,stderr))
        self.conn.commit()


    def fillFileTable(self,file_hash_list,exe_id):
        size = len(file_hash_list)
        for indx,val in enumerate(file_hash_list):
            if "file-name" in val:
                if indx < (size - 1):
                    nextItem = file_hash_list[indx + 1]
                    if "md5sum" in nextItem:
                        fileName = val.split(',')[1]
                        md5 = nextItem.split(',')[1]
                        self.cursor.execute("INSERT INTO input_files VALUES (?,?,?);", (fileName, md5, exe_id))
                        self.conn.commit()
                        #print(fileName, "----", md5)




    def recurse_keys(self,df,fileHashList):
        if isinstance(df,dict):
            for key in df.keys():
                if str(key) == "file-name":
                    fileHashList.append("file-name" + ","+ str(df[key]) )
                elif str(key) == "md5sum":
                    fileHashList.append("md5sum" + ","+ str(df[key]) )
                elif str(key) == "not_found":
                    fileHashList.append("not_found" + ","+str(df[key]) )
                elif str(key) == "hash":
                    fileHashList.append("hash" + ","+ str(df[key]) )
                else:
                    pass
                
                if isinstance(df[key], dict):

                    self.recurse_keys(df[key],fileHashList)

                elif isinstance(df[key], list):
                    for subDict in df[key]:
                        self.recurse_keys(subDict,fileHashList)



''' 
    def getInputFiles(self,invoked,exe_id):
        file_name = ""
        file_hash = ""
        if type(invoked) == type(dict()):
            if "file-name" in invoked.keys():
                file_name = invoked["file-name"]
                if "md5sum" in invoked.keys():
                    file_hash = invoked["md5sum"]
                    self.cursor.execute("INSERT INTO input_files VALUES (?,?,?);", (file_name, file_hash, exe_id))
                    self.conn.commit()
                elif "hash" in invoked.keys():
                    file_hash = invoked["hash"]
                    self.cursor.execute("INSERT INTO input_files VALUES (?,?,?);", (file_name, file_hash, exe_id))
                    self.conn.commit()
                elif "not_found" in invoked.keys():
                    #file_hash = str(invoked["not_found"])
                    file_hash = "not_found"
                    self.cursor.execute("INSERT INTO input_files VALUES (?,?,?);", (file_name, file_hash, exe_id))
                    self.conn.commit()

            else:
                for key, value in invoked.items():
                    if key == "verbose":
                        print("--verbose--",str(value))
                    elif type(value) == type(dict()):
                        self.getInputFiles(value,exe_id)
                    elif type(value) == type(list()):
                        for val in value:
                            if type(val) == type(dict()):
                                self.getInputFiles(val,exe_id)
'''
        
obj = provenanceTableFeeder()
obj.fillProvenanceTable()