#!/usr/bin/env python3
'''
This is the main program
'''

from rich import print as rprint
import numpy as np
from data_reader import file_extractor, file_reader
from data_writer import *
from thermo.thermo_funcs import *
from thin_layer_models.model_fitter import model_fitter




def thermo_calc():
	'''
	function to handles all thermodynamics calculations
	'''
	files = file_extractor()  # extract files in /Data
	data = file_reader(files) # extract files in /Data

	# get keys
	keys = list(data.keys())
	# get temperatures
	temp = np.array([int(i) for i in keys])
	# get thickness
	thickness = list(data[keys[0]].keys())



	output = []

	for i in thickness:
		_ = [] # placeholder to temporary hold Deff

		for key in data.keys():
			try:
				time = data[key][i]['time'] # get time
				MR = data[key][i]['MR'] # get MR
			except Exception as e:
				print('Error!!! Pls Recheck data in files')
				continue
			else:
				Deff = d_eff(time, MR, i) # calculate moisture diffusivity.
			
				_.append(Deff)

		output.append(_) # format d_eff to be written

	# write moisture diffusivity report to file
	df1 = write_csv(output, temp, thickness)


	Ea_data = []
	lndo_data = []
	for Deff in output:
		Ea, lnDo = get_activation_energy(Deff, temp)
		Ea_data.append(Ea/1000)
		lndo_data.append(lnDo)
		    
	# generate activation energy result
	df2 = gen_act_energy_report(Ea_data, thickness)

	# generate enthalpy result
	enthalpy_data = [get_enthalpy(Ea_data[i]*1000, temp) for i in range(len(Ea_data))]
	df3 = custom_csv_writer(temp, thickness, enthalpy_data, 'Enthalpy data (j/mol) for oven samples', 'enthalpy_data') 

	# generate entropy result
	entropy_data = [get_entropy(lndo_data[i], temp) for i in range(len(Ea_data))]
	df4 = custom_csv_writer(temp, thickness, entropy_data, 'Entropy data (j/mol.K) for oven samples', 'entropy_data')

	# generate gibbs free energy result
	gibbs_data = [get_gibbs(get_enthalpy(Ea_data[i]*1000, temp), get_entropy(lndo_data[i], temp), temp) for i in range(len(Ea_data))]
	df5 = custom_csv_writer(temp, thickness, gibbs_data, 'Gibbs free energy data (j/mol) for oven samples', 'gibbs_energy_data')

	df_writer([df1, df2, df3, df4, df5])


	return data


data = thermo_calc()
# get keys
keys = list(data.keys())
# get temperatures
temp = np.array([int(i) for i in keys])
# get thickness
thickness_list = list(data[keys[0]].keys())

# rprint(data)


results = {}
model_list = []
for temp in keys:
	new_data = {}
	for thickness in thickness_list:
		time = data[temp][thickness]['time'] # get time
		MR = data[temp][thickness]['MR'] # get MR

		params = model_fitter(time, MR)
		
		
		if temp in new_data.keys():
			new_data[temp][thickness] = params

		else:
			new_data[temp] = {
				thickness: params
			}
		
	r_data = model_report_writer(new_data, temp)
	main_headers = [f'{i} mm' for i in thickness_list]
	sub_headers = ["(R²)", "SSE", "RMSE"]
	
	create_dynamic_table(f'model-result-{temp}', main_headers, sub_headers, r_data, temp)
	generate_report(new_data)
	# break

# rprint(new_data)
