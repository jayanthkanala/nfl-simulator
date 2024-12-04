import numpy as np
import pandas as pd
import nfl_data_py as nfl

pd.options.display.max_columns = None
nfls = nfl.import_pbp_data([2023], downcast=True, cache=False, alt_path=None)
team_dict = {}
for team in nfls['home_team']:
    if team not in team_dict:
        team_dict[team] = None

class Team:
    def __init__(self, name):
        self._name = name

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

    def play_percent(self, play_type, offdef = "offteam"):
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

    def average_time(self, play_type, offdef):
        team = self._name
        play_df = nfls[nfls[play_type] == 1 & (nfls[offdef] == team)] #Filters for occurences of play
        count = 0
        total = 0
        for i in play_df['drive_game_clock_start']:
            for j in play_df['drive_game_clock_end']:
                count = j - i
                total+=1
        average_time = count / total
        return average_time

    def average_yards(self, play_type, offdef = 'offteam'):
        team = self._name
        type_df = nfls[(nfls[play_type] == 1) & (nfls[offdef] == team)]
        total = 0
        count = 0
        for i in type_df['yards_gained']:
            count += i
            total += 1
        standard_deviation = np.std(type_df['yards_gained'])
        average_yards = count / total
        return average_yards, standard_deviation

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
            