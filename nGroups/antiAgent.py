from .agent import *

class AntiAgent(Agent):
    def __init__(self, unique_id, group, model, fac=None, fMove=None, falign=None):
        super().__init__(unique_id, model, group)
        self.payoff = 0
        coop = random.random()
        self.firstMove = fMove if fMove is not None else coop
        self.biased_coop_level = self.firstMove
        self.prevAct = {}
        self.faction = fac
        
        self.wealth = 1000  # Around 3 times    
        # self.wealth = 230 # 30% of avg observed
        mu = 0.5
        sigma = 0.2
        self.fac_align = falign if falign is not None else random.gauss(mu, sigma)
        self.bias = random.gauss(mu, sigma)
        if (self.fac_align < 0):
            self.fac_align = 0
        elif(self.fac_align > 1):
            self.fac_align = 1

        if (self.bias < 0):
            self.bias = 0
        elif(self.bias > 1):
            self.bias = 1
        
        # Keeping track of difference updates
        self.fac_diff = []
        self.payoff_diff_lst = []

    def getPayoff(self):
        return self.payoff
    
    def getBias(self, other_agent_group):
        if (other_agent_group == self.group_id):
            return self.bias #2
        else:
            return 0
    
    def getFaction(self):
        return self.faction

    def getWealth(self):
        return self.wealth
    
    def getSocialStatus(self):
        return self.current_social_status
    
    def setFaction(self, fact):
        self.faction = fact

    def recieveBroadcast(self, bias_value, against_group):
        return 0

    def isAnti(self):
        return True

    def getGroupsBiasedAgainst(self):
        return [self.group_id]
	
    def getFactionAlignment(self, lalal):
        return 0



    def getOpinion(self, other_agent): 
        if(self.group_id != other_agent.getGroupId()):
            if(other_agent.getId() in self.prevAct):
                unbiased_coop = mean(self.prevAct.get(other_agent.getId()))
            else:
                unbiased_coop = self.firstMove
        
            return unbiased_coop
        
        else:
            if(other_agent.getId() in self.prevAct):
                unbiased_coop = mean(self.prevAct.get(other_agent.getId()))
            else:
                unbiased_coop = self.firstMove
        
            biased_coop = (1 - self.bias) * unbiased_coop
            # self.coop_level = self.prevAct.get(other_agent.getId(), self.firstMove)
            return round(biased_coop, 2)

    def getCoop(self, other_agent):
        self.biased_coop_level = self.getOpinion(other_agent)
        return self.biased_coop_level



    def updateTheta(self, other_agent, coop, payoff_self):
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
        # if (self.faction != None):
        #     self.fac_diff.append(abs(self.bias - self.faction.getFacBias(self)))
        #     if(abs(self.bias - self.faction.getFacBias(self)) < facAlignIncreaseThreshold):
        #         self.fac_align = self.fac_align + facAlignDelta
        #         if(self.fac_align > 1):
        #             self.fac_align = 1
            
        #     elif(abs(self.bias - self.faction.getFacBias(self)) > facAlignDecreaseThreshold):
        #         self.fac_align = self.fac_align - facAlignDelta
        #         if(self.fac_align < 0):
        #             self.fac_align = 0
        
        if(other_agent.getId() in self.prevAct):
            experience_lst = self.prevAct.get(other_agent.getId())
            if(len(experience_lst) < agentMemorySize):
                experience_lst.append(coop)
            else:
                experience_lst.pop(0)
                experience_lst.append(coop)
        else:
            self.prevAct.update({other_agent.getId(): [coop]})

