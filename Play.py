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

    def calculateTimeElapsed(self, playtype, offense):
        #Uses team class functions to find average time for offense and defense team
        mean, sd, skew = offense.average_time(playtype)
        return self.random_yards_time(mean, sd, skew)


    def calculateTimeElapsed2(self, yards):
        return yards*2

    def random_yards(self, mean, sd, yards, skewness):
        while True:
            rand_yards = skewnorm.rvs(skewness, loc=mean, scale=sd, size=1)
            if (yards - 100) <= rand_yards <= yards:
                break
        return rand_yards

        #mean, sd = average_off_def(offense = "BUF", defense = "KC", play_type = "fumble")[0]

        #buf_yards = random_yards(mean, sd, yards = 75, skewness = 0) #75 is a placeholder
      
    def random_yards_time(self, mean, sd, skewness):
        return skewnorm.rvs(skewness, loc=mean, scale=sd, size=1)[0]


class PassPlay(Play):
    def __init__(self):
        self._interceptChance = 0
        Play.__init__(self, 'pass_attempt')

    def makePlay(self, offense, defense):
        offenseChance = offense.average_off_def(offense,defense, 'complete_pass', 'completion_percentage')
        offenseSuccess = random.uniform(0.00,1.00) <= offenseChance

        if offenseSuccess:
            self._name = 'complete_pass'
            averageYards, stdYards, skew = offense.average_off_def(offense, defense, 'complete_pass', 'average_yards')
            yards = self.random_yards_time(averageYards, stdYards, skew)
            time = self.calculateTimeElapsed('complete_pass', offense)
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
        mean, sd, skew = offense.average_off_def(offense, defense, 'rush_attempt', 'average_yards')
        yards = self.random_yards_time(mean, sd, skew)
        time = self.calculateTimeElapsed('rush_attempt', offense)
        self.set_result(yards, time)
        return self._result

class FieldGoal(Play):
    def __init__(self):
        self._name = 'field_goal'
        self._result = {
            'success': False,
            'yards': 0,
            'timeElapsed':0}


    def getSuccess(self):
        return self._result['success']
    
    def set_result(self,success = False, yards=0, timeElapsed=0):
        self._result = {
            'success': success,
            'yards': yards,
            'timeElapsed':timeElapsed}

    def makePlay(self, offense, defense):
        #70 30 field goal chance for now
        if random.uniform(0.00, 1.00) <= 0.7: #offense.fieldGoalChance()
            self.set_result(True, 0, 10)
        else:
            self.set_result(False, 0, 10)
        return self._result

class KickOff(Play):
    def __init__(self):
        Play.__init__(self, 'kick_off')

    def makePlay(self, offense, defense):
        yards = 10 #offense.average_return_yards(self)
        time = 5 + self.calculateTimeElapsed2(yards)
        self.set_result(yards, time)
        return self._result