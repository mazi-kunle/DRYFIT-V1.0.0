'''This file handles all data writing'''

import pandas as pd
import xlsxwriter
import datetime
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side
import json


def generate_report(results):
    '''A function that appends results to file
    '''
    

    current_time = datetime.datetime.now() # get datestamp
    timestamp = current_time.strftime('%Y-%m-%d')

    # append datestamp to file
    temp = list(results.keys())[0]
    new_temp = f'{temp} degrees Celcius'

    thickness = list(results[temp].keys())
    new_thickness = [f'{i} mm' for i in thickness]

    newdata = {
        new_temp: {}
    }

    for i in range(len(thickness)):
        newdata[new_temp][new_thickness[i]] = results[temp][thickness[i]]

    filename = f'model_constants @{temp} _{timestamp}.txt'

    with open(filename, 'w') as f:
        json.dump(newdata, f, indent=4)
        f.write('\n')
    print(f'Data has been written to {filename}')


def write_csv(data, temp, thickness):
    '''
    This function writes data to
    a csv file
    '''
    current_time = datetime.datetime.now() # get datestamp
    timestamp = current_time.strftime('%Y-%m-%d')

    # append datestamp to file
    file_name = f'moisture_diffusivity_{timestamp}.csv'
    
    sample = 'Oven' # sample tested
    _repeat = f'Moisture diffusivity of {sample} samples at different thickness and temperatures (m^2/s)'
    
    # format temperatures
    temp_data = []
    for i in range(len(temp)):
    	new_temp = f'{temp[i]} degrees'

    	if i == 0:
    		_ = (_repeat, new_temp)
    	else:
    		_ = ('', new_temp)

    	temp_data.append(_)

    # create custom header
    headers = pd.MultiIndex.from_tuples(temp_data)

    index = [f'{i}mm' for i in thickness]

    # create dataframe
    df = pd.DataFrame(data, columns=headers, index=index)
    
    # df.to_excel(file_name) # convert dataframe to csv

    print(f'Data has been written successfully to {file_name}')

    return df


def gen_act_energy_report(Ea, thickness):
    '''
    generates a report for activation
    energy results
    '''
    # datestamp file
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d')
    file_name = f'Activation_energy_result_{timestamp}.csv'
    
    index = [f'{i}mm' for i in thickness]
    headers = ['Parameters'] + index
    data = [['Activation energy Ea (kJ/mol) for Oven samples'] + Ea]

    # generate csv file
    df = pd.DataFrame(data, columns=headers)
    # df.to_excel(file_name, index=False)

    print("Activation energy report generated successfully") 
    
    return df


def custom_csv_writer(temp, thickness, data, header, filename):
    '''
    this function writes data to a csv file
    '''
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d')
    file_name = f'{filename}_{timestamp}.csv'
    
    # format temperatures
    temp_data = []
    for i in range(len(temp)):
    	new_temp = f'{temp[i]} degrees'

    	if i == 0:
    		_ = (header, new_temp)
    	else:
    		_ = ('', new_temp)

    	temp_data.append(_)


    # create custom header
    headers = pd.MultiIndex.from_tuples(temp_data)
    index = [f'{i}mm' for i in thickness]

    df = pd.DataFrame(data, columns=headers, index=index) # create dataframe
    
    # df.to_csv(file_name) # convert dataframe to a csv file

    print(f'Data has been written successfully to {file_name}')

    return df


def model_report_writer(data, temp):
    '''
    pass
    '''
    result = []
    # main_key = list(data.keys())[temp] # get first level keys (temperature)
    thickness_list = list(data[temp].keys()) # get second level keys (thickness)

    models = list(data[temp][thickness_list[0]].keys()) # get models

    for i in range(len(models)):

        _ = [i+1,models[i]]

        for thickness in thickness_list:
            # get statistical indicators
            r_square = data[temp][thickness][models[i]]['R_Square']
            sse = data[temp][thickness][models[i]]['SSE']
            rmse = data[temp][thickness][models[i]]['RMSE']


            _.append(r_square)
            _.append(sse)
            _.append(rmse)

        result.append(_)

    return result


def create_dynamic_table(filename, main_headers, sub_headers, data, temp):
    '''
    creates and formats the models report sheet
    '''
    # create title
    title = f'Result summary of the statistical curve fitting analysis at {temp}oC'

    # Create a workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # merge 5 columns in the first row
    ws.merge_cells('A1:H1')

    # input title in merged cell
    ws['A1'] = title

    # Align title
    # ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws['A1'].font = Font(bold=True)

    # Dynamically set the main headers and merge cells
    col_start = 3  # Start column for main headers
    for i, header in enumerate(main_headers):
        col_end = col_start + len(sub_headers) - 1
        ws.merge_cells(start_row=2, start_column=col_start, end_row=2, end_column=col_end)
        ws.cell(row=2, column=col_start).value = header
        ws.cell(row=2, column=col_start).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=2, column=col_start).font = Font(bold=True)
        col_start = col_end + 1

    # Add the sub-headers below the main headers
    ws.append(["No.", "Model Name"] + sub_headers * len(main_headers))

    # Apply bold font and center alignment to sub-headers
    for cell in ws[3]:
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.font = Font(bold=True)

    # Append the data rows
    for row in data:
        ws.append(row)

    # Apply center alignment and borders to the entire table
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )

    for row in ws.iter_rows(min_row=2, max_row=len(data) + 3 , min_col=1, max_col=2 + len(main_headers) * len(sub_headers)):
        for cell in row:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d')
    filename = f'{filename}_{timestamp}.xlsx'

    # Save the workbook
    wb.save(filename)

    return 0


# def df_writer(df_list):
#     '''
#     function takes a list of dataframes and saves
#     them to different sheets in one excel file.
#     '''
#     # create timestamp
#     current_time = datetime.datetime.now()
#     timestamp = current_time.strftime('%Y-%m-%d')
#     file_name = f'Thermodynamics_Results_{timestamp}.xlsx'
    
#     # Create an Excel writer object
#     with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
#         df_list[0].to_excel(writer, sheet_name="Moisture Diffusivity",)  # First sheet
#         df_list[1].to_excel(writer, sheet_name="Activation Energy", index=False)  # Second sheet
#         df_list[2].to_excel(writer, sheet_name="Enthalpy" )  # Third sheet
#         df_list[3].to_excel(writer, sheet_name="Entropy")  # Forth sheet
#         df_list[4].to_excel(writer, sheet_name="Gibbs Free Energy")  # Fifth sheet

    
#     print("Excel file with multiple sheets saved successfully!")


def df_writer(df_list):
    '''
    function takes a list of dataframes and saves
    them to different sheets in one excel file.
    '''
    # create timestamp
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d')
    file_name = f'Thermodynamics_Results_{timestamp}.csv'


    with open(file_name, "w", newline='') as f:
        f.write("Moisture Diffusivity Data\n")  # Add a header
        df_list[0].to_csv(f)

        f.write("\nActivation Energy Data\n")
        df_list[1].to_csv(f, index=False)

        f.write("\nEnthalpy Data\n")
        df_list[2].to_csv(f)

        f.write("\nEntropy Data\n")
        df_list[3].to_csv(f)

        f.write("\nGibbs Free Energy Data\n")
        df_list[4].to_csv(f)

    
    print("Excel file with multiple sheets saved successfully!")

    return 0