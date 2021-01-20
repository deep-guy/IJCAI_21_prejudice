import random
from statistics import mean
import numpy as np
from numba import jit

@jit(nopython=True)
def payoffCalc(a, b):
    C = 3
    D = 1
    S = 0
    T = 5
    payoff = a * b * C + a * (1 - b) * S + (1 - a) * b * T + (1 - a) * (1 - b) * D
    return payoff

@jit(nopython=True)
def facalignCalc(f):
    f_inv = 1-f
    a_inc = 0.01
    b_inc = 0.08
    a_dec = 0.08
    b_dec = 0.2
    increase = ((b_inc - a_inc)*f_inv) + a_inc
    decrease = ((b_dec - a_dec)*f_inv) + a_dec
    return (increase, decrease)

def getAveragePayoff(agent_list):
    tot_avg = 0
    omissions = 0
    for a in agent_list:
        avg = a.getAveragePayoff()
        if (avg == 0):
            omissions += 1
        tot_avg += avg
    if (len(agent_list)-omissions == 0):
        return 0
    return tot_avg / (len(agent_list)-omissions)

def getAverageBias(agent_list):
    tot_avg = 0
    for a in agent_list:
        avg = a.getBias()
        tot_avg += avg
    return tot_avg / len(agent_list)

def getAverageAlign(agent_list):
    tot_avg = 0
    for a in agent_list:
        avg = a.fac_align
        tot_avg += avg
    return tot_avg / len(agent_list)