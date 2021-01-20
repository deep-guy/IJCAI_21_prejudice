import statistics as s
import numpy as np
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
# import tikzplotlib
from cpdModel import *


model_list_20 = []
model_list_40 = []
model_list_60 = []
model_list_80 = []
model_list_100 = []

with open('4a/20.pkl', 'rb') as f:
    model_list_20 = pickle.load(f)
    
with open('4a/40.pkl', 'rb') as f:
    model_list_40 = pickle.load(f)
    
with open('4a/60.pkl', 'rb') as f:
    model_list_60 = pickle.load(f)
    
with open('4a/80.pkl', 'rb') as f:
    model_list_80 = pickle.load(f)
    
with open('4a/100.pkl', 'rb') as f:
    model_list_100 = pickle.load(f)

with open('4a/unbiased.pkl', 'rb') as f:
    model_list_unb = pickle.load(f)

payoff = []
agent_payoff = [[], [], [], [], []]
unb_payoff = []

for model in model_list_20:
    for a in model.agent_list:
        agent_payoff[0].append(a.payoff)
        
for model in model_list_40:
    for a in model.agent_list:
        agent_payoff[1].append(a.payoff)
        
for model in model_list_60:
    for a in model.agent_list:
        agent_payoff[2].append(a.payoff)
        
for model in model_list_80:
    for a in model.agent_list:
        agent_payoff[3].append(a.payoff)
        
for model in model_list_100:
    for a in model.agent_list:
        agent_payoff[4].append(a.payoff)

for model in model_list_unb:
    for a in model.agent_list:
        unb_payoff.append(a.payoff)
        
        
for lst in agent_payoff:
    payoff.append(sum(lst)/len(lst))

for i in range(len(payoff)):
    payoff[i] = payoff[i]/(sum(unb_payoff)/len(unb_payoff))

barWidth = 0.6
fig, (ax) = plt.subplots(figsize = (5, 4))
   
# Set position of bar on X axis 
br1 = np.arange(5)  
   
# Make the plot 
ax.bar(br1, payoff, color ='r', width = barWidth, 
        edgecolor ='grey', label ='Payoff')  

   
# Adding Xticks  
ax.set_xlabel('Societies', fontweight ='bold') 
ax.set_ylabel('Average Payoff Ratio S1/S2', fontweight ='bold') 
plt.xticks([r for r in range(len(payoff))], 
           ["S1", "S2", "S3", "S4", "S5"]) 

plt.savefig('4_a.png', dpi=600, transparent=True, bbox_inches='tight')