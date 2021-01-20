from .agent import *

class BiasedAgent(Agent):
    def __init__(self, unique_id, group, model, fac=None, fMove=None, falign=None):
        super().__init__(unique_id, model, group)
        self.payoff = 0
        # self.bias = random.choice(model.initial_bias_list)
        # model.initial_bias_list.pop(model.initial_bias_list.index(self.bias))
        self.bias = random.gauss(0.5, 0.2)
        if (self.bias > 1):
            self.bias = 1
        elif(self.bias < 0):
            self.bias = 0
        coop = round(random.random(), 2)
        self.firstMove = fMove if fMove is not None else coop
        self.biased_coop_level = self.firstMove
        self.prevAct = {}
        self.faction = fac
        
        self.current_social_status = 2
        self.fac_align = falign if falign is not None else random.gauss(0.5, 0.2)
        if (self.fac_align > 1):
            self.fac_align = 1
        elif(self.fac_align < 0):
            self.fac_align = 0
        
        # Keeping track of difference updates
        self.fac_diff = []
        self.payoff_diff_lst = []

    def getPayoff(self):
        return self.payoff
    
    def getBias(self):
        return self.bias #2
    
    def getFaction(self):
        return self.faction

    
    def getSocialStatus(self):
        return self.current_social_status
    
    def setFaction(self, fact):
        self.faction = fact

    def recieveBroadcast(self, bias_value):
        if (self.bias < bias_value):
            delta = bias_value - self.bias
            if (self.bias <= 0.25):
                self.bias += delta * 0.10
            elif (self.bias <= 0.5):
                self.bias += delta * 0.07
            elif (self.bias <= 0.75):
                self.bias += delta * 0.04
            else:
                self.bias += delta * 0.02



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
        
            biased_coop = (1 - self.bias) * unbiased_coop
            # self.coop_level = self.prevAct.get(other_agent.getId(), self.firstMove)
            return round(biased_coop, 2)

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
        self.biased_coop_level = (self.fac_align * fac_opinion) + ((1 - self.fac_align) * biased_opinion)
        return self.biased_coop_level



    def update(self, other_agent, coop, payoff_self, payoff_other):
        self.payoff += payoff_self
        self.interactions.append(payoff_self)

        agentMemorySize = 10

        maxPayoff = 5
        # minPayoff = 0
        
        biasIncreaseThreshold = 0.45
        biasDecreaseThreshold = 0.35
        biasDelta = 0.005

        facAlignIncreaseThreshold, facAlignDecreaseThreshold = facalignCalc(self.fac_align)
        facAlignDelta = 0.005
        
        # BiasUpdation
        self.payoff_diff_lst.append(payoff_self)
        if(payoff_self >= (biasIncreaseThreshold * maxPayoff)):
            self.bias = self.bias + biasDelta
            if(self.bias > 1):
                self.bias = 1

        if(payoff_self < (biasDecreaseThreshold * maxPayoff)):
            self.bias = self.bias - biasDelta
            if(self.bias < 0):
                self.bias = 0
                
        # FactionAlignmentUpdation
        if (self.faction != None):
            self.fac_diff.append(abs(self.bias - self.faction.getFacBias(self)))
            if(abs(self.bias - self.faction.getFacBias(self)) < facAlignIncreaseThreshold):
                self.fac_align = self.fac_align + facAlignDelta
                if(self.fac_align > 1):
                    self.fac_align = 1
            
            elif(abs(self.bias - self.faction.getFacBias(self)) > facAlignDecreaseThreshold):
                self.fac_align = self.fac_align - facAlignDelta
                if(self.fac_align < 0):
                    self.fac_align = 0
        
        if(other_agent.getId() in self.prevAct):
            experience_lst = self.prevAct.get(other_agent.getId())
            if(len(experience_lst) < agentMemorySize):
                experience_lst.append(coop)
            else:
                experience_lst.pop(0)
                experience_lst.append(coop)
        else:
            self.prevAct.update({other_agent.getId(): [coop]})
