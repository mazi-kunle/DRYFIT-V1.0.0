#!/usr/bin/env python3

import numpy as np

'''this file contains all the models
'''


def modified_henderson_pabis(x, a, b, c, g, h, k):
    return (a*np.exp(-k*x)) + (b*np.exp(-g*x))+ (c*np.exp(-h*x))

def henderson_pabis(x, a, k):
    return a*np.exp(-k*x)

def weibull(x, a, b, n, k):
    return (a-b)*(np.exp(-k*(x**n)))

def page(x, n, k):
    return np.exp(-k*(x**n))

def modified_page(x, n, k):
    return np.exp(-(k*x)**n)

def haghi_ghanadzadeh(x, a, b, c, d, e, f):
    return a*np.exp(-b*(x**c))+(d*(x**2))+(e*x)+f

def verma_et_al(x, a, g, k):
    return (a*np.exp(-k*x))+((1-a)*np.exp(-g*x))

def midilli_et_al(x, a, b, k, n):
    return a*np.exp(-k*x)+(b*x)

def peleg(x, a, b):
    return 1-(x/(a+(b*x)))

def newton(x, k):
    return np.exp(-k*x)

def logarithmic(x, a, k, c):
    return a*np.exp(-k*x) + c 

def silva_et_al(x, a, b):
    return np.exp((-a*x) - (b*np.sqrt(x)))

def wang_and_singh(x, a, b):
    return 1 + a*x + b*(x**2)

def two_term(x, a, k, b, g):
    return a*np.exp(-k*x) + b*np.exp(-g*x)

def demir_et_al(x, a, k, n, b):
    return a*np.exp(-k*x)**n + b

def hill_et_al(x, a, k, n, b, g):
    return a*np.exp(-k*(x**n)) + b*np.exp(-g*(x**n))

