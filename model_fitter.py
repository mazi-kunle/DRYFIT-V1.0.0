#!/usr/bin/env python3


from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import warnings
import inspect
import json
import csv
from sklearn.metrics import mean_squared_error, r2_score
from thin_layer_models.report_generator import *
from thin_layer_models.fit_funcs import *
import sys


# ignore unneccesary warnings
warnings.filterwarnings('ignore')


def get_model_from_file(file):
    '''Read model from file
    '''
    models = {}
    file = sys.path[0] + '/thin_layer_models/' + file

    with open(file) as f:
        line = f.readline()
        while line:
            try:
                model, model_eqn = line.split(':')
                models[model] = model_eqn.strip()
                line = f.readline()

            except ValueError:
                break

    return models



def model_fitter(time, MR, best_model_list):
    '''The main function
    '''
    
    models = get_model_from_file('models.txt')
    data = {}
    flag = 0

    for i in models.keys():
        # get model equations
        model_eqn = models[i]

        # trim  whitespace and "&"
        model = i.replace(' &', '').replace(' ', '_').replace('-', '_').lower()

        try:
            # fit model --- initial trial using trf algorithm
            popt, pconv = curve_fit(eval(model), time, MR, method='trf', maxfev=200000)
            
            
            # get y with fitted model
            MR_model = eval(model)(time, *popt)

            # check if trf is not a good fit
            if (r2_score(MR, MR_model)) < 0:

                # fit model using lm algorithm
                popt, pconv = curve_fit(eval(model), time, MR, method='lm', maxfev=200000)
                # print(f'{model} fitted with lm')
                
                 # get y with fitted model
                MR_model = eval(model)(time, *popt)


            # get model parameters
            model_args = zip(get_args(eval(model)), popt[:].tolist())

            params = {
                'R_Square': r2_score(MR, MR_model),
                'SSE': float(np.sum((MR - MR_model) ** 2)),
                'RMSE': float(np.sqrt(mean_squared_error(MR, MR_model))),
                'Constants': dict(model_args)
            }

            # Get model of best fit based on max R_square and min RMSE
            if params['R_Square'] > flag:  # get maximum R_square

                best_model = {
                    'model name': i,
                    'model equation': model_eqn,
                    'constants': params['Constants'],
                    'time': time,
                    'MR1': MR, # experimental data
                    'MR2': eval(model)(np.array(range(0, max(time) + 1)), *popt) # predicted data
                }

                flag = params['R_Square']
            

            data[i] = params


        # handle exceptions
        except Exception as e:
            print(e)
            print(f'Error in model {i}')

            params = {
                'R_Square': 'NOT FOUND',
                'SSE': 'NOT FOUND',
                'RMSE': 'NOT FOUND',
                'Constants': 'OPTIMAL PARAMETERS NOT FOUND'
            }
            data[i] = params

    best_model_list.append(best_model)
    
    return data


