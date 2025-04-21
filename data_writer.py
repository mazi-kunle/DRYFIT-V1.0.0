'''This file handles all data writing'''


import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side
import pandas as pd
import random
from rich import print as rprint
import xlsxwriter


def generate_report(data, folder_path):
    '''A function that appends results to file
    '''
    

    current_time = datetime.datetime.now() # get datestamp
    timestamp = current_time.strftime('%Y-%m-%d')

    # Extract unique models, constants, thicknesses (preserving order)
    model_constants = {}
    thicknesses = set()
    temperatures = list(data.keys())

    for temp_data in data.values():
        for thick, thickness_data in temp_data.items():
            thicknesses.add(thick)
            for model, model_data in thickness_data.items():
                if model not in model_constants:
                    model_constants[model] = []
                for const in model_data["Constants"].keys():
                    if const not in model_constants[model]:
                        model_constants[model].append(const)

    # Convert thicknesses to a list (sorted if needed)
    thicknesses = sorted(list(thicknesses))

    # Prepare rows and track model boundaries
    rows = []
    sn = 1
    model_boundaries = {}  # {model: (first_row, last_row)}

    current_row = 3  # Starting after headers
    for model in model_constants:
        constants = model_constants[model]
        first_row = current_row
        for i, const in enumerate(constants):
            row = [sn if i == 0 else '', model if i == 0 else '', const]
            for temp in temperatures:
                for thick in thicknesses:
                    value = ""
                    try:
                        value = data[temp][thick][model]["Constants"].get(const, "")
                    except KeyError:
                        pass
                    row.append(value)
            rows.append(row)
            current_row += 1
        model_boundaries[model] = (first_row, current_row - 1)
        sn += 1

    # Create workbook and sheet
    wb = Workbook()
    ws = wb.active

    # Define styles
    center = Alignment(horizontal="center", vertical="center")
    bold_font = Font(bold=True)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    thick_bottom_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thick')
    )

    # Create header rows
    ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column=1)
    ws.merge_cells(start_row=1, start_column=2, end_row=2, end_column=2)
    ws.merge_cells(start_row=1, start_column=3, end_row=2, end_column=3)

    ws.cell(row=1, column=1).value = "S/N"
    ws.cell(row=1, column=2).value = "Models"
    ws.cell(row=1, column=3).value = "Constants"

    ws.cell(row=1, column=1).font = bold_font
    ws.cell(row=1, column=2).font = bold_font
    ws.cell(row=1, column=3).font = bold_font

    col = 4
    for temp in temperatures:
        ws.merge_cells(start_row=1, start_column=col, end_row=1, end_column=col + len(thicknesses) - 1)
        ws.cell(row=1, column=col).value = f'{temp} °C'
        ws.cell(row=1, column=col).font = bold_font
        for i, thick in enumerate(thicknesses):
            cell = ws.cell(row=2, column=col + i)
            cell.value = f'{thick} mm'
            cell.font = bold_font
            cell.alignment = center
            cell.border = thin_border
        col += len(thicknesses)

    # Align and border header cells
    for row in ws.iter_rows(min_row=1, max_row=2):
        for cell in row:
            cell.alignment = center
            cell.border = thin_border

    # Add the data with proper borders
    for r_idx, row_data in enumerate(rows, start=3):
        is_model_last_row = any(r_idx == last for (_, last) in model_boundaries.values())
        
        for c_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.value = val
            cell.alignment = center
            
            # Apply appropriate border
            if is_model_last_row:
                cell.border = thick_bottom_border
            else:
                cell.border = thin_border

            # Bold model names
            if c_idx == 2 and val != '':
                cell.font = bold_font


    filename = f'{folder_path}/model_constants_{timestamp}.xlsx'

    try:
        # Save file
        wb.save(filename)
    except Exception as e:
        print('Error found when writing model constants')
    else:
        print(f'Data has been written to {filename}')

    return 0


def write_csv(data, temp, thickness):
    '''
    This function writes data to
    a csv file
    '''
    current_time = datetime.datetime.now() # get datestamp
    timestamp = current_time.strftime('%Y-%m-%d')

    # append datestamp to file
    file_name = f'moisture_diffusivity_{timestamp}.csv'
    
    # sample = 'Papaya (RW)' # sample tested
    _repeat = f'Moisture diffusivity of samples at different thickness and temperatures (m^2/s)'
    
    # format temperatures
    temp_data = []
    for i in range(len(temp)):
    	new_temp = f'{temp[i]} °C'

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
    data = [['Activation energy Ea (kJ/mol)'] + Ea]

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
    	new_temp = f'{temp[i]} °C'

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


