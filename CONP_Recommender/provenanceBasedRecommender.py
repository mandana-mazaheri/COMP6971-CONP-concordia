import json
import sys
import platform
import os
import os.path
from os import path
import sqlite3
from tabulate import tabulate

class provenanceBasedRecommender(object):
	def init(self):
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

			return [candidate_pipeline,allPipelines[candidate_pipeline]]
		else:
			return [candidate_pipeline,"Not successful execution exists for this pipeline"]


	def recommendPipelineForDataset(self,candidate_dataset, allDatasets):
		if candidate_dataset in allDatasets.keys():
			candidatePipelineGroup = allDatasets[candidate_dataset]
			for datset in allDatasets:
				pipelineGroup = allDatasets[datset]
				if(set(pipelineGroup) & set(candidatePipelineGroup)):
					combinedPipelines = list(set(pipelineGroup) | set(candidatePipelineGroup))
					allDatasets[candidate_dataset] = combinedPipelines
					allDatasets[datset] = combinedPipelines

			return [candidate_dataset,allDatasets[candidate_dataset]]
		else:
			return [candidate_dataset,"Not successful execution exists for this pipeline"]



	def recommendForAllPipelinesAndDatasets(self):
		self.init()
		self.fillDicsFromRecords()
		linesOfPipelineTable = []
		linesOfDatasetTable = []
		self.updateDatasetGroupForPipeline()
		self.updatePipelineGroupForDataset()
		for pipeline in self.pipelinesDict.keys():
			#print(pipeline)
			linesOfPipelineTable.append(self.recommendDatasetForPipeline(pipeline,self.pipelinesDict))

		for dataset in self.datasetDict.keys():
			#print(pipeline)
			linesOfDatasetTable.append(self.recommendPipelineForDataset(dataset,self.datasetDict))
		return linesOfPipelineTable,linesOfDatasetTable

		#print(tabulate(linesOfPipelineTable,headers=["pipeline","List Of Datasets"],tablefmt="grid"))
		#print('\n\n\n')
		#print(tabulate(linesOfDatasetTable,headers=["dataset","List Of pipelines"],tablefmt="grid"))




'''
obj = provenanceBasedRecommender()
obj.init()
obj.fillDicsFromRecords()

obj.recommendForAllPipelinesAndDatasets()
'''
