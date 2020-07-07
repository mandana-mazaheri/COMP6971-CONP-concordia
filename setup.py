import setuptools

VERSION = '0.0'

'''
with open("README.md", "r") as fh:
    long_description = fh.read()
'''

DEPS = [
         "boutiques",
         #"sqlite3",
         "nltk",
         #"pandas",
         #"DataFrame",      #For pandas
         #"Series",          #For pandas
         "pyunpack",        #For CONP Dataset extractor
		 "pygithub",
         "datalad",
       ]

setuptools.setup(
        name='CONP_Recommender',  
        version=VERSION,
        author="Mandana Mazaheri, Aida Vahdani, Saman Soltani",
        author_email="mndmazaheri@gmail.com",
        description="Recommends pipeline-dataset compatible pairs for CONP datasets",
        long_description=open("./README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/mandana-mazaheri/CONP-recommender",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
            "Operating System :: OS Independent",
            ],
        include_package_data=True,
        # If any package contains *.txt or *.rst files, include them:
        package_data={ "": ["*.txt", "*.db", "*.zip"] },
        setup_requires=DEPS,
        install_requires=DEPS,
		#Puts CONP_Recommender.exe to python\Scripts folder
        entry_points={
        "console_scripts": [
            "CONP_Recommender=CONP_Recommender.CONP_Recommender:main",
            ],
        },
 )
