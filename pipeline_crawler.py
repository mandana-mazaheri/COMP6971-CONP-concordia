#import all needed libraries
import pandas as pd
import boutiques as bosh
import os,sys
import json
import sqlite3
from csv import reader
import csv
print("import Done")    


#update pipleline list with maximum number 
max = sys.maxsize
maxString = '-m '+str(max)
pipelinefile = bosh.search(maxString)
PipeLineDOIlist=[]
for each in pipelinefile:
    for key in each:
        if (key == 'ID'):
            PipeLineDOIlist.append(each[key])

# pull pipelines
DirectoryList=[]
for i in PipeLineDOIlist:
    DirectoryList.append(bosh.pull(i))


#extract tags from each pipeline 
dic={} 
counter=0
lastcounter=counter
for i in DirectoryList:
        lastcounter = counter
        i = str(i).strip('[]') 
        i = str(i).strip("''") 
        with open(str(i)) as f: 
            data = json.load(f)
            for key in data:
                if key=='tags': 
                    dic[PipeLineDOIlist[counter]] = data[key]
                    counter += 1
            if(counter==lastcounter):
                dic[PipeLineDOIlist[counter]] = None
                counter += 1
                


#prepare each pipeline and their tags for inserting into table
FinalDic={}
for i in dic:
    tags=None
    if (dic[i] == None):
        FinalDic[i] = None
    else:
        for each in dic[i]:
                if isinstance(dic[i][each],list):
                    for s in dic[i][each]:
                        if (tags==None):
                            tags = str(each)+': '+str(s)
                        else:
                            tags = tags +','+str(s)
                else:
                    if(tags==None):
                        tags = str(each)+': '+str(dic[i][each])
                    else:
                        tags = tags+','+str(each)+': ' +str(dic[i][each])
        FinalDic[i] = tags


# create database and fill pipeline table
conn = sqlite3.connect('ProjectDatabase.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS pipelines")
c.execute("""create table pipelines(
       ID text,
       Tags text,
       PRIMARY KEY (
            ID )
       )""")
try:
    for each in FinalDic:
        idd = each
        tag = FinalDic[each]
        one_record = [(idd),(tag),]
        count = c.execute('INSERT INTO pipelines VALUES (?,?);', one_record)
        conn.commit()
    c.close()
except sqlite3.Error as error:
    print("recored error: ",error)
finally:
    if(conn):
        conn.close()

