import numpy as np
import random
from scipy.stats import skewnorm

class Play:
    def __init__(self, name):
        self._name = None  
        self._result = { 
            'yards': 0,
            'timeElapsed':0}
    
    # Getter and Setter for name
    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    # Getter and Setter for the entire result dictionary
    def get_result(self):
        return self._result

    def set_result(self,yards=0, timeElapsed=0):
        self._result = { 
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

    def calculateTimeElapsed(self, offense, defense):
        #Uses team class functions to find average time for offense and defense team
        average1 = offense.average_time(self._name, 'posteam')
        average2 = defense.average_time(self._name, 'defteam')
        return (average1+average2)/2
    
    def calculateTimeElapsed2(self, yards):
        return yards*2
    
    def random_yards(mean, sd, yards, skewness):
        while True:
            rand_yards = skewnorm.rvs(skewness, loc=mean, scale=sd, size=1)
            if (yards - 100) <= rand_yards <= yards:
                break
        return rand_yards

        mean, sd = average_off_def(offense = "BUF", defense = "KC", play_type = "fumble")[0]
        
        buf_yards = random_yards(mean, sd, yards = 75, skewness = 0) #75 is a placeholder
    
    
class PassPlay(Play):
    def __init__(self):
        self._interceptChance = 0
        Play.__init__(self, 'pass_attempt')
    
    def makePlay(self, offense, defense):
        offenseChance = offense.average_off_def(offense,defense, 'complete_pass', 'completion_percentage')       
        offenseSuccess = random.uniform(0.00,1.00) < offenseChance
        
        if offenseSuccess:
            self._name = 'complete_pass'
            averageYards, stdYards = offense.average_off_def(offense, defense, 'average_yards')
            yards = offense.random_yards(averageYards, stdYards, 75, 0)
            time = self.calculateTimeElapsed(self, offense, defense)
            self.set_result(yards, 10+time)        
        elif not offenseSuccess:
            yards = 0
            time = 10
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
    
        return self._result

class RushPlay(Play):
    def __init__(self):
        self._sackChance = 0
        Play.__init__(self, 'rush_attempt')

    def makePlay(self, offense, defense):
        mean, sd = offense.average_off_def(offense, defense, self._name, 'average_yards')
        yards = offense.random_yards(mean, sd, 75, 0)
        time = self.calculateTimeElapsed(self, offense, defense)
        self.set_result(yards, time)
        return self._result

class FieldGoal(Play):
    def __init__(self):
        Play.__init__(self, 'field goal')
        self._result = { 
            'success': False,
            'yards': 0,
            'timeElapsed':0}

    def getSuccess(self):
        return self._result['success']

    def makePlay(self, offense, defense):
        #70 30 field goal chance for now
        if random.uniform(0.00, 1.00) <= 0.7: #offense.fieldGoalChance()
            self._result['success'] = True
        self.set_result(0, 10)
        return self._result 

class KickOff(Play):
    def __init__(self):
        Play.__init__(self, 'kick_off')

    def makePlay(self, offense, defense):
        yards = 10 #offense.average_return_yards(self)
        time = 5 + self.calculateTimeElapsed2(yards)
        self.set_result(yards, time)
        return self._result 