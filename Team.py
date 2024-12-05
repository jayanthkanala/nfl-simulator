import numpy as np
import pandas as pd
import nfl_data_py as nfl
from random import random
from scipy.stats import skew


pd.options.display.max_columns = None
nfls = nfl.import_pbp_data([2023], downcast=True, cache=False, alt_path=None)
team_dict = {}
for team in nfls['home_team']:
    if team not in team_dict:
        team_dict[team] = None

class Team:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def pass_percent(self):
        team = self._name
        team_df = nfls[nfls['posteam'] == team] #Filter data frame based on offense team
        count = 0
        total = 0
        for i in team_df['pass_attempt']:
            if i == 1:
                count += 1
                total += 1
            else:
                total += 1
        pass_percent = count / total
        return pass_percent

    def play_percent(self, play_type, offdef = "posteam"):
        team = self._name
        team_df = nfls[nfls[offdef] == team] #Filter data frame based on offense team
        count = 0
        total = 0
        for i in team_df[play_type]:
            if i == 1:
                count += 1
                total += 1
            else:
                total += 1
        rush_percent = count / total
        return rush_percent

    def convert_time_to_seconds(self, time):
        if not time:
            return None #handles None values
        minutes, seconds = time.split(':')
        return int(minutes) * 60 + int(seconds)

    def average_time(self, play_type):
        time_seconds = []
        for time in nfls["time"]:
            time_seconds.append(self.convert_time_to_seconds(time))
        nfls["time_seconds"] = time_seconds #New row in the data frame
        nfls_index = nfls.index[nfls[play_type] == 1]
        count = 0
        total = 0
        times = []
        for i in nfls_index:
            if pd.notna(nfls.loc[i, "time_seconds"]) and pd.notna(nfls.loc[i+1, "time_seconds"]):
                play_time = (nfls.loc[i, "time_seconds"]) - (nfls.loc[i+1, "time_seconds"])
                count += play_time
                total += 1
                times.append(play_time)
        avg_time = count / total
        sd = np.std(times)
        skewness = skew(times)
        return avg_time,sd, skewness

    def average_yards(self, play_type, offdef = 'posteam'): #Avg yards and standard devaition for a specified play type
        type_df = nfls[(nfls[play_type] == 1) & (nfls[offdef] == self._name)]
        total = 0
        count = 0
        for i in type_df['yards_gained']:
          count += i
          total += 1
        standard_deviation = np.std(type_df['yards_gained'])
        skewness = skew(type_df['yards_gained'])
        average_yards = count / total
        return average_yards, standard_deviation, skewness

    def kickoffs(self, kickrec):
        team = self._name
        type_df = nfls[(nfls["kickoff_attempt"] == 1) & (nfls[kickrec] == team)]
        total = 0
        count = 0
        for i in type_df['touchback']:
            count += i
            total += 1
        touchback_pct = count / total
        return touchback_pct


    def completion_percentage(self, offdef):
        team = self._name
        type_df = nfls[(nfls["pass_attempt"] == 1) & (nfls[offdef] == team) & ((nfls["touchback"] != 1) & ((nfls["punt_fair_catch"] != 1) & (nfls["kickoff_fair_catch"] != 1)))]
        total = 0
        count = 0
        for i in type_df['complete_pass']:
            count += i
            total += 1
        completion_pct = count / total
        return completion_pct

    def average_return_yards(self, kickpunt = 'kickoff_attempt', kickrec = 'posteam'):
        team = self._name
        type_df = nfls[(nfls[kickpunt] == 1) & (nfls[kickrec] == team)]
        total = 0
        count = 0
        for i in type_df['return_yards']:
            count += i
            total += 1
        avg_return = count / total
        sd = np.std(type_df['return_yards'])
        return avg_return, sd

    def fieldGoalChance(self):
        x=x

    def average_off_def(self, offense, defense, play_type, funcname): #Averages offense with defense based on play_type and function name
        if funcname == 'average_yards':
            off_mean, off_sd, off_skew = offense.average_yards(play_type = play_type, offdef = "posteam") #Use 0 index in case of multiple returns in function
            def_mean, def_sd, def_skew = defense.average_yards(play_type = play_type, offdef = "defteam")
            avg_yards = (off_mean + def_mean) / 2
            avg_sd = (off_sd + def_sd) / 2
            avg_skew = (off_skew + def_skew) /2
            return avg_yards, avg_sd, avg_skew
        elif funcname == 'completion_percentage':
            off_mean = offense.completion_percentage(offdef = "posteam")
            def_mean = defense.completion_percentage(offdef = "defteam")
            avg = (off_mean + def_mean) / 2
            return avg
        elif funcname == 'play_percent':
            off_mean = offense.play_percent(play_type = play_type, offdef = "posteam")
            def_mean = defense.play_percent(play_type = play_type, offdef = "defteam")
            avg = (off_mean + def_mean) / 2
            return avg

        #rush_avg = average_off_def(offense = "BUF", defense = "KC", play_type = "rush_attempt", funcname = average_yards)[0]
        #complete = average_off_def(offense = "BUF", defense = "KC", play_type = "complete_pass", funcname = completion_percentage)
        #pass_att_pct = average_off_def(offense = "BUF", defense = "KC", play_type = "pass_attempt", funcname = play_percent)

    def choosePlay(self, offense, defense):
        outcomes = ["rush_attempt", "pass_attempt", "penalty"] #, "sack", "fumble", "interception", "penalty"
        probs = []
        for outcome in range(len(outcomes)):
            prob = self.average_off_def(offense = offense, defense = defense, play_type = outcomes[outcome], funcname = 'play_percent')
            probs.append(prob)

        total = 0
        normalized_probs = []
        for p in probs:
            total += p
        for p in probs:
            normal_prob = p / total
            normalized_probs.append(normal_prob)
         #Defines normalized probs list
        choice = random.choices(outcomes, weights=normalized_probs, k=1)

        return choice
