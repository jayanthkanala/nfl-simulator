import numpy as np
import random

class Play:
    def __init__(self, name):
        self._name = None  
        self._successChance = 0
        self._yardRange = [0, 0]
        self._result = { 
            'success': False,
            'yards': 0,
            'timeElapsed':0}
        
    
    # Getter and Setter for name
    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    # Getter and Setter for offenseChance
    def get_success_chance(self):
        return self._successChance

    def set_success_chance(self, value):
        self._successChance = value

    # Getter and Setter for defenseChance
    def get_yardRange(self):
        return self._yardRange

    def set_yardRange(self, value):
        self._yardRange = value

    # Getter and Setter for the entire result dictionary
    def get_result(self):
        return self._result

    def set_result(self, success=False,yards=0, timeElapsed=0):
        self._result = { 
            'success': success,
            'yards': yards,
            'timeElapsed':timeElapsed}

    # Individual Getters and Setters for result keys
    def get_yards(self):
        return self._result['yards']

    def set_yards(self, value):
        self._result['yards'] = value

    def get_time_elapsed(self):
        return self._result['timeElapsed']

    def set_time_elapsed(self, value):
        self._result['timeElapsed'] = value

    def makePlay(self):
        #Checks if play is a failure
        if random.random(0, 1) > self._successChance: 
            self.set_result(False, 0, 10) #Use a default of 10 seconds for failed play for now
        #If it didn't fail, it must have succeeded
        else:
            yards = random.random(self._yardRange[0], self._yardRange[1])
            time = somewaytocalculateTime()
            self.set_result(True, yards, 5+time)
        return self._result



class PassPlay(Play):
    def __init__(self):
        self._interceptChance = 0
        Play.__init__(self, 'pass')

class RushPlay(Play):
    def __init__(self):
        self._sackChance = 0
        Play.__init__(self, 'rush')

class FieldGoal(Play):
    def __init__(self):
        Play.__init__(self, 'field goal')

class KickOff(Play):
    def __init__(self):
        Play.__init__(self, 'kick off')