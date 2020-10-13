import json
import sys
import platform
import os
import os.path
from os import path
import sqlite3


class reportResults(object):

	def reportResultsFunc(self):
		"""
		to fill summary_result table that makes us able to match datasets with pipelines through file hahses
		"""
		
		conn = sqlite3.connect(os.path.join(os.environ['CONP_RECOMMENDER_PATH'], 'CONP.db'))
		cursor = conn.cursor()
		cursor.execute("DROP TABLE IF EXISTS summary_results")
		cursor.execute("""CREATE TABLE summary_results (

				exeRecord_id INTEGER,
				infile_hash text,
				Dataset text,			 
				pipeline_DOI text,
				pipeline_name TEXT,
				exit_code TEXT


					)""")
		
		cursor.execute("""INSERT INTO summary_results SELECT input_files.exeRecord_id, input_files.infile_hash,
										data_files.Dataset,
										exe_records.pipeline_DOI,exe_records.pipeline_name , exe_records.exit_code
										
										FROM input_files 
										LEFT JOIN exe_records ON exe_records.ID = input_files.exeRecord_id
										LEFT JOIN data_files ON data_files.Hsah_Value = input_files.infile_hash""")


		
		conn.commit()
		