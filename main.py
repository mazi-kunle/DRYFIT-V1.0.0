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


folder_path = make_dir()



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


	# Handle type A: only one temperature
	if len(keys) == 1:
		# write moisture diffusivity report to file
		df1 = write_csv(output, temp, thickness)
		df_writer([df1, None, None, None, None], folder_path)

	else:
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
		df3 = custom_csv_writer(temp, thickness, enthalpy_data, 'Enthalpy data (j/mol)', 'enthalpy_data') 

		# generate entropy result
		entropy_data = [get_entropy(lndo_data[i], temp) for i in range(len(Ea_data))]
		df4 = custom_csv_writer(temp, thickness, entropy_data, 'Entropy data (j/mol.K)', 'entropy_data')

		# generate gibbs free energy result
		gibbs_data = [get_gibbs(get_enthalpy(Ea_data[i]*1000, temp), get_entropy(lndo_data[i], temp), temp) for i in range(len(Ea_data))]
		df5 = custom_csv_writer(temp, thickness, gibbs_data, 'Gibbs free energy data (j/mol)', 'gibbs_energy_data')

		
		df_writer([df1, df2, df3, df4, df5], folder_path)


	return data


data = thermo_calc()

# get keys
keys = list(data.keys())
# get temperatures
temp = np.array([int(i) for i in keys])
# get thickness
thickness_list = list(data[keys[0]].keys())

# rprint(data)


best_model_result = {}
# model_list = []
best_model_list = []
model_constants_dict = {}

for temp in keys:
	new_data = {}
	for thickness in thickness_list:
		time = data[temp][thickness]['time'] # get time
		MR = data[temp][thickness]['MR'] # get MR

		params = model_fitter(time, MR, best_model_list)
		
		
		if temp in new_data.keys():
			new_data[temp][thickness] = params

		else:
			new_data[temp] = {
				thickness: params
			}


	# group best_model_list by thickness 
	groupby_thickness(best_model_result, best_model_list, thickness_list, temp)

	best_model_list = [] # reset list 
	

	r_data = model_report_writer(new_data, temp)
	main_headers = [f'{i} mm' for i in thickness_list]
	sub_headers = ["(R²)", "SSE", "RMSE"]


	# create models statistical evaluation report
	create_dynamic_table(f'model-result-{temp}', folder_path, main_headers, sub_headers, r_data, temp)
	
	model_constants_dict.update(new_data)

# generate model constants report
generate_report(model_constants_dict, folder_path)


plot_handler(best_model_result, folder_path)





