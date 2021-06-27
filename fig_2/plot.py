import sys
from cpdModel import *
import statistics as s
import numpy as np
from tqdm import tqdm
import matplotlib
import pickle
import matplotlib.pyplot as plt


print("Running model with 10 groups")
print()
model_list = []
for i in range(10):
    model = CPDModel(1000, 10, 50, False)
    for i in tqdm(range(1, 100000)):
        model.step(i)
    model_list.append(model)

with open('1b/model.pkl', 'wb') as output:
    pickle.dump(model_list, output, pickle.HIGHEST_PROTOCOL)

print("Saved 1b/model.pkl")

# with open('1b/model.pkl', 'rb') as f:
#     model_list = pickle.load(f)


agent_payoff = []
for model in model_list:
    for a in model.agent_list:
        agent_payoff.append((a.getId(), a.getGroupId(), a.payoff))


id_list = []        
payoff_list = [[], [], [], [], [], [], [], [], [], []]


for (i, j, k) in agent_payoff:
    
    if(j == 0):
        payoff_list[0].append(k)
    elif(j == 1):
        payoff_list[1].append(k)
    elif(j == 2):
        payoff_list[2].append(k)
    elif(j == 3):
        payoff_list[3].append(k)
    elif (j == 4):
        payoff_list[4].append(k)
    elif(j == 5):
        payoff_list[5].append(k)
    elif(j == 6):
        payoff_list[6].append(k)
    elif(j == 7):
        payoff_list[7].append(k)
    elif(j == 8):
        payoff_list[8].append(k)
    elif (j == 9):
        payoff_list[9].append(k)


payoff = []
# print(len(payoff_list), "***********************")
for lst in payoff_list:
    # print(len(lst))
    payoff.append(sum(lst)/len(lst))

# print(payoff)

payoff1 = [payoff[0], payoff[1], payoff[2], payoff[3], payoff[4]]
payoff2 = [payoff[5], payoff[6], payoff[7], payoff[8], payoff[9]]

lbl1 = ['$G1$', '$G2$', '$G3$', '$G4$', '$G5$']
lbl2 = ['$G6$', '$G7$', '$G8$', '$G9$', '$G10$']

x = np.arange(5)
x = x*10
fig, ax = plt.subplots()
ax.scatter(x, payoff1, color = 'r', s = 40, marker='o')
ax.scatter(x, payoff2, color = 'b', s = 40, marker='s')
plt.xticks(x, "")
plt.tick_params(axis = "x", which = "both", bottom = False, top = False)
ax.set_xlabel('Groups', fontweight ='bold') 
ax.set_ylabel('Average Payoff', fontweight ='bold') 
plt.ylim(300, 500)
plt.xlim(-5, 48)


for i, txt in enumerate(lbl1):
    ax.annotate(txt, (x[i], payoff1[i]))
for i, txt in enumerate(lbl2):
    ax.annotate(txt, (x[i], payoff2[i]))

    
m1, b1 = np.polyfit(x, payoff1, 1)
m2, b2 = np.polyfit(x, payoff2, 1)
# print(m1, m2)
ax.plot(x, m1*x+b1, linewidth=1.5, linestyle='dashed', color='r', label='Out-Group effect $(m=1.73)$')
ax.plot(x, m2*x+b2, linewidth=1.5, linestyle='dashed', color='b', label='In-Group effect $(m=0.70)$')

ax.legend(loc="lower right")
plt.savefig('1_b.png', dpi=600, transparent=True, bbox_inches='tight')

print("Saved output 1_b.png")



