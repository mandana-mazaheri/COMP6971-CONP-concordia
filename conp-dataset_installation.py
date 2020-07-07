import sys
import platform
import os.path
from os import path
from github import Github
from datalad import api as api


cachePath = os.path.expanduser('~')
if not os.path.exists(os.path.join(cachePath, "CONP_Recommender")):
	os.mkdir(os.path.join(cachePath, "CONP_Recommender"))

cachePath = os.path.join(cachePath, "CONP_Recommender")

if not os.path.exists(os.path.join(cachePath, "conp-dataset")):
	os.mkdir(os.path.join(cachePath, "conp-dataset"))


#print(path)
api.install(source='https://github.com/CONP-PCNO/conp-dataset.git',recursive = True, path = os.path.join(cachePath, "conp-dataset"))
