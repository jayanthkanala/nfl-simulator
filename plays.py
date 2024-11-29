import numpy as np

class Play:
    def __init__(self, name):
        self._name = None  
        self._offenseChance = 0
        self._defenseChance = 0
        self._result = { 
            'score': 0,
            'yards': 0,
            'timeElapsed':0}
        
    
    def makePlay(self, offenseChance, defenseChance):
        matrix = [[offenseChance*defenseChance, (1-offenseChance)*defenseChance], 
                  [(1-defenseChance)*offenseChance, (1-defenseChance)*(1-offenseChance)]]

    # Getter and Setter for name
    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    # Getter and Setter for offenseChance
    def get_offense_chance(self):
        return self._offenseChance

    def set_offense_chance(self, value):
        self._offenseChance = value

    # Getter and Setter for defenseChance
    def get_defense_chance(self):
        return self._defenseChance

    def set_defense_chance(self, value):
        self._defenseChance = value

    # Getter and Setter for the entire result dictionary
    def get_result(self):
        return self._result

    def set_result(self, score=0 , yards=0, timeElapsed=0):
        self._result = { 
            'score': score,
            'yards': yards,
            'timeElapsed':timeElapsed}

    # Individual Getters and Setters for result keys
    def get__score(self):
        return self._result['score']

    def set_score(self, value):
        self._result['score'] = value

    def get_yards(self):
        return self._result['yards']

    def set_yards(self, value):
        self._result['yards'] = value

    def get_time_elapsed(self):
        return self._result['timeElapsed']

    def set_time_elapsed(self, value):
        self._result['timeElapsed'] = value

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