# CONP Recommender

This project aims to provide tag-based and provenance-based recommendation systems to recommend [CONP datasets](https://portal.conp.ca/search) to [CONP Pipelines](https://portal.conp.ca/pipelines) and vice versa. 


### Installation:


1. Install [datalad](https://handbook.datalad.org/en/latest/intro/installation.html), in this installation you should install Git, and git-annex.
    
2. Install [CONP_Recommender](https://test.pypi.org/project/CONP-Recommender/0.0/)  (Open **git bash** as terminal on **windows**) or run

 `pip install -i https://test.pypi.org/simple/ CONP-Recommender==0.0`
 
 **OR** clone the whole repository and run 
 
 `pip install .` 
 
in the cloned directory

3. Run

   `$python -m nltk.downloader punkt stopwords` 


---

## CONP_Recommender is ready to use 

You can run these commands in Terminal:

	`$CONP_Recommender --version`
	
1. Firstly, you need to run `conp-dataset_installation.py`on your system to have the whole installed [conp-dataset](https://github.com/CONP-PCNO/conp-dataset) on your machine.

**On windows run it in Git Bash, it takes time**


2. Initialize the database

   `$CONP_Recommender install database`

3. Use provenance-based recommender

   `$CONP_Recommender recom prov`

4. Use tag-based recommender

   `$CONP_Recommender recom tag`

5. If you want to update the conp-dataset run

   `$CONP_Recommender init`




 



