import sys
from cpdModel import *
import statistics as s
import numpy as np
from tqdm import tqdm
import matplotlib
import pickle
import matplotlib.pyplot as plt



model_list = []
for i in range(10):
    model = CPDModel(1000, 4, 50, False)
    for i in tqdm(range(1, 100000)):
        model.step(i)
    model_list.append(model)

with open('2b/model.pkl', 'wb') as output:
    pickle.dump(model_list, output, pickle.HIGHEST_PROTOCOL)


agent_payoff = []
for model in model_list:
    for a in model.agent_list:
        agent_payoff.append((a.getId(), a.getGroupId(), a.payoff))


id_list = []        
payoff_list = [[], [], [], []]


for (i, j, k) in agent_payoff:
    
    if(j == 0):
        payoff_list[0].append(k)
    elif(j == 1):
        payoff_list[1].append(k)
    elif(j == 2):
        payoff_list[2].append(k)
    elif(j == 3):
        payoff_list[3].append(k)

payoff = []
# print(len(payoff_list), "***********************")
for lst in payoff_list:
    # print(len(lst))
    payoff.append(sum(lst)/len(lst))


barWidth = 0.6
fig, (ax) = plt.subplots(figsize = (5, 4))
# Set position of bar on X axis 
br1 = np.arange(4)  
# Make the plot 
ax.bar(br1, payoff, color ='r', width = barWidth, 
        edgecolor ='grey')  


# Adding Xticks  
ax.set_xlabel("Size of Group", labelpad=-3)
ax.set_ylabel("Average payoff of Group", labelpad=-2)
plt.xticks([r for r in range(len(payoff))], ['100 (G1)', '200 (G2)', '300 (G3)', '400 (G4)']) 

plt.savefig('2_b.png', dpi=600, transparent=True, bbox_inches='tight')