def create_dynamic_table(filename, folder_path, main_headers, sub_headers, data, temp, model_data=None):
    '''
    creates and formats the models report sheet
    '''
    # create title
    title = f'Result summary of the statistical curve fitting analysis at {temp} °C'

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

    

    # Handle writing of best model details
    
    # # Border and font styles
    # thin = Side(border_style="thin", color="000000")
    # border = Border(left=thin, right=thin, top=thin, bottom=thin)
    # center = Alignment(horizontal="center", vertical="center")
    # bold_font = Font(bold=True)
    # title_font = Font(bold=True)

    # # Title row (merged and styled)
    # ws.merge_cells("A30:D30")
    # ws["A31"] = "Model of Best Fit"
    # ws["A31"].font = title_font
    # ws["A31"].alignment = center

    # # Header row
    # headers = ["S/N", "MODEL NAME", "", "MODEL CONSTANTS"]
    # for col, header in zip(["A", "B", "C", "D"], headers):
    #     cell = ws[f"{col}32"]
    #     cell.value = header
    #     cell.font = bold_font
    #     cell.alignment = center
    #     cell.border = border

    # # Row 33 — Model serial and name
    # ws["A33"] = 1
    # ws["A33"].alignment = center
    # ws["A33"].border = border

    # ws["B33"] = model_data["model name"]
    # ws["B33"].font = bold_font
    # ws["B33"].alignment = center
    # ws["B33"].border = border

    # # Row 34 — Model equation
    # ws["B34"] = model_data["model equation"]
    # ws["B34"].alignment = center
    # ws["B34"].border = border

    # # Constants section (from row 34 down)
    # row = 33
    # for const, value in model_data["constants"].items():
    #     ws[f"C{row}"] = const
    #     ws[f"D{row}"] = value

    #     ws[f"C{row}"].alignment = center
    #     ws[f"D{row}"].alignment = center

    #     ws[f"C{row}"].border = border
    #     ws[f"D{row}"].border = border

    #     row += 1

    # # Fill in any missing cells with empty strings and apply borders/centering
    # for r in range(32, row):
    #     for col in ["A", "B", "C", "D"]:
    #         cell = ws[f"{col}{r}"]
    #         if cell.value is None:
    #             cell.value = ""
    #         cell.border = border
    #         cell.alignment = center

    # # Auto-adjust column widths (approximate by max length of content)
    # for col in ["A", "B", "C", "D"]:
    #     max_length = max(len(str(ws[f"{col}{r}"].value)) for r in range(31, row))
    #     ws.column_dimensions[col].width = max(10, max_length + 2)

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d')
    filename = f'{folder_path}/{filename}_{timestamp}.xlsx'

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


def df_writer(df_list, folder_path):
    '''
    function takes a list of dataframes and saves
    them to different sheets in one excel file.
    '''
    # create timestamp
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d')
    file_name = f'{folder_path}/Thermodynamics_Results_{timestamp}.csv'


    with open(file_name, "w", newline='') as f:
        f.write("Moisture Diffusivity Data\n")  # Add a header
        df_list[0].to_csv(f)

        if all(i is not None for i in df_list[1:]):
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



def make_dir():
    '''
    This function creates a result folder to 
    contain all results generated
    '''
    from pathlib import Path
    import time

    # use current time as a unique identifier for every folder created
    current_time = datetime.datetime.now()
    folder_name = f'RESULTS_{time.time()}'

    desktop_path = Path.home() / "Desktop"  # Get desktop path
    folder_path = desktop_path / folder_name  # Full path to new folder
    
    folder_path.mkdir(parents=True, exist_ok=True) # create folder
    print(f"Folder created at: {folder_path}")

    return folder_path



def groupby_thickness(new_data, best_model_list, thickness_list, temp):
    '''
    '''
    for i in range(len(thickness_list)):
            if thickness_list[i] not in new_data.keys():
                new_data[thickness_list[i]] = {
                    temp: best_model_list[i]
                }
            else:
                new_data[thickness_list[i]][temp] = best_model_list[i]

    return 0


