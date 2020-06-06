import os
from github import Github
from datalad import api


GIHUB_USER = "....@gmail.com"
GIHUB_PASS = "your password"


g = Github(GIHUB_USER, GIHUB_PASS)
repo = g.get_repo("CONP-PCNO/conp-dataset")
contents = repo.get_contents("projects")  # List of "ContentFile"

x = api.Dataset('testDatalad')
#print( x.path)
api.install(source='https://github.com/CONP-PCNO/conp-dataset.git',recursive = True)
#os.chdir('C:/Test1/conp-dataset/projects')
#api.install(source ='https://github.com/emmetaobrien/1000GenomesProject.git')
#'https://github.com/CONP-PCNO/conp-dataset.git')
'''for content_file in contents:
    print(content_file)
    datalad.api.install(source='https://github.com/CONP-PCNO/conp-dataset.git')

    print("URL : " + content_file.path + " SHA1 : " + content_file.sha + "\n")
'''
