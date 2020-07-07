import json
import sys
import platform
import os
import os.path
from os import path
import sqlite3

class reportStatistics(object):
        
    def reportStatistics(self):
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

        
        conn = sqlite3.connect(os.path.join(cachePath, 'CONP.db'))
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(exeRecord_id) from summary_results WHERE summary_results.exit_code = 0 ")
        rows = cursor.fetchone()[0]
        print (rows)

        cursor.execute("SELECT pipeline_DOI,COUNT(pipeline_DOI) from summary_results GROUP BY pipeline_DOI HAVING COUNT(*) >= 1 ")
        list = cursor.fetchall()
        for r in list:
            print(r)
            doi = r[0]
            print(doi)
            pipDic = dict(len(list))