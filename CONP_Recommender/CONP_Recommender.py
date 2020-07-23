"""
@author Mandana Mazaheri, mndmazaheri@gmail.com

This script contains the main functions that run the CONP_Recommender API
CONP_Recommneder API helps us to install and collect required information, 
file hashes and dataset information from "https://github.com/CONP-PCNO/conp-dataset"
and provenance records from zenodo using boutiques pull  




"""


import sys
import platform
import os.path
from os import path
from pyunpack import Archive
from github import Github
import git
from datalad import api
from tabulate import tabulate
import logging
from CONP_Recommender import dataTableFeeder
from CONP_Recommender import pipelineCrawler
from CONP_Recommender import datasetDats
from CONP_Recommender import provenanceTableFeeder
from CONP_Recommender import reportResults
from CONP_Recommender import reportStatistics
from CONP_Recommender import provenanceBasedRecommender
from CONP_Recommender import tagBasedRecommender


class CONP_Recommender(object):
	"""
	The main class containing all refrences and commands
	"""

	def __init__(self):
		"""
		Creating objects for all necessary classes 
		"""

		logging.basicConfig(level = logging.INFO)

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

		

	def loadConfig(self):
		"""
		TODO: This function should be completed to check the execution steps
		"""
		
		if not os.path.exists(os.path.join(os.environ['CONP_RECOMMENDER_PATH'], "config.bin")):
			#os.mkdir(os.path.join(cachePath, "config.bin"))
			logging.info("Initialize CONP_Recommender by \"CONP_Recommender init\"")

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
		self.reportResults.reportResultsFunc()
		self.reportResultsCalled = True

	def reportStatistics(self):
		if self.reportResultsCalled:
			self.reportStatistics.reportStatistics()

	def recommendProvenanceBased(self):
		self.provenanceBasedRecommender.recommendForAllPipelinesAndDatasets()

	def recommendTagBased(self):
		self.tagBasedRecommender.recommend()

	def process(self,argv):
		"""
		Every command and operation is going to be handled here
		"""
		cachePath = os.path.expanduser('~')
		if not os.path.exists(os.path.join(cachePath, "CONP_Recommender")):
			os.mkdir(os.path.join(cachePath, "CONP_Recommender"))

		cachePath = os.path.join(cachePath, "CONP_Recommender")
		#set the default directory to store database and result of recommendations

		os.environ['CONP_RECOMMENDER_PATH'] = cachePath 
		# define an environment variable for this pupose


		#logging.info( "This is the name of the script: ", sys.argv[0])
		#logging.info("Number of arguments: ", len(sys.argv))
		#logging.info("The arguments are: " , str(sys.argv))
		if len(argv) > 0:
			if str(argv[0]) in ['-v', '--version']:
				logging.info("CONP_Recommender version 0.0")


			elif str(argv[0]) == 'init':
				"""
				to clone the conp-dataset repository and be able to extract all file hashes
				"""

				ans = input("The default path to store database is home/CONP_Recommender, do you want to change it?(y/n)")

				if str(ans.lower()) == ("y" or "yes"):
					os.environ['CONP_RECOMMENDER_PATH'] = input("Enter a directory path: ")
					while not os.path.exists(os.environ['CONP_RECOMMENDER_PATH']):
						os.environ['CONP_RECOMMENDER_PATH'] = input("Error, please enter a valid directory path: ")
				logging.info("The path to store conp-dataset and CONP.db is set as: " + os.environ['CONP_RECOMMENDER_PATH'])


				# clone datasets recursively
				logging.info("cloning git repo conp-dataset, takes a while")

				git.Git(os.environ['CONP_RECOMMENDER_PATH']).clone("--recurse-submodules","https://github.com/CONP-PCNO/conp-dataset.git")

				logging.info("cloned successfully")


				
			elif str(argv[0]) == 'update':

				repo = git.Repo(os.path.join(os.environ['CONP_RECOMMENDER_PATH'], "conp-dataset"))
				logging.info(repo.git.pull("--recurse-submodules"))


			elif str(argv[0]) == 'install':
				for item in argv[1:len(argv)]:
					if str(item) == 'database':
						"""
						by this command the database will be filled
						"""
						
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
						
						#replace with pull boutiques, this is a temporary solution to have provenance records
						logging.warning("use boutique to pull...this should be fixed...")
						source = os.path.join(os.path.dirname(__file__), "data.zip")
						destination = os.path.join(homePath,'.cache','boutiques')
						Archive(source).extractall(destination)
						logging.info("data folder containing provenances extracted successfully")

						logging.info("Please waite... it takes a while to fill the database")
						self.fillDataTable()
						logging.info("data_files table has been filled")
						

						self.provenanceTableFeederService()
						logging.info("provenance table has been filled")
						self.reportResultsTable()
						logging.info("reults table has been filled")
						self.getAndFillPipeline()
						self.fillDatsTable()
						logging.info("pipeline table has been filled")


			elif str(argv[0]) == 'recom':
				#self.reportResultsTable()
				if argv[1]:
					if str(argv[1]) == 'prov':
						self.recommendProvenanceBased()
						logging.info("provenanced-based recommender, recommendForPiplines.json and recommendForDatasets.json is created in " +os.environ['CONP_RECOMMENDER_PATH'])
						
					elif str(argv[1]) == 'tag':
						logging.info("tag-based recommender")
						self.recommendTagBased()

		else:
			logging.warning("Insert at least 1 item")



def main(args=None):
	recommender = CONP_Recommender()
	recommender.process(sys.argv[1:len(sys.argv)])
	
