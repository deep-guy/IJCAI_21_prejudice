import sys
from cpdModel import *
import statistics as s
import numpy as np
from tqdm import tqdm
import matplotlib
import pickle
import matplotlib.pyplot as plt

print("Running model with two groups and renegades")
model_list = []
for i in range(10):
    model = CPDModel(1000, 40)
    for i in tqdm(range(1, 100000)):
        model.step(i)
    model_list.append(model)

with open('3b/model.pkl', 'wb') as output:
    pickle.dump(model_list, output, pickle.HIGHEST_PROTOCOL)

print("Model saved as 3b/model.pkl")

# with open('3a/model.pkl', 'rb') as f:
#     model_list = pickle.load(f)


x_axis = []
y_axis1 = []
y_axis2 = []
y_axis3 = []
y_axis4 = []

for i in range(1, 1000):
    x_axis.append(100*i)
    y_axis1.append(0)
    y_axis2.append(0)
    y_axis3.append(0)
    

for model in model_list:
    l1 = model.bias_list[0]
    l2 = model.bias_list[1]
    l3 = model.bias_list[2]
    for i in range(len(l1)):
        y_axis1[i] += l1[i]
        y_axis2[i] += l2[i]
        y_axis3[i] += l3[i]
for i in range(len(y_axis1)):
    y_axis1[i] = y_axis1[i]/10
    y_axis2[i] = y_axis2[i]/10
    y_axis3[i] = y_axis3[i]/10

fig, (ax) = plt.subplots(1, 1, figsize =(5, 4))
# ax.grid(b=None)
ax.plot(x_axis, y_axis1, linewidth=1.5, marker='o', markersize=4, markevery=100, color='b', label='$G1$')
ax.plot(x_axis, y_axis2, linewidth=1.5, marker='v', markersize=4, markevery=100, color='r', label='$G2$')
ax.plot(x_axis, y_axis3, linewidth=1.5, marker='x', markersize=4, markevery=100, color='g', label='$R$')
# ax.plot(x_axis, y_axis4, linewidth=1.5, marker='s', markersize=5, markevery=100, color='y', label='$\epsilon_{G1} = 0.8$')
# ax.plot(x_axis, y_axis5, linewidth=1.5, marker='D', markersize=5, markevery=100, color='b', label='$\epsilon_{G1} = 1.0$')
ax.grid(False)
# Set the axis limits
# ax.xlim(0, 100000)
plt.ylim(0.2, 0.6)
ax.legend(loc='upper left', ncol=3)
ax.set_xlabel("Number of iterations")
ax.set_ylabel("Avg. prejudice $(p)$")

plt.savefig('3_b.png', dpi=600, transparent=True, bbox_inches='tight')
print("Plot saved as 3_b.png")