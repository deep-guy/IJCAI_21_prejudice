import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from twoGroups.baseClass import *
from twoGroups.biasedAgent import *
from twoGroups.unbiasedAgent import *
from twoGroups.tftAgent import *
from twoGroups.faction import *
from twoGroups.antiAgent import *



import statistics as s
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import pickle

class CPDModel():
    def __init__(self, num_agents, num_factions, broadcasts=False, broadcast_percent=None):
        self.num_agents = num_agents
        self.agent_list = []
        self.broadcast = broadcasts
        self.broadcast_percentage = broadcast_percent if broadcast_percent is not None else random.random()
        self.group_list = [[], []]
        self.payoff_list = [[], []]
        self.bias_list = [[],[]]
        self.faction_list = []
        self.facalign_list = [[],[]]
        self.initial_bias_list = np.random.normal(0.5, 0.2, 1000).tolist()
        # self.national_median = 117
        self.upper_class_track = []
        self.anti_agents = []

        # Keeping a track of payoff difference
        self.payoff_diff = []

        for i in range(len(self.initial_bias_list)):
            if (self.initial_bias_list[i] >= 1):
                self.initial_bias_list[i] = 1
            elif (self.initial_bias_list[i] <= 0):
                self.initial_bias_list[i] = 0


        fac_agent_lists = []
        for i in range(num_factions):
            fac_agent_lists.append([])

        

        # Create agents and divide them in factions (Biased, S-TFT)
        for i in range(0, 200):
            grp_id = 0
            fac_id = int(i / 20)
            a = BiasedAgent(i, grp_id, self)
            fac_agent_lists[fac_id].append(a)
            self.group_list[grp_id].append(a)
            self.agent_list.append(a)

        for i in range(200, 500):
            grp_id = 0
            fac_id = int(i / 20)
            a = UnbiasedAgent(i, grp_id, self)
            fac_agent_lists[fac_id].append(a)
            self.group_list[grp_id].append(a)
            self.agent_list.append(a)

        for i in range(500, 700):
            grp_id = 1
            fac_id = int(i / 20)
            a = BiasedAgent(i, grp_id, self)
            fac_agent_lists[fac_id].append(a)
            self.group_list[grp_id].append(a)
            self.agent_list.append(a)

        for i in range(700, 1000):
            grp_id = 1
            fac_id = int(i / 20)
            a = UnbiasedAgent(i, grp_id, self)
            fac_agent_lists[fac_id].append(a)
            self.group_list[grp_id].append(a)
            self.agent_list.append(a)


        # Create Factions
        for i in range(num_factions):
            f = Faction(i, fac_agent_lists[i])
            self.faction_list.append(f)



    def step(self, step_number):
        '''Advance the model by one step.'''
        logging_granularity = 100
        # Select two agents from the agent list at random
        if (self.broadcast):
            rand = random.random()
            if (rand>0.60 and rand<0.61):
                # Perform broadcast Interaction
                # possible_broadcasting_agents = []
                # for a in self.agent_list:
                #     if(a.getSocialStatus() == 3):
                #         possible_broadcasting_agents.append(a)
                
                # if(len(possible_broadcasting_agents) == 0):
                #     for a in self.agent_list:
                #         if(a.getSocialStatus() == 2):
                #             possible_broadcasting_agents.append(a)


                [broadcasting_agent] = random.sample(self.group_list[0], 1)
                group_id = broadcasting_agent.getGroupId()
                size = len(self.group_list[group_id])
                size = int(size * self.broadcast_percentage)
                broadcast_group = random.sample(self.group_list[group_id], size)
                bias = broadcasting_agent.getBias()
                for i in broadcast_group:
                    i.recieveBroadcast(bias)

        #Perform normal interaction
        A, B = random.sample(self.agent_list, 2)
        coopA = A.getCoop(B)
        coopB = B.getCoop(A)
        payoffA = payoffCalc(coopA, coopB)
        payoffB = payoffCalc(coopB, coopA)
        
        self.payoff_diff.append(abs(payoffA - payoffB))

        A.update(B, coopB, payoffA, payoffB)
        B.update(A, coopA, payoffB, payoffA)

        # Update national median after each interaction
        # median_update_lst = []
        self.upper_class_track = []
        for a in self.agent_list:
        #     median_update_lst.append(a.getWealth())
            if(a.getSocialStatus() == 3):
                self.upper_class_track.append(a)
        
        # median_index = int(self.num_agents/2)
        # self.national_median = median_update_lst[median_index]
        
        # if (step_number % logging_granularity == 0):
        #     self.payoff_list[0].append(getAveragePayoff(self.group_list[0]))
        #     self.payoff_list[1].append(getAveragePayoff(self.group_list[1]))

        #     self.bias_list[0].append(getAverageBias(self.group_list[0]))
        #     self.bias_list[1].append(getAverageBias(self.group_list[1]))

        #     self.facalign_list[0].append(getAverageAlign(self.group_list[0]))
        #     self.facalign_list[1].append(getAverageAlign(self.group_list[1]))

print("Running expt with 40 precent prejudiced agents")
model_list = []
for r in range(10):
    model = CPDModel(1000, 50)
    for i in tqdm(range(1, 100000)):
        model.step(i)
    model_list.append(model)

with open('4a/40.pkl', 'wb') as output:
    pickle.dump(model_list, output, pickle.HIGHEST_PROTOCOL)