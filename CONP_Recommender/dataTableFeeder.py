import sys
import platform
import os
import os.path
from os import path
import sqlite3
import csv
from os import stat
import logging

class dataTableFeeder(object):

    def symlinkCount(self, folder):
        count = 0
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)

            #if os.path.isfile(path):
            if os.path.islink(path):
                count += 1
            elif os.path.isdir(path):
                count += self.symlinkCount(path)
        return count

    def dataladDataset(self, folder):
        count = 0
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)

            #if os.path.isfile(path):
            if os.path.islink(path):
                count += 1
            elif os.path.isdir(path):
                count += self.symlinkCount(path)
        return count

    def fillDataTable(self):
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
        
        root = os.path.join(os.environ['CONP_RECOMMENDER_PATH'], "conp-dataset", "projects")
        
        list_of_datasets_path = self.findDataset(root)
        print("Total num of datasets : ", len(list_of_datasets_path))
        #for dataset in list_of_datasets_path:
        #    print(dataset)
        conn = sqlite3.connect(os.path.join(os.environ['CONP_RECOMMENDER_PATH'], 'CONP.db'))
        HASH_KEYWORDS = ["MD5E-"]
        # HASH_KEYWORDS = ["/MD5E-", "/URL"]

        # conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS data_files")
        cursor.execute("""CREATE TABLE data_files (

                        ID INTEGER PRIMARY KEY,
                        Dataset text,
                        File_Name text,             
                        Hash_Function text,
                        Hsah_Value text ,
                        Commmit_Number text


                            )""")
        # comment after first time-----------
        # FOREIGN KEY (Hsah_Value) REFERENCES input_files (infile_hash)
        count = 0
        
        numOfFilesToProcess = 0
        numOfProcessedFiles = 0
        for dataset_path in list_of_datasets_path:
            numOfFilesToProcess += self.symlinkCount(dataset_path)
            #print(self.symlinkCount(dataset_path))
        
        keyDetected = 0    
        HASH_KEYWORDS = ["MD5E-"]
        for dataset_path in list_of_datasets_path:
            #dataset_name = str(dataset_path).split('\\')[-1]
            dataset_name = str(dataset_path).split(os.path.sep)[-1]
            #print(dataset_name)
            for path, subdirs, files in os.walk(dataset_path):
                for name in files:
                    #print(name)
                    path_fileName = os.path.join(path, name)
                    
                    #if os.path.islink(path_fileName):
                    #    print(os.readlink(path_fileName))

                    if os.path.islink(path_fileName):
                        numOfProcessedFiles += 1
                        print("\r" + str(numOfProcessedFiles) + " file of "+ str(numOfFilesToProcess) + " processed (" + str(int(numOfProcessedFiles * 100 / numOfFilesToProcess)) + "%)", end='')

                        #if os.path.getsize(os.path.join(path, name)) < 2000:
                        file_content = os.readlink(path_fileName)
                        #print(file_content)  

                        list_to_insert = []
                        
                        for hash_key in HASH_KEYWORDS:
                            if hash_key in file_content:
                                #keyDetected += 1
                                #print(keyDetected)
                                
                                file_name = (path_fileName.split(os.path.sep + "projects" + os.path.sep)[1]).split(os.path.sep)[-1]

                                # print(file_content)
                                string_lists = file_content.split("/")
                                # print("string_lists_", flush = True)
                                # print(string_lists)
                                if dataset_name and file_name:
                                    for string in string_lists:
                                        if hash_key.replace('/', '') in string:
                                            # print(string)
                                            string = string.replace('--', '-')
                                            sub_strings = string.split("-")
                                            # print(sub_strings)
                                            hash_function = sub_strings[0]
                                            # print("Fnction : " + hash_function)

                                            hash_value = sub_strings[2].split('.')[0]
                                            # print("Hash Value : " + hash_value)
                                            latest_commit = sub_strings[1]
                                            if not latest_commit:
                                                latest_commit = ""

                                            # print("Commit : " + latest_commit)
                                            try:
                                                cursor.execute("INSERT INTO data_files VALUES (?,?,?,?,?,?);", (
                                                count, dataset_name, file_name, hash_function, hash_value, latest_commit))
                                                conn.commit()
                                                # print("after database", flush = True)
                                                count = count + 1
                                                #print("Count : " + str(count))
                                            except sqlite3.IntegrityError:
                                                logging.error("duplicated file in dataset: ", dataset_name, "\n file name: ",file_name)

                                            break


        conn.close()



    def findDataset(self,root):
        list_of_datasets_path = []
        for path in os.listdir(root):
            path = os.path.join(root, path)

            #print("********", path)
            if os.path.exists(os.path.join(path, 'DATS.json')):
                list_of_datasets_path.append(path)
            elif os.path.isdir(path):
                list_of_datasets_path += self.findDataset(path)
            
        return list_of_datasets_path

        '''
            path = os.path.join(folder, filename)


            #if os.path.isfile(path):
            if os.path.islink(path):
                count += 1
            elif os.path.isdir(path):
                count += self.symlinkCount(path)
        return count


        #for path, subdirs, files in os.walk(root):
        for 
            if (os.path.isdir(path)):
                if (os.listdir(path).__contains__('DATS.json')):
                    list_of_datasets_path.append(path)
        return list_of_datasets_path
        '''

