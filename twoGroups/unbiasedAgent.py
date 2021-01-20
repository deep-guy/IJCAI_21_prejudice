from .agent import *

class UnbiasedAgent(Agent):
    def __init__(self, unique_id, group, model, fac=None, fMove=None, falign=None):
        super().__init__(unique_id, model, group)
        self.payoff = 0
        coop = random.random()
        self.firstMove = fMove if fMove is not None else coop
        self.coop_level = self.firstMove
        self.prevAct = {}
        self.faction = fac
        self.fac_align = falign if falign is not None else random.gauss(0.5, 0.2)
        if (self.fac_align > 1):
            self.fac_align = 1
        elif(self.fac_align < 0):
            self.fac_align = 0
        # self.interactions = []


        self.current_social_status = 2

    def getPayoff(self):
        return self.payoff
    
    def getBias(self):
        return 0
    
    def getFaction(self):
        return self.faction


    def getSocialStatus(self):
        return self.current_social_status
    
    def setFaction(self, fact):
        self.faction = fact

    def recieveBroadcast(self, bias_value):
        # Do nothing on recieving broadcast
        return



    def getOpinion(self, other_agent): 
        if(other_agent.getId() in self.prevAct):
            unbiased_coop = mean(self.prevAct.get(other_agent.getId()))
        else:
            unbiased_coop = self.firstMove
    
        return unbiased_coop
        

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

        # self.biased_coop_level = (opinion_weight * fac_opinion * self.fac_align) + ((1-opinion_weight) * biased_opinion)
        self.coop_level = (self.fac_align * fac_opinion) + ((1 - self.fac_align) * unbiased_opinion)
        return self.coop_level


    def update(self, other_agent, coop, payoff_self, payoff_other):
        self.payoff += payoff_self
        self.interactions.append(payoff_self)

        agentMemorySize = 10

        maxPayoff = 5
        # minPayoff = 0

        # facAlignIncreaseThreshold = 0.5
        # facAlignDecreaseThreshold = 0.2
        # facAlignDelta = 0.005
                
        # # FactionAlignmentUpdation
        # if (self.faction != None):
        #     if(abs(self.getOpinion(other_agent) - self.faction.getFacCoop(other_agent, self)) < facAlignIncreaseThreshold):
        #         self.fac_align = self.fac_align - facAlignDelta
        #         if(self.fac_align < 0):
        #             self.fac_align = 0
            
        #     elif(abs(self.getOpinion(other_agent) - self.faction.getFacCoop(other_agent, self)) > facAlignDecreaseThreshold):
        #         self.fac_align = self.fac_align + facAlignDelta
        #         if(self.fac_align > 1):
        #             self.fac_align = 1
        
        if(other_agent.getId() in self.prevAct):
            experience_lst = self.prevAct.get(other_agent.getId())
            if(len(experience_lst) < agentMemorySize):
                experience_lst.append(coop)
            else:
                experience_lst.pop(0)
                experience_lst.append(coop)
        else:
            self.prevAct.update({other_agent.getId(): [coop]})
