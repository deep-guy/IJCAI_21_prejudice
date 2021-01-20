from .baseClass import *


class Agent():
    def __init__(self, uid, model, group):
        self.unique_id = uid
        self.model = model
        self.group_id = group
        self.interactions = []

    def getId(self):
        return self.unique_id

    def getModel(self):
        return self.model #1

    def getGroupId(self):
        return self.group_id
    
    def getBias(self):
        return 0

    def recieveBroadcast(self, bias_value):
        return

    def getAveragePayoff(self):
        if (len(self.interactions) != 0):
            return mean(self.interactions)
        else:
            return 0

    def isAnti(self):
        return False