def plot_drying_curve(best_model_results, folder_path):
    '''
    This function plots and saves the drying curve
    to folder path using the data in best_model_results
    '''

    # colors = ['red', 'black', 'blue', 'green', 'purple']
    linestyle = ['--', '-.', '-', ':']
    markers = ['v', '*', '+', 'x', '^','o']

    
    for thickness in best_model_results.keys():

        plt.figure(figsize=(10, 6))

        for temp in best_model_results[thickness].keys():
            
            # extract time and moisture ratio (experimental and predicted)
            time = best_model_results[thickness][temp]['time']
            MR1 = best_model_results[thickness][temp]['MR1'] # experimental moisture ratio
            MR2 = best_model_results[thickness][temp]['MR2'] # predicted moisture ratio
 
        
            random.shuffle(markers)
            plt.scatter(time, MR1, label=f'Experimental: {temp} Degrees Celcius', 
                marker=random.choice(markers))
                       

            plt.plot(list(range(0, max(time)+1)), MR2, label=f'Predicted: {temp} Degrees Celcius',
                linestyle=random.choice(linestyle))


        plt.legend(fontsize=10, title_fontsize=12, loc="upper right")

        plt.xlabel("Time (mins)", fontsize=12)
        plt.ylabel("Moisture Ratio (Dry Basis)", fontsize=12)
        plt.title(f'Drying Curve for {thickness}mm thickness')

        # Optional: grid for better readability
        plt.grid(True, linestyle='--', alpha=0.5)

        # Display the plot
        plt.tight_layout()
        plt.savefig(f'{folder_path}/Drying_Curve_{thickness}.jpg', dpi=300)
        plt.close()


def plot_drying_rate_curve(best_model_results, folder_path):
    '''
    '''

    for thickness in best_model_results.keys():

        plt.figure(figsize=(10, 6))
        
        for temp in best_model_results[thickness].keys():
            
            # extract time and moisture ratio (predicted)
            time = best_model_results[thickness][temp]['time']

            time2 = np.array(range(0, max(time) + 1))
            MR2 = best_model_results[thickness][temp]['MR2'] # predicted moisture ratio
            
            drying_rate = -np.diff(MR2) / np.diff(time2)
            drying_rate_arr = np.insert(drying_rate, 0, 0) # insert 0 at index 0



            plt.plot(time2, drying_rate_arr, label=f'{temp} Degrees Celcius')


        plt.legend(fontsize=10, title_fontsize=12, loc="upper right")

        plt.xlabel("Time (mins)", fontsize=12)
        plt.ylabel("Drying Rate (per mins)", fontsize=12)
        plt.title(f'Drying Rate Curve ({thickness}mm)')

        # Optional: grid for better readability
        plt.grid(True, linestyle='--', alpha=0.5)

        # Display the plot
        plt.tight_layout()
        plt.savefig(f'{folder_path}/Drying_Rate_Curve_{thickness}.jpg', dpi=300)
        plt.close()


def  plot_krischer_curve(best_model_results, folder_path):
    '''
    '''

    for thickness in best_model_results.keys():

        plt.figure(figsize=(10, 6))

        for temp in best_model_results[thickness].keys():
        
            # extract time and moisture ratio (predicted)
            time = best_model_results[thickness][temp]['time']

            time2 = np.array(range(0, max(time) + 1))
            MR2 = best_model_results[thickness][temp]['MR2'] # predicted moisture ratio
            
            drying_rate = -np.diff(MR2) / np.diff(time2)
            drying_rate_arr = np.insert(drying_rate, 0, 0) # insert 0 at index 0

        
            plt.plot(MR2, drying_rate_arr, label=f'{temp} Degrees Celcius')


        plt.legend(fontsize=10, title_fontsize=12, loc="upper left")

        plt.xlabel("Moisture ratio (Dry Basis)", fontsize=12)
        plt.ylabel("Drying Rate (per mins)", fontsize=12)
        plt.title(f'Krischer Curve ({thickness}mm)')

        # Optional: grid for better readability
        plt.grid(True, linestyle='--', alpha=0.5)

        # Display the plot
        plt.tight_layout()
        plt.savefig(f'{folder_path}/Krischer_Curve_{thickness}.jpg', dpi=300)
        plt.close()

    return 0



def plot_handler(best_model_results, folder_path):
    '''
    This function handles the drawing of the 
    required plots: Drying curve,
    Drying rate curve and Krischer curve.
    '''
    
    # plot drying curve
    plot_drying_curve(best_model_results, folder_path)

    # plot drying rate curve
    plot_drying_rate_curve(best_model_results, folder_path)
    
    # plot krischer curve
    plot_krischer_curve(best_model_results, folder_path)

    
    return 0
