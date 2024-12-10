from Play import Play
from Team import nfls
import numpy as np
import random
from scipy.stats import skewnorm, skew
import pandas as pd

class PassPlay(Play):
    def __init__(self):
        self._interceptChance = 0
        Play.__init__(self, 'pass_attempt')

    def int_chance(self, off, deff):
        """
        Calculates the chance of an interception based on offense and defense.
        :param off: Abbreviation of offense.
        :type off: string
        :param deff: Abbreviation of defense.
        :type deff: string
        :return: Decimal representation of interception chance.
        """
        play_off = nfls[(nfls["pass_attempt"] == 1) & (nfls["posteam"] == off.get_name())]
        count_off = 0
        total_off = 0
        for i in play_off["interception"]:
            count_off += i
            total_off += 1
        int_off = count_off / total_off
        play_def = nfls[(nfls["pass_attempt"] == 1) & (nfls["defteam"] == deff.get_name())]
        count_def = 0
        total_def = 0
        for i in play_def["interception"]:
            count_def += i
            total_def += 1
        int_def = count_def / total_def
        int_pct = (int_off + int_def) / 2
        return int_pct

    def makePlay(self, offense, defense):
        offenseChance = offense.average_off_def(offense,defense, 'complete_pass', 'completion_percentage')
        offenseSuccess = random.uniform(0.00,1.00) <= offenseChance

        sackChance = self.sack_chance(offense, defense)
        sackSuccess = random.uniform(0.00,1.00) <= sackChance

        interceptChance = self.int_chance(offense, defense)/3
        interceptSuccess = random.uniform(0.00,1.00) <= interceptChance

        penalty = self.penalty_Check('pass_attempt')
        if penalty:
            yards = self.flag_yards(penalty, 'pass_attempt')
            self._name = penalty
            mean, sd, skew = self.avg_pen_time(penalty)
            time = self.random_yards_time(mean, sd, skew)
            self.set_result(yards, time)
        elif sackSuccess:
            self._name = 'sack'
            sack_mean, sack_std, sack_skew = defense.average_off_def(offense, defense, play_type = "sack", funcname = 'average_yards')
            yards = self.random_yards_time(sack_mean, sack_std, sack_skew)
            time = self.calculateTimeElapsed('sack', offense)
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        elif interceptSuccess:
            self._name = 'interception'
            int_mean, int_std, int_skew = defense.average_off_def(offense, defense, play_type = "interception", funcname = 'average_yards')
            if int_mean == 0:
              int_mean = 10
              int_std = 10
              int_skew = 2
            yards = self.random_yards_time(int_mean, int_std, int_skew)
            time = self.calculateTimeElapsed('interception', offense)
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
        elif offenseSuccess:
            self._name = 'complete_pass'
            averageYards, stdYards, skew = offense.average_off_def(offense, defense, 'complete_pass', 'average_yards')
            yards = self.random_yards_time(averageYards, stdYards, skew)
            time = self.calculateTimeElapsed('complete_pass', offense)
            self.set_result(yards, time)
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
        penalty = self.penalty_Check('pass_attempt')
        if penalty:
            yards = self.flag_yards(penalty, 'pass_attempt')
            self._name = penalty
            mean, sd, skew = self.avg_pen_time(penalty)
            time = self.random_yards_time(mean, sd, skew)
            self.set_result(yards, time)
        else:
            mean, sd, skew = offense.average_off_def(offense, defense, 'rush_attempt', 'average_yards')
            yards = self.random_yards_time(mean, sd, skew)
            if yards > 0:
              self._name = 'rush'
            time = self.calculateTimeElapsed('rush_attempt', offense)
            self.set_result(yards, time)
        return self._result

