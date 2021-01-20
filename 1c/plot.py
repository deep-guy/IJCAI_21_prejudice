import statistics as s
import numpy as np
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
from cpdModel import *
# import tikzplotlib


payoff = [[], [], [], []]
folders = ['prej_prej', 'prej_unprej', 'unprej_prej', 'unprej_unprej']

for i in range(4):
    with open('1c/models/' + folders[i] + '/500-500.pkl', 'rb') as f:
        model_list_20 = pickle.load(f)
        
    with open('1c/models/' + folders[i] + '/600-400.pkl', 'rb') as f:
        model_list_40 = pickle.load(f)
        
    with open('1c/models/' + folders[i] + '/700-300.pkl', 'rb') as f:
        model_list_60 = pickle.load(f)
        
    with open('1c/models/' + folders[i] + '/800-200.pkl', 'rb') as f:
        model_list_80 = pickle.load(f)
    
    with open('1c/models/' + folders[i] + '/900-100.pkl', 'rb') as f:
        model_list_100 = pickle.load(f)

    all_models = [model_list_20, model_list_40, model_list_60, model_list_80, model_list_100]

    for current_model in all_models:
        g1_lst = []
        g2_lst = []
        for model in current_model:
            g1_payoff = 0
            g2_payoff = 0
            for a in model.group_list[0]:
                g1_payoff += a.payoff
            for a in model.group_list[1]:
                g2_payoff += a.payoff
            g1_lst.append(g1_payoff/len(model.group_list[0]))
            g2_lst.append(g2_payoff/len(model.group_list[1]))
        payoff[i].append(s.mean(g1_lst)/s.mean(g2_lst))
    print("Finished loading " + folders[i])

x_axis = [1, 2, 3, 4, 5]

fig, (ax) = plt.subplots(1, 1, figsize =(5, 4))
# ax.grid(b=None)
ax.plot(x_axis, payoff[0], linewidth=1.5, linestyle='dashed', marker='o', markersize=5, color='b', label='G1, G2 prejudiced')
ax.plot(x_axis, payoff[1], linewidth=1.5, linestyle='dashed', marker='v', markersize=5, color='r', label='Only G1 prejudiced')
ax.plot(x_axis, payoff[2], linewidth=1.5, linestyle='dashed', marker='x', markersize=5, color='g', label='Only G2 prejudiced')
ax.plot(x_axis, payoff[3], linewidth=1.5, linestyle='dashed', marker='s', markersize=5, color='y', label='None')

ax.grid(False)
# Set the axis limits
# ax.xlim(0, 100000)
# ax.ylim(1, 1.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.24),
          ncol=2)
ax.set_xlabel("Size ratio G1 : G2", labelpad=-3)
ax.set_ylabel("Avg. Payoff of G1 / Avg. Payoff of G2", labelpad=-2)
plt.xticks(np.arange(1, 6), ['5:5', '6:4', '7:3', '8:2', '9:1'])
# tikzplotlib.clean_figure()
# tikzplotlib.save('4.1.3.tex')

plt.savefig('1_c.png', dpi=600, transparent=True, bbox_inches='tight')
print("Saved plot output as 1_c.png")