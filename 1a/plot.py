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

with open('1a/20.pkl', 'rb') as f:
    model_list_20 = pickle.load(f)
    
with open('1a/40.pkl', 'rb') as f:
    model_list_40 = pickle.load(f)
    
with open('1a/60.pkl', 'rb') as f:
    model_list_60 = pickle.load(f)
    
with open('1a/80.pkl', 'rb') as f:
    model_list_80 = pickle.load(f)
    
with open('1a/100.pkl', 'rb') as f:
    model_list_100 = pickle.load(f)

x_axis = []
y_axis1 = []
y_axis2 = []
y_axis3 = []
y_axis4 = []
y_axis5 = []

for i in range(1, 100):
    x_axis.append(1000*i)
    y_axis1.append(0)
    y_axis2.append(0)
    y_axis3.append(0)
    y_axis4.append(0)
    y_axis5.append(0)

for model in model_list_20:
    l1 = model.payoff_list[0]
    l2 = model.payoff_list[1]
    for i in range(len(l1)):
        ratio = l1[i]/l2[i]
        y_axis1[i] += ratio
        
for model in model_list_40:
    l1 = model.payoff_list[0]
    l2 = model.payoff_list[1]
    for i in range(len(l1)):
        ratio = l1[i]/l2[i]
        y_axis2[i] += ratio
        
for model in model_list_60:
    l1 = model.payoff_list[0]
    l2 = model.payoff_list[1]
    for i in range(len(l1)):
        ratio = l1[i]/l2[i]
        y_axis3[i] += ratio
        
for model in model_list_80:
    l1 = model.payoff_list[0]
    l2 = model.payoff_list[1]
    for i in range(len(l1)):
        ratio = l1[i]/l2[i]
        y_axis4[i] += ratio
        
for model in model_list_100:
    l1 = model.payoff_list[0]
    l2 = model.payoff_list[1]
    for i in range(len(l1)):
        ratio = l1[i]/l2[i]
        y_axis5[i] += ratio
        
        
for i in range(len(y_axis1)):
    y_axis1[i] = y_axis1[i]/10
    y_axis2[i] = y_axis2[i]/10
    y_axis3[i] = y_axis3[i]/10
    y_axis4[i] = y_axis4[i]/10
    y_axis5[i] = y_axis5[i]/10


for i in range(len(x_axis)):
    x_axis[i] = x_axis[i]/100000

fig, (ax) = plt.subplots(1, 1, figsize =(5, 4))
# ax.grid(b=None)
ax.plot(x_axis, y_axis1, linewidth=1.5, marker='o', markersize=5, markevery=10, color='k', label='$\epsilon_{G1} = 0.2$')
ax.plot(x_axis, y_axis2, linewidth=1.5, marker='v', markersize=5, markevery=10, color='r', label='$\epsilon_{G1} = 0.4$')
ax.plot(x_axis, y_axis3, linewidth=1.5, marker='x', markersize=5, markevery=10, color='g', label='$\epsilon_{G1} = 0.6$')
ax.plot(x_axis, y_axis4, linewidth=1.5, marker='s', markersize=5, markevery=10, color='y', label='$\epsilon_{G1} = 0.8$')
ax.plot(x_axis, y_axis5, linewidth=1.5, marker='D', markersize=5, markevery=10, color='b', label='$\epsilon_{G1} = 1.0$')
ax.grid(False)
# Set the axis limits
# ax.xlim(0, 100000)
# ax.ylim(1, 1.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.24), ncol=3)
ax.set_xlabel("Number of iterations $ / 10^5 $")
ax.set_ylabel("Avg. Payoff of G1 / Avg. Payoff of G2")

plt.savefig('1_a.png', dpi=600, transparent=True, bbox_inches='tight')
print("Saved plot output as 1_a.png")