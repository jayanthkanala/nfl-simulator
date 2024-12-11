import numpy as np
import random
from scipy.stats import skewnorm, skew
import pandas as pd
from Team import nfls

class Play:
    """
    Represents a single play in the game simulation.

    This class encapsulates the details of a single play, including its name, 
    simulation results in terms of yards and time elapsed, and the total game variables after the play

    Attributes:
        _name (str): The name of the play.
        _result (dict): A dictionary tracking the result of the play in terms of yards and time elapsed.
        _gameResult (dict): A dictionary representing the overall game state changes after the play.
    """
    def __init__(self, name):
        self._name = name
        self._result = {
            'yards': 0,
            'timeElapsed':0}
        self._gameResult = {
            'Home Score': 0,
            'Away Score': 0,
            'Offense': '',
            'Defense': '',
            'Position': 0,
            'Play Number': 0,
            'Play Name': '',
            'Yards': 0,
            'Clock': 0,
            'Down': 1,
            'Quarter': 1,
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

    def set_game_results(self, playNum,playName,homeScore, awayScore, offense, defense, position, yards, timeElapsed, down, quarter):
        """
        Sets all values in the _gameResult dictionary.
        """
        self._gameResult['Play Number'] = playNum
        self._gameResult['Play Name'] = playName
        self._gameResult['Home Score'] = homeScore
        self._gameResult['Away Score'] = awayScore
        self._gameResult['Yards'] = round(yards, 0)
        self._gameResult['Clock'] = round(timeElapsed, 1)
        self._gameResult['Position'] = position
        self._gameResult['Offense'] = offense
        self._gameResult['Defense'] = defense
        self._gameResult['Down'] = down
        self._gameResult['Quarter'] = quarter



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
        avg, sd, skew = offense.average_time(playtype)
        mean = avg + skewnorm.rvs(2, 18, scale=3, size=1)[0] #random Flat increase to time
        #print('mean: ', mean, 'sd: ', sd, 'skew: ', skew)
        return self.random_yards_time(mean, sd, skew)

    def random_yards(self, mean, sd, yards, skewness):
        while True:
            rand_yards = skewnorm.rvs(skewness, loc=mean, scale=abs(sd), size=1)
            if (yards - 100) <= rand_yards <= yards:
                break
        return rand_yards

        #mean, sd = average_off_def(offense = "BUF", defense = "KC", play_type = "fumble")[0]

        #buf_yards = random_yards(mean, sd, yards = 75, skewness = 0) #75 is a placeholder

    def random_yards_time(self, mean, sd, skewness):
        """
        Outputs a random number of yards or time elapsed based on mean, standard deviation, and skewness. Uses a skewed normal distribution.
        :param mean: Average time or yards
        :type mean: float
        :param sd: Standard deviation.
        :type sd: float
        :param skewness: Skew of normal distribution.
        :type skewness: float
        :return: Random yards or time.
        """
        if not isinstance(sd, float):
          sd = 1e-6
        if not isinstance(skewness, float):
          skewness = 1e-6
        return skewnorm.rvs(skewness, loc=mean, scale=abs(sd), size=1)[0]

    def fumble_chance(self, play_type, off, deff):
        """
        Calculates the chance of a fumble based on the offense, defense, and play type
        :param play_type: Play type corresponding to nfls dataframe column title.
        :type play_type: string
        :param off: Abbreviation of offense.
        :type off: string
        :param deff: Abbreviation of defense.
        :type deff: string
        :return: Decimal representation of fumble chance.
        """
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

    def percent_chance_penalty(self, play_type):
        """
        Outputs the percent chance of a live ball penalty for any play type.
        :param play_type: Play type corresponding to column name of nfls data frame.
        :type play_type: string
        :return: Percent chance of a penalty on a specified play type.
        """
        new = nfls[nfls[play_type] == 1]
        count = 0
        total = 0
        for i in new["penalty"]:
          count += i
          total += 1
        chance = count / total
        return chance

    def penalty_Check(self,  play_type):
        #Presnap penalty before choose play should not depend on the playtype
        pen_types = nfls['penalty_type'].unique()
        #Check if penalty
        if random.uniform(0.00, 1.00) > self.percent_chance_penalty(play_type)*6:
          return None
        pen_prob, penalty_avgs = self.pen_probs(play_type)
        penalty_type = None
        for penalty, probability, avg in zip(pen_types, pen_prob, penalty_avgs):
            if random.uniform(0.00,1.00) <= probability:
                penalty_type = penalty

        return penalty_type

    def pen_probs(self, play_type):
        """
        Finds the probability of every penalty and the average yards of every penalty for a specified play_type (rush or pass).
        :param play_type: Play type corresponding to column name of nfls data frame.
        :type play_type: string
        :return: Two lists of probabilities of each penalty type and average yards for each penalty type.
        """
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
        """
        Defines the yards of each penalty type defining it as 5, 10, or 15 based on the average yards and the spot foul of defensive pass interference.
        :param flag_type: Penalty name.
        :type flag_type: string
        :param play_type: Play type corresponding to column name of nfls data frame.
        :type play_type: string
        :return: Yards for a penalty.
        """
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
            return yards
        else:###need check for special penalty types
            return -yards

    def offensive_pens(self):
        """
        Outputs a list of all penalties that can only be called on the offense.
        :return: List of offensive penalties.
        """
        off_pens = []
        for i in nfls['penalty_type'].unique():
            if (isinstance(i, str) and "Offensive" in i):
                off_pens.append(i)
        other_off_pens = ["False Start", "Illegal Formation", "Ilegal Shift", "Ineligible Downfield Pass", "Intentional Grounding", "Low Block", "Illegal Motion"]
        off_pens.extend(other_off_pens)
        return off_pens

    def defensive_pens(self):
        """
        Outputs a list of all penalties that can only be called on the defense.
        :return: List of defensive penalties.
        """
        def_pens = []
        for i in nfls['penalty_type'].unique():
            if (isinstance(i, str) and "Defensive" in i):
                def_pens.append(i)
        other_def_pens = ["Roughing The Passer", "Neutral Zone Infraction"]
        def_pens.extend(other_def_pens)
        return def_pens

    def avg_pen_time(self, penalty_type):
        """"
        Outputs the average elapsed time for plays that have a certain penalty type
        :param penalty_type: Penalty name.
        :type penalty_type: string
        :return: Average time elapsed in seconds for a penalty type.
        """
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

    def sack_chance(self, off, deff):
      """
      Calculates the chance of an sack based on offense and defense.
      :param off: Abbreviation of offense.
      :type off: string
      :param deff: Abbreviation of defense.
      :type deff: string
      :return: Decimal representation of sack chance.
      """
      play_off = nfls[(nfls["pass_attempt"] == 1) & (nfls["posteam"] == off)]
      count_off = 0
      total_off = 0
      for i in play_off["sack"]:
        count_off += i
        total_off += 1
      sack_off = (count_off / total_off) if total_off != 0 else 0.02
      play_def = nfls[(nfls["pass_attempt"] == 1) & (nfls["defteam"] == deff)]
      count_def = 0
      total_def = 0
      for i in play_def["sack"]:
        count_def += i
        total_def += 1
      sack_def = count_def / total_def  if total_def != 0 else 0.02
      sack_pct = (sack_off + sack_def) / 2
      return sack_pct

