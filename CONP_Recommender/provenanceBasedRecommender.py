import json
import sys
import platform
import os
import os.path
from os import path
import sqlite3
from tabulate import tabulate
import codecs
import logging


class provenanceBasedRecommender(object):
	def init(self):
		
		self.conn = sqlite3.connect( os.path.join(os.environ['CONP_RECOMMENDER_PATH'], 'CONP.db'))
		self.cursor = self.conn.cursor()

	def datasetGroup(self):
			self.cursor.execute("SELECT Dataset,Hsah_Value FROM data_files WHERE Hsah_Value IN (SELECT Hsah_Value FROM data_files GROUP BY Hsah_Value HAVING COUNT(*) >= 2)")
			list = self.cursor.fetchall()
			#print(list)
			duplicateHashList = {}

			for line in list:
				commonDatasets = []
				hash = line[1]
				dataset	= line[0]
				if(hash in duplicateHashList.keys()):

					if not(dataset in duplicateHashList[hash]):
						duplicateHashList[hash].append(dataset)
				else:
					commonDatasets.append(dataset)
					duplicateHashList[hash] = commonDatasets

			sameDatasets = []
			for h in duplicateHashList:
				datasets = duplicateHashList[h]
				if(len(datasets) > 1):
					if not datasets in sameDatasets:
						sameDatasets.append(datasets)
			#print(sameDatasets)				
			return sameDatasets

	def fillDicsFromRecords(self):	
		

		#conn.execute("PRAGMA foreign_keys = 1")
				
		self.datasetDict = {}
		self.successfullPipeline = []
		self.pipelinesDict = {} # a dictionary to store all successful datasets for each pipeline
		self.successfullDatasets = []
		pipelineInfo = self.cursor.execute("SELECT pipeline_DOI, pipeline_name FROM summary_results")

		self.pipelineInfoDict = {}
		for record in pipelineInfo:
			pipDOI = record[0]
			pipName = record[1]
			if not pipDOI in self.pipelineInfoDict:
				self.pipelineInfoDict[pipDOI] = pipName

		#print(pipelineInfoDict)


		summaryRecords = self.cursor.execute("SELECT pipeline_DOI, Dataset, exit_code FROM summary_results")

		# filling pipeline dict
		for record in summaryRecords:
			pipline_doi = record[0]
			dataset_name = record[1]
			run_status = str(record[2])
			#print(pipline_doi,dataset_name,run_status)
			if(run_status == "0"):
				if not dataset_name == None:
					if(pipline_doi in self.pipelinesDict.keys()):
						self.successfullDatasets = self.pipelinesDict[pipline_doi]
						if not dataset_name in self.successfullDatasets:
							self.successfullDatasets.append(dataset_name)
					else:
						self.successfullDatasets = [dataset_name]
						self.pipelinesDict[pipline_doi] = self.successfullDatasets


		summaryRecords = self.cursor.execute("SELECT pipeline_DOI, Dataset, exit_code FROM summary_results")
		# filling dataset dict
		for record in summaryRecords:
			
			pipline_doi = record[0]
			dataset_name = record[1]
			run_status = str(record[2])
			if(run_status == "0"):
				if not dataset_name == None:
					if(dataset_name in self.datasetDict.keys()):
						self.successfullPipeline = self.datasetDict[dataset_name]
						if not pipline_doi in self.successfullPipeline:
							self.successfullPipeline.append(pipline_doi)
							self.datasetDict[dataset_name] = self.successfullPipeline
					else:
						self.successfullPipeline = [pipline_doi]
						self.datasetDict[dataset_name] = self.successfullPipeline
					
		self.datasetsGroupList = self.datasetGroup()
		#print(self.datasetsGroupList)

		
	def updateDatasetGroupForPipeline(self):
		
		for pipeline in self.pipelinesDict: 				# to create a group of all datasets that have at least one common file for each dataset
			datasetList = self.pipelinesDict[pipeline]
			#print(pipeline)
			for group in self.datasetsGroupList:
				if(set(datasetList) & set(group)):
					datasetList = list(set(datasetList) | set(group))
					self.pipelinesDict[pipeline] = datasetList

	def updatePipelineGroupForDataset(self):
		
		for datasetName in self.datasetDict: 				# to create a group of all datasets that have at least one common file for each dataset
			pipelineList = self.datasetDict[datasetName]
			#print(pipeline)
			for group in self.datasetsGroupList:
				if datasetName in group:
					for subDataset in group:
						if not subDataset == datasetName:
							if subDataset in self.datasetDict.keys():
								subPipelineList = self.datasetDict[subDataset]
								if(set(pipelineList) & set(subPipelineList)):
									joinedPipelines = list(set(pipelineList)| set(subPipelineList))
									self.datasetDict[datasetName] = joinedPipelines
									self.datasetDict[subDataset] = joinedPipelines


	def recommendDatasetForPipeline(self,candidate_pipeline, allPipelines):
		if candidate_pipeline in allPipelines.keys():
			candidatedatasetGroup = allPipelines[candidate_pipeline]
			for pipeline in allPipelines:
				self.datasetsGroupList = allPipelines[pipeline]
				if(set(self.datasetsGroupList) & set(candidatedatasetGroup)):
					combinedDatasets = list(set(self.datasetsGroupList) | set(candidatedatasetGroup))
					allPipelines[pipeline] = combinedDatasets
					allPipelines[candidate_pipeline] = combinedDatasets

			return allPipelines[candidate_pipeline]
		else:
			return "Not successful execution exists for this pipeline"


	def recommendPipelineForDataset(self,candidate_dataset, allDatasets):
		if candidate_dataset in allDatasets.keys():
			candidatePipelineGroup = allDatasets[candidate_dataset]
			for datset in allDatasets:
				pipelineGroup = allDatasets[datset]
				if(set(pipelineGroup) & set(candidatePipelineGroup)):
					combinedPipelines = list(set(pipelineGroup) | set(candidatePipelineGroup))
					allDatasets[candidate_dataset] = combinedPipelines
					allDatasets[datset] = combinedPipelines

			return allDatasets[candidate_dataset]
		else:
			return "Not successful execution exists for this pipeline"

	def writeToJson(self,path,fileName, contents):
		
		pathFileName = path+'/'+fileName+'.json'
		#with open(pathFileName, 'w' , 'utf-8') as file:
			#parsed = str(json.loads(contents))
		filehandle = codecs.open(pathFileName,'w','utf-8')
		newContent = json.dumps(contents,indent = 4, sort_keys = True)
		filehandle.write(newContent+'\n')
			#print(pathFileName)

	def recommendForAllPipelinesAndDatasets(self):
		pipContents = {}
		dataContents = {}
		pip_wholeList = []
		data_wholeList = []
		self.init()
		self.fillDicsFromRecords()
		linesOfPipelineTable = []
		linesOfDatasetTable = []

		for pipeline in self.pipelinesDict.keys():
			eachPipInfo = {}
			self.updateDatasetGroupForPipeline()
			self.updatePipelineGroupForDataset()
			pipName = self.pipelineInfoDict[pipeline]
			pipDetailInfo = {}
			pipDetailInfo["name"] = pipName
			pipDetailInfo["DOI"] = pipeline

			eachPipInfo["pipline_info"] = pipDetailInfo


			#print(pipeline)
			linesOfPipelineTable = (self.recommendDatasetForPipeline(pipeline,self.pipelinesDict))
			eachPipInfo["recommended_datasets"] = linesOfPipelineTable
			pip_wholeList.append(eachPipInfo)

			#pipContents[pipeline] = eachPipInfo


		for dataset in self.datasetDict.keys():
			eachDataInfo = {}
			self.updateDatasetGroupForPipeline()
			self.updatePipelineGroupForDataset()
			#print(pipeline)
			
			eachDataInfo["dataset_name"] = dataset
			linesOfDatasetTable = (self.recommendPipelineForDataset(dataset,self.datasetDict))
			
			listOfRecomPip = []
			for pip in linesOfDatasetTable:
				#pipDOI_name = {}
				#pipDOI_name["pipeline_DOI"] = pip
				#pipDOI_name["pipeline_name"] = self.pipelineInfoDict[pip]
				listOfRecomPip.append(self.pipelineInfoDict[pip])
				#pipDOI_name[pip] = self.pipelineInfoDict[pip]


			eachDataInfo["recommended_pipelines"] = listOfRecomPip
			#dataContents[dataset] = eachDataInfo
			data_wholeList.append(eachDataInfo)

		
		pipContents["results_for_pipelines"] = pip_wholeList
		dataContents["results_for_datasets"] = data_wholeList
		self.writeToJson(os.environ['CONP_RECOMMENDER_PATH'],'recommendForPiplines',pipContents)
		self.writeToJson(os.environ['CONP_RECOMMENDER_PATH'],'recommendForDatasets',dataContents)
		




