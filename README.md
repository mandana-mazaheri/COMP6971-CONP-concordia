# CONP Recommender

This project aims to provide tag-based and provenance-based recommendation systems to recommend [CONP datasets](https://portal.conp.ca/search) to [CONP Pipelines](https://portal.conp.ca/pipelines) and vice versa. 


### Installation:  


1. Make sure Git, and [git-annex](https://git-annex.branchable.com/install/) are installed on your machine

2. Clone the whole repository and run thic command in the cloned directory
 
 `pip install .` 

3. Make sure you have the stopwords for NLTK

   `python -m nltk.downloader punkt stopwords` 


---

## CONP_Recommender is ready to use 

You can run these commands in Terminal:

`CONP_Recommender --version`
	
1. Make sure your git is properly congigured, the instruction is [here](https://docs.github.com/en/github/using-git/setting-your-username-in-git).

2. Clone [conp-dataset](https://github.com/CONP-PCNO/conp-dataset) and set the path for the result

`CONP_Recommender init`

2. Initialize the database

`CONP_Recommender install database`

3. Use provenance-based recommender

`CONP_Recommender recom prov`

4. Use tag-based recommender

`CONP_Recommender recom tag`

5. If you want to update the conp-dataset run

`CONP_Recommender update`

   
--on **windows** work on **git bash** as terminal

** You could see the result of the CONP_Recommnder on a summary dashboard which is available on : https://github.com/Aidavhd/CONP-Provenance-Dashboard **


 



