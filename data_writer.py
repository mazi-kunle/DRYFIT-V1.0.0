'''This file handles all data writing'''

import pandas as pd
import datetime
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side



def write_csv(data, temp, thickness):
    '''
    This function writes data to
    a csv file
    '''
    current_time = datetime.datetime.now() # get datestamp
    timestamp = current_time.strftime('%Y-%m-%d')

    # append datestamp to file
    file_name = f'moisture_diffusivity_{timestamp}.csv'
    
    _repeat = 'Moisture diffusivity for samples at different thickness and temperatures'
    
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
    
    df.to_csv(file_name) # convert dataframe to csv

    print(f'Data has been written successfully to {file_name}')

    return 0


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
    data = [['Activation energy Ea (kJ/mol)'] + Ea]

    # generate csv file
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(file_name, index=False)

    print("Activation energy report generated successfully") 
    
    return 0


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
    
    df.to_csv(file_name) # convert dataframe to a csv file

    print(f'Data has been written successfully to {file_name}')

    return 0


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
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
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