class FieldGoal(Play):
    def __init__(self, score):
        Play.__init__(self, 'field_goal')
        self._result['success'] = False
        self._score = score

    def getScore(self):
        return self._score

    def setScore(self, newScore):
        self._score = newScore

    def getSuccess(self):
        return self._result['success']

    def set_result(self,success = False, yards=0, timeElapsed=0):
        self._result = {
            'success': success,
            'yards': yards,
            'timeElapsed':timeElapsed}

    def field_goal_percentage(self, currentPosition, offense):
        """
        Calculates the field goal percentage of a team for kicks within 5 yards of 100 - currentPostion
        :param currentPosition: Position on field for offense (1-100)
        :type currentPosition: float
        :param team: Abbreviation of offensive team name.
        :type team: string
        :return: Decimal representation of field goal percentage
        """
        fg = nfls[(nfls["field_goal_attempt"]== 1) & (abs((nfls["yardline_100"] - (100-currentPosition))) <= 5) & (nfls["posteam"]== offense.get_name()) ] #Creates new df for fg attempts and the yardline being within 5 of the currentPosition
        count = 0
        total = 0
        for i in fg["field_goal_result"]:
            if i == "made":
                count += 1
                total += 1
            else:
                total += 1
        fg_pct = (count / total) if total >0 else 0
        return fg_pct

    def makePlay(self, offense, currentPosition, touchdown = True):
        #Need to add check if offense or defense penalty to see if yards is positive or negative
        #70 30 field goal chance for now

        fieldGoalSuccess = random.uniform(0.00, 1.00) <= self.field_goal_percentage(currentPosition, offense)
        penalty = self.penalty_Check('field_goal_attempt')
        if penalty:
            yards = self.flag_yards(penalty, 'field_goal_attempt')
            self._name = penalty
            mean, sd, skew = self.avg_pen_time(penalty)
            time = self.random_yards_time(mean, sd, skew)
            self.set_result(False, -1*yards, time)
        elif fieldGoalSuccess:
            time = self.calculateTimeElapsed('field_goal_attempt', offense)
            self.set_result(True, 0, time)
        else:
            time = self.calculateTimeElapsed('field_goal_attempt', offense)
            self.set_result(False, 0, time)
        return self._result

class KickOff(Play):
    def __init__(self):
        Play.__init__(self, 'kick_off')

    def punt_kick_simulator(self, off, currentPosition, puntorkick = 'kickoff_attempt'): #parameter is offense
        """
        Calculates a random punt or kick yardage based on the offense and current position on the field.
        :param off: Abbreviation of offensive team name.
        :type off: string
        :param currentPosition: Position on field for offense (1-100)
        :type currentPosition: float
        :param puntorkick: "punt_attempt" or "kickoff_attempt"
        :type puntorkick: string
        :return: A punt or kick yardage.
        """
        if puntorkick == 'kickoff_attempt':
            self._name = 'kickoff'
        punt_df = nfls[(nfls[puntorkick] == 1) & (nfls["posteam"]==off)]
        count = 0
        total = 0
        for i in punt_df["kick_distance"]:
            count += i
            total += 1
        punt_avg = count / total
        punt_sd = np.std(punt_df["kick_distance"])
        skewness = skew(punt_df["kick_distance"])
        while True: #Check that punt isn't too far
            rand_punt = skewnorm.rvs(skewness, punt_avg, punt_sd, 1)
            if rand_punt < ((100- currentPosition) + 10): #Represents currentPosition + end zone length because punts can land in endzone
                break
        return rand_punt[0]

    def makePlay(self, offense, defense):
        kick_yards = (35+self.punt_kick_simulator(defense.get_name(), 35, puntorkick = 'kickoff_attempt'))
        mean, sd, skew = offense.average_return_yards("kickoff_attempt", 'posteam')
        return_yards = self.random_yards_time(mean, sd, skew)
        yards = return_yards + (100-kick_yards)
        if yards < 0:
          yards = 20
        time = self.calculateTimeElapsed('kickoff_attempt', offense)
        self.set_result(yards, time)
        return self._result



class Punt(Play):

    def __init__(self):
        Play.__init__(self, 'puntorkick')

    def punt_simulator(self, off, currentPosition, puntorkick = 'punt_attempt'): #parameter is offense
        if puntorkick == 'punt_attempt':
            self._name = 'punt_attempt'
        punt_df = nfls[(nfls[puntorkick] == 1) & (nfls["posteam"]==off.get_name())]
        count = 0
        total = 0
        for i in punt_df["kick_distance"]:
            count += i
            total += 1
        punt_avg = count / total
        punt_sd = np.std(punt_df["kick_distance"])
        skewness = skew(punt_df["kick_distance"])
        while True: #Check that punt isn't too far
            rand_punt = skewnorm.rvs(skewness, punt_avg, punt_sd, 1)
            if rand_punt < ((100- currentPosition) + 10): #Represents currentPosition + end zone length because punts can land in endzone
                break
        return rand_punt[0]

    def makePlay(self, offense, currentPosition, puntorkick = 'punt_attempt'):
        yards = self.punt_simulator(offense, currentPosition, puntorkick)
        time = self.calculateTimeElapsed(puntorkick, offense)
        self.set_result(yards, time)
        return self._result