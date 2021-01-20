from .agent import *

class Faction():
    def __init__(self, id, list_of_agents = [], biased_mem_thersh=0.3):
        self.fac_id = id
        self.agent_list = list_of_agents
        self.num_members = len(self.agent_list)
        self.biased_members_threshold = biased_mem_thersh
        for i in self.agent_list:
            i.setFaction(self)

    def getId(self):
        return self.fac_id #3
    
    def addAgent(self, agent):
        self.agent_list.append(agent)
    
    def getFacCoop(self, agent, requesting_agent):
        avg = 0
        for i in self.agent_list:
            if (i.getId() != requesting_agent.getId()):
                avg += i.getOpinion(agent)
        
        avg = avg / (len(self.agent_list) - 1)
        return avg

    # Use this method to obtain the bias, for updating the faction alignment variable
    def getFacBias(self, requesting_agent, other_agent_group):
        avg = 0
        count = 0
        size = int(self.num_members * self.biased_members_threshold)

        if (requesting_agent == None):
            for i in self.agent_list:
                if(i.getBias(other_agent_group) != None):
                    avg += i.getBias(other_agent_group)
                    count += 1

            if(count >= size):
                return avg/count
            else:
                None

        for i in self.agent_list:
            if (i.getId() != requesting_agent.getId()):
                if(i.getBias(other_agent_group) != None):
                    avg += i.getBias(other_agent_group)
                    count += 1
        avg = avg / count

        if(count >= size):
            return avg
        else:
            None

    # @jit(nopython=True)
    def getNetPayoff(self):
        net = 0
        for i in self.agent_list:
            net += i.getPayoff()
        return net