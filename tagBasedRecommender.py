### import all neccessery libraries###
import os
import sqlite3
import nltk
from nltk.corpus import stopwords
import re
import math
import numpy
import json 
######################################


class tagBasedRecommender:

    ####computing TF values###############
    def computing_tf(self,dic,worddic):
        tfDic={}
        for i in dic:
            tem_dic={}
            tem_list = dic[i]
            lenght = len(tem_list)
            for word in tem_list:
                tf = worddic[i][word]/float(lenght)
                tem_dic[word]=tf
            tfDic[i] = tem_dic
        return tfDic
    #######################################



    ###computing IDF values################
    def computing_idf(self,uniquewords,dic):
        idfDic={}
        for word in uniquewords:
            N = len(dic)
            down = float(uniquewords[word])+1
            idf = math.log10(N/down)
            idfDic[word] = idf
        return idfDic
    ########################################



    ###calculating Dot Product##############
    def cosine(self,d1,d2):
        dot=0
        for i in d1:
            if i in d2:
                dot += d1[i] * d2[i]
        firstNumber=0
        secondNumber=0
        for i in d1:
            firstNumber += d1[i]*d1[i]
        for i in d2:
            secondNumber += d2[i]*d2[i]
        firstNumber = math.sqrt(firstNumber)
        secondNumber = math.sqrt(secondNumber)
        eucildean = firstNumber*secondNumber
        return dot/eucildean
    ########################################


    ###computing final values of tf-idf#####
    def computing_tfidf(self,tfDic,idfDic):
        tfidfDic ={}
        for each in tfDic:
            tem_dic={}
            for word in tfDic[each]:
                if word in idfDic:
                    tfidf = tfDic[each][word] * idfDic[word]
                else:
                    tfidf = tfDic[each][word] * 0
                tem_dic[word] = tfidf
            tfidfDic[each] = tem_dic
        return tfidfDic
    #########################################


    def recommend(self):

        ###retrive data from pipelenes table in database###
        #conn = sqlite3.connect(os.path.join(os.path.expanduser('~'), 'CONP_Recommender', 'CONP.db'))
        conn = sqlite3.connect( os.path.join(os.environ['CONP_RECOMMENDER_PATH'], 'CONP.db'))
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pipelines")
        rows = cursor.fetchall()
        ###################################################



        ###preparing data in order to pass them to tf-idf functions###
        dic={}
        for row in rows:
            ID = row[0]
            tags = row[1]
            des = row[2]
            tags_list=[]
            if(tags != None):
                tem_tags = tags.split(',')
            for i in tem_tags:
                if(":" in i):
                    j = i.split(": ")
                    j[1]=j[1].lower()
                    tags_list.append(j[1])
                else:
                    i = i.lower()
                    tags_list.append(i)
            tem_des = nltk.word_tokenize(des)
            stop_words = set(stopwords.words('english'))
            filtered_words=[]
            for each in tem_des:
                if not each in stop_words:
                    filtered_words.append(each)
            regex = re.compile('[^a-zA-Z]')
            for i in filtered_words:
                i = regex.sub("",i)
                if not (i==None or i==''):
                    i= i.lower()
                    tags_list.append(i)
            dic[ID] = tags_list
        ##############################################################



        ###calculating word accurances in pipelines###
        worddic={}
        uniquewords={}
        wordsList=[]
        for each in dic:
            tem_dic={}
            tem_list = dic[each]
            for i in tem_list:
                if not i in wordsList:
                    wordsList.append(i)
                if i in tem_dic:
                    tem_dic[i] += 1
                else:
                    tem_dic[i] = 1
            worddic[each] = tem_dic
        #############################################



        ###calculating unique words in courpse###
        for word in wordsList:
            for each in dic:
                if word in dic[each]:
                    if word in uniquewords:
                        uniquewords[word] += 1
                    else:
                        uniquewords[word] = 1
        ##########################################



        ###retrive data from dats table in database###
        cursor.execute("SELECT * FROM dats_table")
        rows = cursor.fetchall()
        ##############################################



        ###preparing data in order to pass them to tf-idf functions###
        dataset_dic={}
        for row in rows:
            name = row[0]
            keywords = row[1]
            des = row[2]
            tags_list=[]
            if(keywords != None):
                tem_keywords = keywords.split(',')
                for i in tem_keywords:
                    tags_list.append(i.lower())
            tem_des = nltk.word_tokenize(des)
            stop_words = set(stopwords.words('english'))
            filtered_words=[]
            for each in tem_des:
                if not each in stop_words:
                    filtered_words.append(each)
            regex = re.compile('[^a-zA-Z]')
            for i in filtered_words:
                i = regex.sub("",i)
                if not (i==None or i==''):
                    tags_list.append(i.lower())
            dataset_dic[name] = tags_list
        ##############################################################



        ###calculating word accurances in datasets###
        dataset_worddic={}
        dataset_uniquewords={}
        dataset_wordsList=[]
        for each in dataset_dic:
            tem_dic={}
            tem_list = dataset_dic[each]
            for i in tem_list:
                if not i in dataset_wordsList:
                    dataset_wordsList.append(i)
                if i in tem_dic:
                    tem_dic[i] += 1
                else:
                    tem_dic[i] = 1
            dataset_worddic[each] = tem_dic
        #############################################



        ###calculating unique words in courpse###
        for word in dataset_wordsList:
            for each in dataset_dic:
                if word in dataset_dic[each]:
                    if word in dataset_uniquewords:
                        dataset_uniquewords[word] += 1
                    else:
                        dataset_uniquewords[word] = 1
        #########################################

        ###calculating score and suggest a result to selected option###
        finalpipeline_dic={}
        finaldataset_dic={}
        PipelinetfDic = self.computing_tf(dic,worddic)
        PipelineidfDic = self.computing_idf(uniquewords,dic)
        PipelinetfidfDic = self.computing_tfidf(PipelinetfDic,PipelineidfDic)
        DatasettfDic = self.computing_tf(dataset_dic,dataset_worddic)
        DatasetidfDic = self.computing_idf(dataset_uniquewords,dataset_dic)
        DatasettfidfDic = self.computing_tfidf(DatasettfDic,DatasetidfDic)
        resultDicforpipeline={}
        for i in PipelinetfidfDic:
            datasetresultdic={}
            for j in DatasettfidfDic:
                result = self.cosine(PipelinetfidfDic[i],DatasettfidfDic[j])
                datasetresultdic[j] = result
            resultDicforpipeline[i] = datasetresultdic
        for each in resultDicforpipeline:
            datasetresult = resultDicforpipeline[each]
            List = []
            for i in datasetresult:
                List.append(datasetresult[i])
            median = numpy.median(List)
            resultlist=[]
            for i in datasetresult:
                if datasetresult[i] >= median:
                    resultlist.append(i)
            finalpipeline_dic[each] = resultlist
        resultdicfordataset={}
        for i in DatasettfidfDic:
            pipelineresultdic={}
            for j in PipelinetfidfDic:
                result = self.cosine(DatasettfidfDic[i],PipelinetfidfDic[j])
                pipelineresultdic[j] = result
            resultdicfordataset[i] = pipelineresultdic
        for each in resultdicfordataset:
            pipelineresult = resultdicfordataset[each]
            List=[]
            for i in pipelineresult:
                List.append(pipelineresult[i])
            median = numpy.median(List)
            resultlist = []
            for i in pipelineresult:
                if pipelineresult[i] >= median:
                    resultlist.append(i)
            finaldataset_dic[each] = resultlist
        ###writing result###############
        with open ('pipelineresult.json','w') as outfile:
            json.dump(finalpipeline_dic,outfile,indent=4)
        with open ('datasetresult.json','w') as outfile:
            json.dump(finaldataset_dic,outfile,indent=4)
        ###############################################################    
#obj = tagBasedRecommender()
#obj.recommend()