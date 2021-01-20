from .agent import *
import statistics as s

class BiasedAgent(Agent):
    def __init__(self, unique_id, group, groups_biased_against, model, fac, fMove=None, falign=None):
        super().__init__(unique_id, model, group)
        self.payoff = 0
        self.payoff_list = []
        self.bias_list = []
        self.groups_biased_against = groups_biased_against
        coop = round(random.random(), 2)
        self.firstMove = fMove if fMove is not None else coop
        self.biased_coop_level = self.firstMove
        self.prevAct = {}
        self.faction = fac
        self.fac_align = []
        mu = 0.5
        sigma = 0.2
        temp = []
        temp2 = []
        for i in range(model.num_groups):
            temp.append(0)
            temp2.append(0)
        for j in self.groups_biased_against:
                temp[j] = (random.gauss(mu, sigma))
                temp2[j] = (random.gauss(mu, sigma))
        for k in temp:
            if (k < 0):
                k = k * (-1)
            elif (k > 1):
                k = 1

        for k in temp2:
            if (k < 0):
                k = k * (-1)
            elif (k > 1):
                k = 1

        # Initializing Bias for all Groups and FacAlign
        for i in range(model.num_groups):
            self.fac_align.append(temp2[i])
            if(i in self.groups_biased_against):
                self.bias_list.append(temp[i])
            else:
                self.bias_list.append(None)


    def getPayoff(self):
        return self.payoff
    
    def getBias(self, group_number):
        return self.bias_list[group_number]  # 2
    
    def getFactionAlignment(self, group_number):
        return self.fac_align[group_number]

    def getGroupsBiasedAgainst(self):
        return self.groups_biased_against
    
    def getFaction(self):
        return self.faction
    
    def setFaction(self, fact):
        self.faction = fact

    def recieveBroadcast(self, broadcasting_agent, against_group):

        broadcasted_bias = broadcasting_agent.getBias(against_group)
        if(broadcasted_bias != None):
            if(self.bias_list[against_group] != None):
                if (self.bias_list[against_group] < broadcasted_bias):
                    delta = broadcasted_bias - self.bias_list[against_group]
                    if (self.bias_list[against_group] <= .25):
                        self.bias_list[against_group] += delta * 0.10
                    elif (self.bias_list[against_group] <= .5):
                        self.bias_list[against_group] += delta * 0.07
                    elif (self.bias_list[against_group] <= .75):
                        self.bias_list[against_group] += delta * 0.04
                    else:
                        self.bias_list[against_group] += delta * 0.02
                    # self.bias += 0.05


    def getOpinion(self, other_agent):
        if(self.group_id == other_agent.getGroupId()):
            if(other_agent.getId() in self.prevAct):
                unbiased_coop = mean(self.prevAct.get(other_agent.getId()))
            else:
                unbiased_coop = self.firstMove

            return round(unbiased_coop, 2)

        else:
            if(other_agent.getId() in self.prevAct):
                unbiased_coop = mean(self.prevAct.get(other_agent.getId()))
            else:
                unbiased_coop = self.firstMove

            bias_against_group = self.bias_list[other_agent.getGroupId()]

            if(bias_against_group != None):
                biased_coop = (1 - bias_against_group) * unbiased_coop
                # self.coop_level = self.prevAct.get(other_agent.getId(), self.firstMove)
                return round(biased_coop, 2)
            else:
                return round(unbiased_coop, 2)

    def getCoop(self, other_agent):
        if (self.faction == None):
            self.biased_coop_level = self.getOpinion(other_agent)
            return self.biased_coop_level
        # agent collects both his own opinion, and his
        # faction's opinion of this other agent
        biased_opinion = self.getOpinion(other_agent)
        fac_opinion = self.faction.getFacCoop(other_agent, self)

        # Variable that denotes the maximum possible fraction given to the faction opinion
        # opinion_weight = 0.5

        # self.biased_coop_level = (opinion_weight * fac_opinion * self.fac_align) + ((1-opinion_weight) * biased_opinion)
        if(fac_opinion != None):
            self.biased_coop_level = (self.fac_align[other_agent.getGroupId(
            )] * fac_opinion) + ((1 - self.fac_align[other_agent.getGroupId()]) * biased_opinion)
            return self.biased_coop_level
        else:
            return biased_opinion

    def updateTheta(self, other_agent, coop, payoff):
        self.payoff += payoff
        self.payoff_list.append(payoff)
        self.interactions.append(payoff)
        other_agent_id = other_agent.getId()
        other_agent_group = other_agent.getGroupId()

        agentMemorySize = 10

        maxPayoff = 5
        # minPayoff = 0

        biasIncreaseThreshold = 0.40
        biasDecreaseThreshold = 0.30
        biasDelta = 0.005

        facAlignIncreaseThreshold, facAlignDecreaseThreshold = facalignCalc(s.mean(self.fac_align))
        facAlignDelta = 0.005

        # BiasUpdation
        if(self.bias_list[other_agent_group] != None):
            if(payoff >= (biasIncreaseThreshold * maxPayoff)):
                self.bias_list[other_agent_group] = self.bias_list[other_agent_group] + biasDelta
                if(self.bias_list[other_agent_group] > 1):
                    self.bias_list[other_agent_group] = 1

            if(payoff < (biasDecreaseThreshold * maxPayoff)):
                self.bias_list[other_agent_group] = self.bias_list[other_agent_group] - biasDelta
                if(self.bias_list[other_agent_group] < 0):
                    self.bias_list[other_agent_group] = 0

        # FactionAlignmentUpdation
        if(self.bias_list[other_agent_group] != None):
            if(self.faction.getFacBias(self, other_agent_group) != None):
                if(abs(self.bias_list[other_agent_group] - self.faction.getFacBias(self, other_agent_group)) < facAlignIncreaseThreshold):
                    self.fac_align[other_agent_group] = self.fac_align[other_agent_group] + facAlignDelta
                    if(self.fac_align[other_agent_group] > 1):
                        self.fac_align[other_agent_group] = 1

                if(abs(self.bias_list[other_agent_group] - self.faction.getFacBias(self, other_agent_group)) > facAlignDecreaseThreshold):
                    self.fac_align[other_agent_group] = self.fac_align[other_agent_group] - facAlignDelta
                    if(self.fac_align[other_agent_group] < 0):
                        self.fac_align[other_agent_group] = 0
            else:
                if(self.faction.getFacCoop(other_agent, self) != None):
                    if(abs(self.getOpinion(other_agent) - self.faction.getFacCoop(other_agent, self)) < facAlignIncreaseThreshold):
                        self.fac_align[other_agent_group] = self.fac_align[other_agent_group] + facAlignDelta
                        if(self.fac_align[other_agent_group] > 1):
                            self.fac_align[other_agent_group] = 1

                    if(abs(self.getOpinion(other_agent) - self.faction.getFacCoop(other_agent, self)) > facAlignDecreaseThreshold):
                        self.fac_align[other_agent_group] = self.fac_align[other_agent_group] - facAlignDelta
                        if(self.fac_align[other_agent_group] < 0):
                            self.fac_align[other_agent_group] = 0

        # else:
        #     if(self.faction.getFacCoop(other_agent, self) != None):
        #         if(abs(self.getOpinion(other_agent) - self.faction.getFacCoop(other_agent, self)) < facAlignIncreaseThreshold):
        #             self.fac_align[other_agent_group] = self.fac_align[other_agent_group] + facAlignDelta
        #             if(self.fac_align[other_agent_group] > 1):
        #                 self.fac_align[other_agent_group] = 1

        #         if(abs(self.getOpinion(other_agent) - self.faction.getFacCoop(other_agent, self)) > facAlignDecreaseThreshold):
        #             self.fac_align[other_agent_group] = self.fac_align[other_agent_group] - facAlignDelta
        #             if(self.fac_align[other_agent_group] < 0):
        #                     self.fac_align[other_agent_group] = 0

        if(other_agent_id in self.prevAct):
            experience_lst = self.prevAct.get(other_agent_id)
            if(len(experience_lst) < agentMemorySize):
                experience_lst.append(coop)
            else:
                experience_lst.pop(0)
                experience_lst.append(coop)
        else:
            self.prevAct.update({other_agent_id: [coop]})

