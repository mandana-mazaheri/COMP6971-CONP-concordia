import sys
import platform
import os.path
from os import path
from pyunpack import Archive
from github import Github
from datalad import api
from tabulate import tabulate
#Since CONP_Recommender will be a folder in python, all modules should be addressed
#from sit-packages from Python
from CONP_Recommender import dataTableFeeder
from CONP_Recommender import pipelineCrawler
from CONP_Recommender import datasetDats
from CONP_Recommender import provenanceTableFeeder
from CONP_Recommender import reportResults
from CONP_Recommender import reportStatistics
from CONP_Recommender import provenanceBasedRecommender
from CONP_Recommender import tagBasedRecommender
'''
import dataTableFeeder
import pipelineCrawler
import datasetDats
import provenanceTableFeeder
import reportResults
import reportStatistics
'''

class CONP_Recommender(object):

	def __init__(self):
		self.dataTableFeeder = dataTableFeeder.dataTableFeeder()
		self.pipelineCrawler = pipelineCrawler.pipelineCrawler()
		self.datasetDats = datasetDats.datasetDats()
		self.provenanceTableFeeder = provenanceTableFeeder.provenanceTableFeeder()
		self.reportResults = reportResults.reportResults()
		self.reportStatistics = reportStatistics.reportStatistics()
		self.provenanceBasedRecommender = provenanceBasedRecommender.provenanceBasedRecommender()
		self.tagBasedRecommender = tagBasedRecommender.tagBasedRecommender()


		self.fillDataTableCalled = False
		self.getAndFillPipelineCalled = False
		self.provenanceTableFeederCalled = False
		self.reportResultsCalled = False
		self.reportStatisticsCalled = False
		self.getAndFillDatsTableCalled = False

		#print("CONP_Recommender Initialized")

	def loadConfig(self):
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

		if not os.path.exists(os.path.join(cachePath, "config.bin")):
			#os.mkdir(os.path.join(cachePath, "config.bin"))
			print("Initialize CONP_Recommender by \"CONP_Recommender init\"")

	def fillDataTable(self):
		self.dataTableFeeder.fillDataTable()
		self.fillDataTableCalled = True

	def getAndFillPipeline(self):
		self.pipelineCrawler.getAndFillPipeline()
		self.getAndFillPipelineCalled = True
	def fillDatsTable(self):
		self.datasetDats.findDatsFiles()

	def provenanceTableFeederService(self):
		self.provenanceTableFeeder.fillProvenanceTable()
		self.getAndFillDatsTableCalled = True

	def reportResultsTable(self):
		self.loadConfig()
		#print(self.fillDataTableCalled, self.getAndFillPipelineCalled , self.provenanceTableFeederCalled)
		#if self.fillDataTableCalled and self.getAndFillPipelineCalled and self.provenanceTableFeederCalled:
		self.reportResults.reportResultsFunc()
		self.reportResultsCalled = True

	def reportStatistics(self):
		if self.reportResultsCalled:
			self.reportStatistics.reportStatistics()

	def recommendProvenanceBased(self):
		#self.provenanceBasedRecommender.init()
		#self.provenanceBasedRecommender.fillDicsFromRecords()
		self.provenanceBasedRecommender.recommendForAllPipelinesAndDatasets()
	def recommendTagBased(self):
		self.tagBasedRecommender.recommend()

	def process(self,argv):
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

		#print( "This is the name of the script: ", sys.argv[0])
		#print("Number of arguments: ", len(sys.argv))
		#print("The arguments are: " , str(sys.argv))
		if len(argv) > 0:
			if str(argv[0]) in ['-v', '--version']:
				print("CONP_Recommender version 0.0")
			elif str(argv[0]) == 'init':
				source = os.path.join(os.path.dirname(__file__), "conp-dataset.zip")
				destination = cachePath
				if path.exists(os.path.join(cachePath, "conp-dataset")):
					userAnswer = input("conp-dataset extracted before. overwrite it? (y/n)")
					if userAnswer in ['y', 'Y', 'yes', 'YES']:
						print("conp-dataset is extracting", flush=True)
						print("plase wait . . .", flush=True)
						#sys.stdout.flush()
						Archive(source).extractall(destination)
						print("conp-dataset extracted successfully")
				else:
					print("conp-dataset is extracting", flush=True)
					print("plase wait . . .", flush=True)
					#sys.stdout.flush()
					Archive(source).extractall(destination)
					print("conp-dataset extracted successfully", flush=True)

			
			elif str(argv[0]) == 'update':  ####Problem,should be run in bash
				#api.install(source='https://github.com/CONP-PCNO/conp-dataset.git', path = cachePath)
				api.install(source='https://github.com/CONP-PCNO/conp-dataset.git',recursive = True, path = os.path.join(cachePath, "conp-dataset"))
				'''
					g = Github()
					repo = g.get_repo("CONP-PCNO/conp-dataset")
					contents = repo.get_contents("projects")  # List of "ContentFile"
					api.install(source='https://github.com/CONP-PCNO/conp-dataset.git',recursive = True, path = cachePath)
				'''
			elif str(argv[0]) == 'install':
				for item in argv[1:len(argv)]:
					if str(item) == 'database':
						#homePath = os.path.join(os.getenv('HOMEDRIVE'),os.getenv('HOMEPATH'))
						homePath = os.path.expanduser('~')
						
						provenancePath = os.path.join(homePath,'.cache')
						if not path.exists(provenancePath):
							os.mkdir(provenancePath)
						
						provenancePath = os.path.join(homePath,'.cache','boutiques')
						if not path.exists(provenancePath):
							os.mkdir(provenancePath)
						
						provenancePath = os.path.join(homePath,'.cache','boutiques','data')
						if not path.exists(provenancePath):
							os.mkdir(provenancePath)
						
						#replace with pull boutiques
						print("use boutique to pull...this should be fixed...")
						source = os.path.join(os.path.dirname(__file__), "data.zip")
						destination = os.path.join(homePath,'.cache','boutiques')
						Archive(source).extractall(destination)
						print("data folder containing provenances extracted successfully")

						print("Please waite... it takes a while to fill the database")
						self.fillDataTable()
						print("data_files table has been filled")
						#elif str(item) == 'provenance': # After bosh data pu;; is ok DELETE THESE

						self.provenanceTableFeederService()
						print("provenance table has been filled")
						self.reportResultsTable()
						print("reults table has been filled")
						self.getAndFillPipeline()
						self.fillDatsTable()
						print("pipeline table has been filled")

				"""				
				elif str(argv[0]) == 'FillDataTable':
					print("install FillDataTable")
					#self.fillDataTable()
				elif str(argv[0]) == 'FillPipelineTable':
					print("install FillPipelineTable")
					self.getAndFillPipeline()
					self.fillDatsTable()

				elif str(argv[0]) == 'FillProvenanceTable':
					print("install FillProvenanceTable")
				"""
			elif str(argv[0]) == 'recom':
				#self.reportResultsTable()
				if argv[1]:
					if str(argv[1]) == 'prov':
						self.recommendProvenanceBased()
						print("provenanced-based recommender, recommendForPiplines.json and recommendForDatasets.json is created in ")
						'''
						linesOfPipelineTable,linesOfDatasetTable = self.recommendProvenanceBased()
						print(tabulate(linesOfPipelineTable,headers=["pipeline","List Of Datasets"],tablefmt="grid"))
						print('\n\n\n')
						print(tabulate(linesOfDatasetTable,headers=["dataset","List Of pipelines"],tablefmt="grid"))
						'''
					elif str(argv[1]) == 'tag':
						print("tag-based recommender")
						self.recommendTagBased()

		else:
			print("Insert at least 1 item")



def main(args=None):
	#print(sys.argv[1:len(sys.argv)])

	recommender = CONP_Recommender()
	#recommender.process(["init"])
	recommender.process(sys.argv[1:len(sys.argv)])
	
