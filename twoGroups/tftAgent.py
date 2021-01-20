from .agent import *


class TFTAgent(Agent):
    """ An agent that uses the Tit for Tat strategy """
    def __init__(self, unique_id, group, model, fac, fMove=None, susp=False, falign=None):
        super().__init__(unique_id, model, group)
        self.payoff = 0
        self.susp = susp
        coop = 0
        if (susp == False):
            coop = random.random()
        self.firstMove = fMove if fMove is not None else coop
        self.prevAct = {}
        self.coop_level = self.firstMove
        self.faction = fac
        self.fac_align = falign if falign is not None else random.random()

    def getId(self):
        return self.unique_id
    
    def getPayoff(self):
        return self.payoff

    # Set my cooperation level to the quantity that the other agent had in
    # our last cooperation. If no records exist, set it to some random value
    def getOpinion(self, other_agent):
        self.coop_level = self.prevAct.get(other_agent.getId(), self.firstMove)
        return self.coop_level

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
        self.biased_coop_level = (fac_opinion * self.fac_align) + ((1-self.fac_align) * biased_opinion)
        return self.biased_coop_level

    def update(self, other_agent, coop, payoff):
        self.payoff += payoff
        self.prevAct.update({other_agent.getId() : coop})
