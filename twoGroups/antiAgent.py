from .agent import *

class AntiAgent(Agent):
    def __init__(self, unique_id, group, model, fac=None, fMove=None, falign=None):
        super().__init__(unique_id, model, group)
        self.payoff = 0
        self.bias = random.choice(model.initial_bias_list)
        model.initial_bias_list.pop(model.initial_bias_list.index(self.bias))
        coop = round(random.random(), 2)
        self.firstMove = fMove if fMove is not None else coop
        self.biased_coop_level = self.firstMove
        self.prevAct = {}
        self.faction = fac
        
        self.wealth = 1000  # Around 3 times    
        # self.wealth = 230 # 30% of avg observed
        
        self.current_social_status = 2
        self.fac_align = falign if falign is not None else random.random()
        
        # Keeping track of difference updates
        self.fac_diff = []
        self.payoff_diff_lst = []

    def getPayoff(self):
        return self.payoff
    
    def getBias(self):
        return self.bias #2
    
    def getFaction(self):
        return self.faction

    def getWealth(self):
        return self.wealth
    
    def getSocialStatus(self):
        return self.current_social_status
    
    def setFaction(self, fact):
        self.faction = fact

    def recieveBroadcast(self, bias_value):
        return 0

    def isAnti(self):
        return True



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

        # WealthUpdation
        
        payoff_diff = round(abs(payoff_self - payoff_other), 2)

        # Determined ten intervals
        if(payoff_diff <= 0.08):
            multiplier = 1
        elif(payoff_diff > 0.08 and payoff_diff <= 0.17):
            multiplier = 2
        elif(payoff_diff > 0.17 and payoff_diff <= 0.28):
            multiplier = 3
        elif(payoff_diff > 0.28 and payoff_diff <= 0.39):
            multiplier = 4
        elif(payoff_diff > 0.39 and payoff_diff <= 0.53):
            multiplier = 5
        elif(payoff_diff > 0.53 and payoff_diff <= 0.69):
            multiplier = 6
        elif(payoff_diff > 0.69 and payoff_diff <= 0.90):
            multiplier = 7
        elif(payoff_diff > 0.90 and payoff_diff <= 1.17):
            multiplier = 8
        elif(payoff_diff > 1.17 and payoff_diff <= 1.61):
            multiplier = 9
        else:
            multiplier = 10

        # if(payoff_diff <= 0.07):
        #     multiplier = 1
        # elif(payoff_diff > 0.07 and payoff_diff <= 0.14):
        #     multiplier = 2
        # elif(payoff_diff > 0.14 and payoff_diff <= 0.22):
        #     multiplier = 3
        # elif(payoff_diff > 0.22 and payoff_diff <= 0.31):
        #     multiplier = 4
        # elif(payoff_diff > 0.31 and payoff_diff <= 0.43):
        #     multiplier = 5
        # elif(payoff_diff > 0.43 and payoff_diff <= 0.57):
        #     multiplier = 6
        # elif(payoff_diff > 0.57 and payoff_diff <= 0.78):
        #     multiplier = 7
        # elif(payoff_diff > 0.78 and payoff_diff <= 1.08):
        #     multiplier = 8
        # elif(payoff_diff > 1.08 and payoff_diff <= 1.59):
        #     multiplier = 9
        # else:
        #     multiplier = 10

        if(payoff_self >= payoff_other):
            self.wealth += (payoff_diff * multiplier)
        else:
            self.wealth -= (payoff_diff * multiplier)


        # Social Status Update
        national_median = 1032
        if(self.wealth < (0.66 * national_median)):
            self.current_social_status = 1
        elif((self.wealth >= (0.66 * national_median)) and (self.wealth <= (2 * national_median))):
            self.current_social_status = 2
        else:
            self.current_social_status = 3
