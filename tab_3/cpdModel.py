import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from nGroups.baseClass import *
from nGroups.biasedAgent import *
from nGroups.unbiasedAgent import *
from nGroups.tftAgent import *
from nGroups.faction import *
from nGroups.antiAgent import *

class CPDModel():
    def __init__(self, num_agents, num_groups, num_factions, broadcasts=False, broadcast_percent=None):
        self.num_agents = num_agents
        self.num_groups = num_groups  #Taken as 5 for this experiment
        self.agent_list = []
        self.broadcast = broadcasts
        self.broadcast_percentage = broadcast_percent if broadcast_percent is not None else random.random()
        self.minimum_biased_groups_threshold = 3 # We are not using this value
        self.faction_list = []
        self.group_list = []

        # Parameters for tracking change in bias/payoff
        self.payoff_list = []
        self.bias_list = []
        self.facalign_list = []

        # Setup:
        # 5 Groups of 200 agents each
        # Each group has 5 factions of 40 agents each
        # All agents are biased
        # Every Group is biased againt every other group

        # Initialize Group Lists
        for i in range(num_groups):
            self.group_list.append([])
            self.payoff_list.append([])
            self.bias_list.append([])
            self.facalign_list.append([])


        # Create Factions
        fac_agent_lists = []
        for i in range(num_factions):
            fac_agent_lists.append([])

        # Creating agents of Group 1
        for i in range(0, 100):
            fac_id = int(i / 20)
            grp_id = 0
            groups_biased_against = [5]
            a = BiasedAgent(i, grp_id, groups_biased_against, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        for i in range(100, 200):
            fac_id = int(i / 20)
            grp_id = 1
            groups_biased_against = [5, 6]
            a = BiasedAgent(i, grp_id, groups_biased_against, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        for i in range(200, 300):
            fac_id = int(i / 20)
            grp_id = 2
            groups_biased_against = [5, 6, 7]
            a = BiasedAgent(i, grp_id, groups_biased_against, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        for i in range(300, 400):
            fac_id = int(i / 20)
            grp_id = 3
            groups_biased_against = [5, 6, 7, 8]
            a = BiasedAgent(i, grp_id, groups_biased_against, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        for i in range(400, 500):
            fac_id = int(i / 20)
            grp_id = 4
            groups_biased_against = [5, 6, 7, 8, 9]
            a = BiasedAgent(i, grp_id, groups_biased_against, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)


        for i in range(500, 600):
            fac_id = int(i / 20)
            grp_id = 5
            # groups_biased_against = [0, 1]
            a = UnbiasedAgent(i, grp_id, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        for i in range(600, 700):
            fac_id = int(i / 20)
            grp_id = 6
            # groups_biased_against = [0, 1]
            a = UnbiasedAgent(i, grp_id, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        for i in range(700, 800):
            fac_id = int(i / 20)
            grp_id = 7
            # groups_biased_against = [0, 1]
            a = UnbiasedAgent(i, grp_id, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        for i in range(800, 900):
            fac_id = int(i / 20)
            grp_id = 8
            # groups_biased_against = [0, 1]
            a = UnbiasedAgent(i, grp_id, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        for i in range(900, 1000):
            fac_id = int(i / 20)
            grp_id = 9
            # groups_biased_against = [0, 1]
            a = UnbiasedAgent(i, grp_id, self, fac_id)
            self.agent_list.append(a)
            self.group_list[grp_id].append(a)
            fac_agent_lists[fac_id].append(a)

        

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
                [broadcasting_agent] = random.sample(self.agent_list, 1)
                group_id = broadcasting_agent.getGroupId()
                size = len(self.group_list[group_id])
                size = int(size * self.broadcast_percentage)
                broadcast_group = random.sample(self.group_list[group_id], size)
                
                # Group against whom the bias is being broadcasted
                against_group = random.randint(0, (self.num_groups - 1))

                # bias = broadcasting_agent.getBias()
                for i in broadcast_group:
                    i.recieveBroadcast(broadcasting_agent, against_group)


        #Perform normal interaction
        A, B = random.sample(self.agent_list, 2)
        coopA = A.getCoop(B)
        coopB = B.getCoop(A)
        payoffA = payoffCalc(coopA, coopB)
        payoffB = payoffCalc(coopB, coopA)
        A.updateTheta(B, coopB, payoffA)
        B.updateTheta(A, coopA, payoffB)
        
        # if (step_number % logging_granularity == 0):
        #     for i in range(5):
        #         self.payoff_list[i].append(getAveragePayoff(self.group_list[i]))
        #         self.bias_list[i].append(getAverageBias(self.group_list[i]))
        #         self.facalign_list[i].append(getAverageAlign(self.group_list[i]))
