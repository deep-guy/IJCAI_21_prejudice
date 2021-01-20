from .baseClass import *

class Faction():
    def __init__(self, id, list_of_agents = []):
        self.fac_id = id
        self.agent_list = list_of_agents
        for i in self.agent_list:
            i.setFaction(self)

    def getId(self):
        return self.fac_id #3
    
    def addAgent(self, agent):
        self.agent_list.append(agent)
    
    # Takes 2 params: agent and req agent
    # agent is the guy whose opinion you want to fetch
    # req agent is the guy who asked for it. So we
    # wont count his opinion twice
    def getFacCoop(self, agent, requesting_agent):
        avg = 0
        for i in self.agent_list:
            if (i.getId() != requesting_agent.getId()):
                avg += i.getOpinion(agent)
        
        avg = avg / (len(self.agent_list) - 1)
        return avg

    # Use this method to obtain the bias, for updating the faction alignment variable
    def getFacBias(self, requesting_agent):
        avg = 0
        if (requesting_agent == None):
            for i in self.agent_list:
                avg += i.getBias()
            return avg/len(self.agent_list)

        for i in self.agent_list:
            if (i.getId() != requesting_agent.getId()):
                avg += i.getBias()
        avg = avg / (len(self.agent_list) - 1)
        return avg

    # @jit(nopython=True)
    def getNetPayoff(self):
        net = 0
        for i in self.agent_list:
            net += i.getPayoff()
        return net
