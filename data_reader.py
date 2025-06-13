#!/usr/bin/env python3

'''This file handles file reading and data extraction'''
import os
import pandas as pd
import numpy as np


# def file_extractor():
# 	'''
# 	This function extracts all excel files in the folder /Data
# 	'''
# 	# get list of all files in Data folder
# 	path = './Data'
# 	data = ['./Data/' + i for i in os.listdir(path) if i.endswith('.xlsx')]

# 	# check if Data folder is empty
# 	if len(data) == 0:
# 		print('No files found in ./Data')
# 		return 0

# 	return data


def file_reader(file_path: str):
	'''
	Parameters
	----------
	file_list : List
		A list of all data files
	'''
	# ensure file_list contains at least one file
	# if len(file_list) == 0:
	# 	print('File list is empty')
	# 	return 0

	data = {}

	# load the excel file
	excel_file = pd.ExcelFile(file_path)

	for sheet in excel_file.sheet_names:
		print(sheet)
		df = pd.read_excel(file_path, sheet_name=sheet)

		columns = df.columns.tolist()

		if len(columns) != 4:
			print(f'{file} is not properly formatted')
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
			print(f'{file} is not properly formatted')

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