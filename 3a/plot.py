import sys
from cpdModel import *
import statistics as s
import numpy as np
from tqdm import tqdm
import matplotlib
import pickle
import matplotlib.pyplot as plt


print("Running model with 5 groups, G4 G4 have 10 percent renegades")
model_list = []
for i in range(10):
    model = CPDModel(1000, 5, 50, False)
    for i in tqdm(range(1, 100000)):
        model.step(i)
    model_list.append(model)

with open('3a/model.pkl', 'wb') as output:
    pickle.dump(model_list, output, pickle.HIGHEST_PROTOCOL)

print("Model saved as 3a/model.pkl")


agent_payoff = []
for model in model_list:
    for a in model.agent_list:
        agent_payoff.append((a.getId(), a.getGroupId(), a.payoff))


id_list = []        
payoff_list = [[], [], [], [], [], []]


for (i, j, k) in agent_payoff:
    
    if(j == 0):
        payoff_list[0].append(k)
    elif(j == 1):
        payoff_list[1].append(k)
    elif(j == 2):
        payoff_list[2].append(k)
    elif(j == 3):
        payoff_list[3].append(k)
    elif(j == 4):
        payoff_list[4].append(k)

for model in model_list:
    for a in model.anti_agents:
        payoff_list[5].append(a.payoff)

payoff = []
# print(len(payoff_list), "***********************")
for lst in payoff_list:
    # print(len(lst))
    payoff.append(sum(lst)/len(lst))

barWidth = 0.6
fig, (ax) = plt.subplots(figsize = (5, 4))
   
# Set position of bar on X axis 
br1 = np.arange(6)  
   
# Make the plot 
ax.bar(br1, payoff, color ='r', width = barWidth, 
        edgecolor ='grey')  

plt.ylim(200, 400)
# Adding Xticks  
ax.set_xlabel("Groups")
ax.set_ylabel("Average payoff")
plt.xticks([r for r in range(len(payoff))], 
           ['G1', 'G2', 'G3', 'G4', 'G5', 'Renegade']) 

plt.savefig('3_a.png', dpi=600, transparent=True, bbox_inches='tight')
print("Figure saved as 3_a.png")