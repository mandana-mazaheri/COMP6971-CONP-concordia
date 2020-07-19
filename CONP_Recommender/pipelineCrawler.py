import boutiques as bosh
import os,sys
import json
import sqlite3
from csv import reader
import csv
import platform
import os.path
from os import path
import logging



class pipelineCrawler(object):

    def getAndFillPipeline(self):
        '''
        osType = platform.system()
        cachePath = None
        if osType == 'Windows':
            cachePath = os.getenv('APPDATA')
        elif osType == 'Linux':
            cachePath = "~/.cache"
        '''
        '''
        cachePath = os.path.expanduser('~')
        
        if not os.path.exists(os.path.join(cachePath, "CONP_Recommender")):
            os.mkdir(os.path.join(cachePath, "CONP_Recommender"))

        cachePath = os.path.join(cachePath, "CONP_Recommender")

        '''
        root = os.path.join(os.environ['CONP_RECOMMENDER_PATH'], "conp-dataset", "projects")
        #print(root)
        #root = os.getcwd()+"/conp-dataset\\projects"
       
        conn = sqlite3.connect( os.path.join(os.environ['CONP_RECOMMENDER_PATH'], 'CONP.db'))

        #update pipleline list with maximum number
        x = 2
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
        description_dic={}
        nameDic={} 
        counter=0
        lastcounter=counter
        for i in DirectoryList:
                lastcounter = counter
                i = str(i).strip('[]') 
                i = (i).strip("''") 
                with open(str(i)) as f: 
                    data = json.load(f)
                    for key in data:
                        if key=='tags': 
                            dic[PipeLineDOIlist[counter]] = data[key]
                        if key == 'description':
                            description_dic[PipeLineDOIlist[counter]] = data[key]
                        if key == 'name':
                            nameDic[PipeLineDOIlist[counter]] = data[key]
                    if not (dic.__contains__(PipeLineDOIlist[counter])):
                        dic[PipeLineDOIlist[counter]] = None
                    counter +=1
                        
        #print(len(description_dic))

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
        #conn = sqlite3.connect('CONP.db')
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS pipelines")
        c.execute("""create table pipelines(
               Name text,
               ID text,
               Tags text,
               Descrption text,
               PRIMARY KEY (
                    ID )
               )""")
        try:
            for each in FinalDic:
                idd = each
                tag = FinalDic[each]
                if(description_dic[each] != None):
                    des = description_dic[each]
                else:
                    des = None
                pipelineName = nameDic[each]
                one_record = [(pipelineName),(idd),(tag),(des),]
                count = c.execute('INSERT INTO pipelines VALUES (?,?,?,?);', one_record)
                conn.commit()
            c.close()
        except sqlite3.Error as error:
            logging.error("recored error: ",error)
        finally:
            if(conn):
                conn.close()
