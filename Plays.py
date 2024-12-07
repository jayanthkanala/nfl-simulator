import numpy as np
import random
from scipy.stats import skewnorm

class Play:
    def __init__(self, name):
        self._name = name
        self._result = {
            'yards': 0,
            'timeElapsed':0}
        self._gameResult = {
            'homeScore': 0,
            'awayScore': 0,
            'yards': 0,
            'timeElapsed': 0,
            'down': 1,
            'quarter': 1,
            'Probability': 0,
            'penalty': False,
            'TouchDown': False,
            'FieldGoal': False,
            'TurnOver': False,
        }
    def get_success(self):
        return False

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

    def set_game_results(self, homeScore, awayScore, yards, timeElapsed, down, quarter, Probability, penalty, TouchDown, FieldGoal, TurnOver):
        """
        Sets all values in the _gameResult dictionary.
        """
        self._gameResult['homeScore'] = homeScore
        self._gameResult['awayScore'] = awayScore
        self._gameResult['yards'] = yards
        self._gameResult['timeElapsed'] = timeElapsed
        self._gameResult['down'] = down
        self._gameResult['quarter'] = quarter
        self._gameResult['Probability'] = Probability
        self._gameResult['penalty'] = penalty
        self._gameResult['TouchDown'] = TouchDown
        self._gameResult['FieldGoal'] = FieldGoal
        self._gameResult['TurnOver'] = TurnOver

    def get_game_results(self):
        return self._gameResult

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
        return self.random_yards_time(mean, sd, skew)/2

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

        sackChance = 0.10
        sackSuccess = random.uniform(0.00,1.00) <= sackChance

        #interceptChance = 0.05
        #interceptSuccess = random.uniform(0.00,1.00) <= interceptChance


        if sackSuccess:
            self._name = 'sack'
            sack_mean, sack_std, sack_skew = defense.average_off_def(offense, defense, play_type = "sack", funcname = 'average_yards')
            yards = self.random_yards_time(sack_mean, sack_std, sack_skew)
            time = self.calculateTimeElapsed('sack', offense)
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        #elif interceptSuccess:
            #self._name = 'interception'
            #int_mean, int_std, int_skew = defense.average_off_def(offense, defense, play_type = "interception", funcname = 'average_yards')
            #yards = self.random_yards_time(int_mean, int_std, int_skew)
            #time = self.calculateTimeElapsed('interception', offense)
            #self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        elif offenseSuccess:
            self._name = 'complete_pass'
            averageYards, stdYards, skew = offense.average_off_def(offense, defense, 'complete_pass', 'average_yards')
            yards = self.random_yards_time(averageYards, stdYards, skew)
            time = self.calculateTimeElapsed('complete_pass', offense)
            self.set_result(yards, 10+time)
        else:
            yards = 0
            time = round(random.gauss(10, 2), 2)
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now

        return self._result

class RushPlay(Play):
    def __init__(self):
        self._sackChance = 0
        Play.__init__(self, 'rush_attempt')

    def makePlay(self, offense, defense):
        sackChance = 0.10
        sackSuccess = random.uniform(0.00,1.00) <= sackChance
        if sackSuccess:
            self._name = 'sack'
            sack_mean, sack_std, sack_skew = defense.average_off_def(offense, defense, play_type = "sack", funcname = 'average_yards')
            yards = self.random_yards_time(sack_mean, sack_std, sack_skew)
            time = self.calculateTimeElapsed('sack', offense)
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now

        else:
            mean, sd, skew = offense.average_off_def(offense, defense, 'rush_attempt', 'average_yards')
            yards = self.random_yards_time(mean, sd, skew)
            if yards > 0:
              self._name = 'rush'
            time = self.calculateTimeElapsed('rush_attempt', offense)
            self.set_result(yards, time)
        return self._result

class FieldGoal(Play):
    def __init__(self):
        Play.__init__(self, 'field_goal')
        self._result['success'] = False


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
            self.set_result(True, 0, 5)
        else:
            self.set_result(False, 0, 5)
        return self._result

class KickOff(Play):
    def __init__(self):
        Play.__init__(self, 'kick_off')

    def makePlay(self, offense, defense):
        yards = 10 #offense.average_return_yards(self)
        time = 5 + self.calculateTimeElapsed2(yards)
        self.set_result(yards, time)
        return self._result

class Penalty(Play):
    def __init__(self):
        Play.__init__(self, 'penalty')
        self._options = [5, 10, 15]
        self._weights = [1555/2624, 679/2624, 390/2624]


    def weighted_rand_penalty_yds(self):
        return -1*(random.choices(self._options, self._weights, k =1)[0])

    def makePlay(self, offense, defense):
        yards = self.weighted_rand_penalty_yds()
        self._name = f'{-1*yards} yard penalty'
        time = self.calculateTimeElapsed('penalty', offense)
        self.set_result(yards, time)
        return self._result


