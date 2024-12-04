import numpy as np
import random

class Play:
    def __init__(self, name):
        self._name = None  
        self._result = { 
            'success': False,
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
        average1 = offense.average_time(self._name)
        average2 = defense.average_time(self._name, 'defteam')
        return (average1+average2)/2
    
    def calculateTimeElapsed2(self, yards):
        return yards*2
    
    def makePlay(self, offense, defense):
        offenseChance = offense.pass_percent(self._name)
        defenseChance = defense.pass_percent(self._name, 'defteam')
        offenseSuccess = random.random(0,1) < offenseChance
        defenseSuccess = random.random(0,1) < defenseChance

        if offenseSuccess and defenseSuccess:
            yards = 0
            time = self.calculateTimeElapsed(self, offense, defense)/2
            chancetoPick()
            self.set_result(yards, time)
        elif offenseSuccess and not defenseSuccess:
            yards = offense.average_yards(self._name)
            time = self.calculateTimeElapsed(self, offense, defense)
            self.set_result(yards, time)
        elif not offenseSuccess and defenseSuccess:
            yards = 0
            time = 10
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        elif not offenseSuccess and not defenseSuccess:
            yards = 0
            time = 10
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        return self._result
    
class PassPlay(Play):
    def __init__(self):
        self._interceptChance = 0
        Play.__init__(self, 'pass_attempt')
    
    def makePlay(self, offense, defense):
        offenseChance = offense.pass_percent(self._name)
        defenseChance = defense.pass_percent(self._name, 'defteam')
        offenseSuccess = random.random(0,1) < offenseChance
        defenseSuccess = random.random(0,1) < defenseChance

        if offenseSuccess and defenseSuccess:
            yards = 0
            time = self.calculateTimeElapsed(self, offense, defense)/2
            #chancetoPick()
            self.set_result(yards, time)
        elif offenseSuccess and not defenseSuccess:
            yards = offense.average_yards(self._name)
            time = self.calculateTimeElapsed(self, offense, defense)
            self.set_result(yards, time)
        elif not offenseSuccess and defenseSuccess:
            yards = 0
            time = 10
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        elif not offenseSuccess and not defenseSuccess:
            yards = 0
            time = 10
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        return self._result

class RushPlay(Play):
    def __init__(self):
        self._sackChance = 0
        Play.__init__(self, 'rush_attempt')

    def makePlay(self, offense, defense):
        offenseChance = offense.play_percent(self._name)
        defenseChance = defense.play_percent(self._name, 'defteam')
        offenseSuccess = random.random(0,1) < offenseChance
        defenseSuccess = random.random(0,1) < defenseChance

        if offenseSuccess and defenseSuccess:
            yards = random_yards(mean, sd)
            time = self.calculateTimeElapsed(self, offense, defense)/2
            self.set_result(yards, time)
        elif offenseSuccess and not defenseSuccess:
            yards = offense.average_yards(self._name)
            time = self.calculateTimeElapsed(self, offense, defense)
            self.set_result(yards, time)
        elif not offenseSuccess and defenseSuccess:
            yards = 0
            time = 10
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        elif not offenseSuccess and not defenseSuccess:
            yards = 0
            time = 10
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        return self._result

class FieldGoal(Play):
    def __init__(self):
        self._success = False
        Play.__init__(self, 'field goal')

    def getSuccess(self):
        return self._success

    def makePlay(self, offense, defense):
        if random(0, 1) <= offense.fieldGoalChance():
            self._success = True
        self.set_result(0, 10)
        return self._result 

class KickOff(Play):
    def __init__(self):
        Play.__init__(self, 'kick off')

    def makePlay(self, offense, defense):
        yards = offense.average_return_yards(self)
        time = 5 + self.calculateTimeElapsed2(yards)
        self.set_result(yards, time)
        return self._result 