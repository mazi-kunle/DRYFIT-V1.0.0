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
            model, model_eqn = line.split(':')
            models[model] = model_eqn.strip()
            line = f.readline()

    
    return models



def model_fitter(time, MR):
    '''The main function
    '''
    
    models = get_model_from_file('models.txt')
    data = {}

    for i in models.keys():
        # trim  whitespace and "&"
        model = i.replace(' &', '').replace(' ', '_').lower()
        
        try:
            # fit model -initial trial using trf algorithm
            popt, pconv = curve_fit(eval(model), time, MR, method='trf', maxfev=50000)
            
            
            # get y with fitted model
            MR_model = eval(model)(time, *popt)

            # check if lm is not a good fit
            if (r2_score(MR, MR_model)) < 0:

                # fit model using lm algorithm
                popt, pconv = curve_fit(eval(model), time, MR, method='lm', maxfev=50000)
                # print(f'{model} fitted with lm')
                
                 # get y with fitted model
                MR_model = eval(model)(time, *popt)

            # check if lm is not a good fit
            # elif (r2_score(MR, MR_model)) < 0:

            #     # fit model using lm algorithm
            #     popt, pconv = curve_fit(eval(model), time, MR, method='dogbox', maxfev=10000)
            #     # print(f'{model} fitted with lm')
                
            #      # get y with fitted model
            #     MR_model = eval(model)(time, *popt)


            # get model parameters
            model_args = zip(get_args(eval(model)), popt[:])
            
            params = {
                'R_Square': r2_score(MR, MR_model),
                'SSE': np.sum((MR - MR_model) ** 2),
                'RMSE': np.sqrt(mean_squared_error(MR, MR_model)),
                'Constants': dict(model_args)
            }
            data[i] = params

        # handle exceptions
        except Exception as e:
            print(e)
            print(f'Error in model {i}')

            params = {
                'R_Square': '',
                'SSE': '',
                'RMSE': '',
                'Constants': {}
            }
            data[i] = params

    return data
