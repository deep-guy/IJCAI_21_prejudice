import sys
from cpdModel import *
import statistics as s
import numpy as np
from tqdm import tqdm
import matplotlib
import pickle
import matplotlib.pyplot as plt


with open('4b/0_group.pkl', 'rb') as f:
    model_list_0 = pickle.load(f)
    
with open('4b/1_group.pkl', 'rb') as f:
    model_list_1 = pickle.load(f)
    
with open('4b/2_group.pkl', 'rb') as f:
    model_list_2 = pickle.load(f)
    
with open('4b/3_group.pkl', 'rb') as f:
    model_list_3 = pickle.load(f)
    
with open('4b/4_group.pkl', 'rb') as f:
    model_list_4 = pickle.load(f)

with open('4b/5_group.pkl', 'rb') as f:
    model_list_5 = pickle.load(f)

agent_payoff = [[], [], [], [], [], []]
for model in model_list_0:
    for a in model.agent_list:
        agent_payoff[0].append(a.payoff)

for model in model_list_1:
    for a in model.agent_list:
        agent_payoff[1].append(a.payoff)

for model in model_list_2:
    for a in model.agent_list:
        agent_payoff[2].append(a.payoff)

for model in model_list_3:
    for a in model.agent_list:
        agent_payoff[3].append(a.payoff)

for model in model_list_4:
    for a in model.agent_list:
        agent_payoff[4].append(a.payoff)

for model in model_list_5:
    for a in model.agent_list:
        agent_payoff[5].append(a.payoff)

payoff = []

for lst in agent_payoff:
    payoff.append(s.mean(lst))

print("-------------RESULTS------------")
print()
print("Payoff for 0 prejudiced groups:", payoff[0])
print("Payoff for 1 prejudiced groups:", payoff[1])
print("Payoff for 2 prejudiced groups:", payoff[2])
print("Payoff for 3 prejudiced groups:", payoff[3])
print("Payoff for 4 prejudiced groups:", payoff[4])
print("Payoff for 5 prejudiced groups:", payoff[5])


