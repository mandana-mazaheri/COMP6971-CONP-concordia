# CONP Recommender

This project aims to provide tag-based and provenance-based recommendation systems to recommend [CONP datasets](https://portal.conp.ca/search) to [CONP Pipelines](https://portal.conp.ca/pipelines) and vice versa. 

## Installation

Firstly, you need to install requirements

---

### On Windows and Linux:


1. Install [datalad](https://handbook.datalad.org/en/latest/intro/installation.html), in this installation you should install Git, and git-annex.
2. Install requirements

   `$pip install nltk`
    
   `$python -m nltk.downloader punkt stopwords` 
    
3. Install [CONP_Recommender](https://test.pypi.org/project/CONP-Recommender/0.0/)  (Open **git bash** as terminal) or run

 `pip install -i https://test.pypi.org/simple/ CONP-Recommender==0.0`


---

## CONP_Recommender is ready to use 

You can run these commands in Terminal:

	`$CONP_Recommender --version`

1. Extract the installed [conp-dataset](https://github.com/CONP-PCNO/conp-dataset) to your local machine

   `$CONP_Recommender init`

2. Initialize the database

   `$CONP_Recommender install database`

3. Use provenance-based recommender

   `$CONP_Recommender recom prov`

4. Use tag-based recommender

   `$CONP_Recommender recom tag`





 



