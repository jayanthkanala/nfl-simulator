import numpy as np
import random
from scipy.stats import skewnorm, skew
import pandas as pd
from Team import nfls

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

    def convert_time_to_seconds(self, time):
        if not time:
            return None #handles None values
        minutes, seconds = time.split(':')
        return int(minutes) * 60 + int(seconds)
    
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
            rand_yards = skewnorm.rvs(skewness, loc=mean, scale=abs(sd), size=1)
            if (yards - 100) <= rand_yards <= yards:
                break
        return rand_yards

        #mean, sd = average_off_def(offense = "BUF", defense = "KC", play_type = "fumble")[0]

        #buf_yards = random_yards(mean, sd, yards = 75, skewness = 0) #75 is a placeholder

    def random_yards_time(self, mean, sd, skewness):
        return skewnorm.rvs(skewness, loc=mean, scale=abs(sd), size=1)[0]
    
    def fumble_chance(self, play_type, off, deff):
        play_off = nfls[(nfls[play_type] == 1) & (nfls["posteam"] == off)]
        count_off = 0
        total_off = 0
        for i in play_off["fumble_lost"]:
            count_off += i
            total_off += 1
        fumble_chance_off = count_off / total_off
        play_def = nfls[(nfls[play_type] == 1) & (nfls["defteam"] == deff)]
        count_def = 0
        total_def = 0
        for i in play_def["fumble_lost"]:
            count_def += i
            total_def += 1
        fumble_chance_def = count_def / total_def
        fumble_pct = (fumble_chance_off + fumble_chance_def) / 2
        return fumble_pct
    
    def isPenalty(self):
        return (self._name in (nfls['penalty_type'].unique()))
    
    
    def percent_chance_penalty(self, play_type): #Assume penalty type is random (use entire nfl).
        new = nfls[nfls[play_type] == 1]
        count = 0
        total = 0
        for i in new["penalty"]:
          count += i
          total += 1
        chance = count / total
        return chance
    
    def penalty_Check(self,  play_type):
        pen_types = nfls['penalty_type'].unique()
        if random.uniform(0.00, 1.00) > self.percent_chance_penalty(play_type):
            return None
        pen_prob, penalty_avgs = self.pen_probs(play_type)
        penalty_type = None
        for penalty, probability, avg in zip(pen_types, pen_prob, penalty_avgs):
            if random.uniform(0.00,1.00) <= probability: 
                penalty_type = penalty
            
        return penalty_type
    
    def pen_probs(self, play_type):
        unique_penalties = nfls['penalty_type'].unique()
        new = nfls[(nfls[play_type] == 1) & (nfls["penalty"]==1)]
        penalty_frequencies = [0] * len(unique_penalties)
        penalty_yds = [0] * len(unique_penalties)
        penalty_probs = [] #Create dictionaries with penalty name as key
        penalty_avgs = []
        for i in new.index:
            for k in range(len(unique_penalties)):
                if unique_penalties[k] == new.loc[i, "penalty_type"]:
                    penalty_frequencies[k] += 1
                    penalty_yds[k] += new.loc[i, "penalty_yards"]
        for i in range(len(penalty_yds)):
            if penalty_frequencies[i] > 0:
                penalty_avg = penalty_yds[i] / penalty_frequencies[i]
                penalty_avgs.append(penalty_avg)
            else:
                penalty_avg = 0
                penalty_avgs.append(penalty_avg)
        for i in range(len(penalty_frequencies)):
            penalty_prob = penalty_frequencies[i] / sum(penalty_frequencies)
            penalty_probs.append(penalty_prob)
        return penalty_probs, penalty_avgs
    
    def flag_yards(self, flag_type, play_type):
        unique_values = nfls['penalty_type'].unique()
        penalty_avgs = self.pen_probs(play_type)[1]
        avg_flag_yds = 0
        for idx, flag in enumerate(unique_values):
            if flag_type == unique_values[idx]:
                if  0 < penalty_avgs[idx] <= 5:
                    yards = 5
                elif 5 < penalty_avgs[idx] <= 10:
                    yards = 10
                elif penalty_avgs[idx] > 10 and (unique_values[idx] != "Defensive Pass Interference"):
                    yards = 15
                elif penalty_avgs[idx] == 0:
                    yards = 0
                elif flag_type == "Defensive Pass Interference":
                    mean = penalty_avgs[idx]
                    yards = skewnorm.rvs(2.5, mean, 10, 1)[0] #assume sd of 10 and skew of 2.5, returns array
        if flag_type in self.offensive_pens():
            return -yards
        if flag_type in self.defensive_pens():
            return -yards
        else:###need check for special penalty types
            return -yards 
    
    def offensive_pens(self):
        off_pens = []
        for i in nfls['penalty_type'].unique():
            if (isinstance(i, str) and "Offensive" in i):
                off_pens.append(i)
        other_off_pens = ["False Start", "Illegal Formation", "Ilegal Shift", "Ineligible Downfield Pass", "Intentional Grounding", "Low Block", "Illegal Motion"]
        off_pens.extend(other_off_pens)
        return off_pens

    def defensive_pens(self):
        def_pens = []
        for i in nfls['penalty_type'].unique():
            if (isinstance(i, str) and "Defensive" in i):
                def_pens.append(i)
        other_def_pens = ["Roughing The Passer", "Neutral Zone Infraction"]
        def_pens.extend(other_def_pens)
        return def_pens
    
    def special_teams_pens(self):
        spec_pens = []
        for i in nfls['penalty_type'].unique():
            if (isinstance(i, str) and (("Kick" in i) or ("Kicker" in i))):
                spec_pens.append(i)
        other_spec_pens = ["Leverage", "Leaping"]
        spec_pens.extend(other_spec_pens)
        return spec_pens

    def avg_pen_time(self, penalty_type):
        time_seconds = []
        for time in nfls["time"]:
            time_seconds.append(self.convert_time_to_seconds(time))
        nfls["time_seconds"] = time_seconds #New row in the data frame
        nfls_index = nfls.index[(nfls["penalty"] == 1) & (nfls["penalty_type"] == penalty_type)]
        count = 0
        total = 0
        times = []
        for i in nfls_index:
            if pd.notna(nfls.loc[i, "time_seconds"]) and pd.notna(nfls.loc[i+1, "time_seconds"]):
                play_time = (nfls.loc[i, "time_seconds"]) - (nfls.loc[i+1, "time_seconds"])
                count += play_time
                total += 1
                times.append(play_time)
        if total > 0:
            avg_time = count / total
            sd = np.std(times)
            skewness = skew(times)
        else:
            avg_time = None
            sd = None
            skewness = None
        return avg_time,sd, skewness


