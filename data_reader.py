#!/usr/bin/env python3

'''This file handles file reading and data extraction'''
import os
import pandas as pd
import numpy as np



def file_reader(file_path: str):
	'''
	Parameters
	----------
	file_list : List
		A list of all data files
	'''
	data = {}

	# Get all sheet names
	sheet_names = pd.ExcelFile(file_path).sheet_names

	for sheet in sheet_names:
		df = pd.read_excel(file_path, sheet_name=sheet)

		
		columns = df.columns.tolist()
		print(columns)

		if len(columns) != 4:
			raise ValueError(f'Sheet:"{sheet}" in {file_path} is not properly formatted, Kindly read the documentation.')
			return 0

		try:
			# get temperature as key
			key = str(int(df[columns[0]].tolist()[0]))
			
			# get thickness
			thickness =df[columns[1]].tolist()[0]
			

			# get time
			time = np.array(df[columns[2]].tolist())
			
			# get moisture ratio
			MR = np.array(df[columns[3]].tolist())

		except Exception as e:
			raise ValueError(f'Sheet:"{sheet}" in {file_path} is not properly formatted, Kindly read the documentation.')


		else:
			# extract data into data dictionary
			new_data = {
				'time': time,
				'MR' : MR
			}

		if key in data.keys():
			data[key][thickness] = new_data
		else:
			data[key] = {
				thickness: new_data
			}

	return data