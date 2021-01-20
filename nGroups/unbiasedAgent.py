from .agent import *
import statistics as s

class UnbiasedAgent(Agent):
    def __init__(self, unique_id, group, model, fac, fMove=None, falign=None):
        super().__init__(unique_id, model, group)
        self.payoff = 0
        coop = round(random.random(), 2)
        self.firstMove = fMove if fMove is not None else coop
        self.coop_level = self.firstMove
        self.prevAct = {}
        self.faction = fac
        self.fac_align = []
        self.bias_list = []
        mu = 0.5
        sigma = 0.2
        temp = []
        for i in range(model.num_groups):
            temp.append(0)
        # for j in self.groups_biased_against:
        #         temp[j] = (random.gauss(mu, sigma))
        for k in temp:
            if (k < 0):
                k = k * (-1)
            elif (k > 1):
                k = 1

        # Initializing Bias for all Groups and FacAlign
        for i in range(model.num_groups):
            self.fac_align.append(temp[i])

    def getPayoff(self):
        return self.payoff
    
    def getBias(self, group_number):
        return 0

    def getGroupsBiasedAgainst(self):
        return []
    
    def getFaction(self):
        return self.faction

    def getFactionAlignment(self, group_number):
        return self.fac_align[group_number]
    
    def setFaction(self, fact):
        self.faction = fact

    def recieveBroadcast(self, broadcasting_agent, against_group):
        return


    def getOpinion(self, other_agent):
        if(other_agent.getId() in self.prevAct):
            unbiased_coop = mean(self.prevAct.get(other_agent.getId()))
        else:
            unbiased_coop = self.firstMove

        return round(unbiased_coop, 2)


    def getCoop(self, other_agent):
        if (self.faction == None):
            self.coop_level = self.getOpinion(other_agent)
            return self.coop_level
        # agent collects both his own opinion, and his
        # faction's opinion of this other agent
        unbiased_opinion = self.getOpinion(other_agent)
        fac_opinion = self.faction.getFacCoop(other_agent, self)

        # Variable that denotes the maximum possible fraction given to the faction opinion
        # opinion_weight = 0.5

        # self.coop_level = (opinion_weight * fac_opinion * self.fac_align) + ((1-opinion_weight) * biased_opinion)
        if(fac_opinion != None):
            self.coop_level = (self.fac_align[other_agent.getGroupId(
            )] * fac_opinion) + ((1 - self.fac_align[other_agent.getGroupId()]) * unbiased_opinion)
            return self.coop_level
        else:
            return unbiased_opinion

    def updateTheta(self, other_agent, coop, payoff):
        self.payoff += payoff
        self.interactions.append(payoff)
        other_agent_id = other_agent.getId()
        other_agent_group = other_agent.getGroupId()

        agentMemorySize = 10

        maxPayoff = 5
        # minPayoff = 0

        # facAlignIncreaseThreshold, facAlignDecreaseThreshold = facalignCalc(s.mean(self.fac_align))
        # facAlignDelta = 0.005


        # # FactionAlignmentUpdation
        # if (self.faction != None):
        #     if(abs(self.getOpinion(other_agent) - self.faction.getFacCoop(other_agent, self)) < facAlignIncreaseThreshold):
        #         self.fac_align[other_agent_group] = self.fac_align[other_agent_group] + facAlignDelta
        #         if(self.fac_align[other_agent_group] > 1):
        #             self.fac_align[other_agent_group] = 1
            
        #     if(abs(self.getOpinion(other_agent) - self.faction.getFacCoop(other_agent, self)) > facAlignDecreaseThreshold):
        #         self.fac_align[other_agent_group] = self.fac_align[other_agent_group] - facAlignDelta
        #         if(self.fac_align[other_agent_group] < 0):
        #             self.fac_align[other_agent_group] = 0
        
        if(other_agent.getId() in self.prevAct):
            experience_lst = self.prevAct.get(other_agent.getId())
            if(len(experience_lst) < agentMemorySize):
                experience_lst.append(coop)
            else:
                experience_lst.pop(0)
                experience_lst.append(coop)
        else:
            self.prevAct.update({other_agent.getId(): [coop]})