class PassPlay(Play):
    def __init__(self):
        self._interceptChance = 0
        Play.__init__(self, 'pass_attempt')

    def int_chance(self, off, deff):
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

        sackChance = 0.10
        sackSuccess = random.uniform(0.00,1.00) <= sackChance

        interceptChance = self.int_chance(offense, defense)
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
            yards = self.random_yards_time(int_mean, int_std, int_skew)
            time = self.calculateTimeElapsed('interception', offense)
            self.set_result(yards, time) #Use a default of 10 seconds for failed play for now
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
        sackChance = 0.10 #Add function for this
        sackSuccess = random.uniform(0.00,1.00) <= sackChance
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
        
    def field_goal_percentage(self, currentPosition, offense): #Function calculates field goal percentage based on yardage interval of kick
        fg = nfls[(nfls["field_goal_attempt"]== 1) & (abs((nfls["yardline_100"] - (100-currentPosition))) <= 5) & (nfls["posteam"]== offense.get_name()) ] #Creates new df for fg attempts and the yardline being within 5 of the currentPosition
        count = 0
        total = 0
        for i in fg["field_goal_result"]:
            if i == "made":
                count += 1
                total += 1
            else:
                total += 1
        fg_pct = count / total
        return fg_pct

    def makePlay(self, offense, currentPosition):
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



class Punt(Play):

    def __init__(self):
        Play.__init__(self, 'puntorkick')

    def punt_simulator(self, off, currentPosition, puntorkick = 'kickoff_attempt'): #parameter is offense
        if puntorkick == 'kickoff_attempt':
            self._name = 'kickoff_attempt'
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
    
    def makePlay(self, offense, currentPosition, puntorkick):
        yards = self.punt_simulator(offense, currentPosition, puntorkick)
        time = self.calculateTimeElapsed(puntorkick, offense)
        self.set_result(yards, time)
        return self._result