import os
from github import Github
from datalad import api

'''
g = Github()
repo = g.get_repo("CONP-PCNO/conp-dataset")
contents = repo.get_contents("projects")  # List of "ContentFile"

x = api.Dataset('testDatalad')
#print( x.path)
'''
api.install(source='https://github.com/CONP-PCNO/conp-dataset.git',recursive = True, path = 'your dataset destination')
