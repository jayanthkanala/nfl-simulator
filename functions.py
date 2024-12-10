# -*- coding: utf-8 -*-
"""NFLGameSimulator.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XoVs9O1Txo5wDwedOOim6g5i7nXCfOq_

NFL GAME SIMULATOR FUNCTIONS
"""

!pip install nfl-data-py

import nfl_data_py as nfl

"""Create Data Frame"""

import pandas as pd
pd.options.display.max_columns = None
nfls = nfl.import_pbp_data([2023], downcast=True, cache=False, alt_path=None)
team_dict = {}
for team in nfls['home_team']:
    if team not in team_dict:
        team_dict[team] = None

"""Create dictionary for teams (is not used within functions but could be useful for other sections)"""

import numpy as np
team_dict = {}
for team in nfls['home_team']:
    if team not in team_dict:
        team_dict[team] = None
print(team_dict)

def play_percent(team, play_type, offdef):
  team_df = nfls[nfls[offdef] == team] #Filter data frame based on offense team
  count = 0
  total = 0
  for i in team_df[play_type]:
    if i == 1:
      count += 1
      total += 1
    else:
      total += 1
  percent = count / total
  return percent

def average_time(play_type):
  play_df = nfls[nfls[play_type] == 1] #Filters for occurences of play
  count = 0
  total = 0
  for i in play_df['drive_game_clock_start']:
    for j in play_df['drive_game_clock_end']:
      count = j - i
      total+=1
  average_time = count / total
  return average_time

def average_yards(play_type, team, offdef): #Avg yards and standard devaition for a specified play type
  type_df = nfls[(nfls[play_type] == 1) & (nfls[offdef] == team)]
  total = 0
  count = 0
  for i in type_df['yards_gained']:
    count += i
    total += 1
  standard_deviation = np.std(type_df['yards_gained'])
  average_yards = count / total
  return average_yards, standard_deviation

def kickoffs(team, kickrec): #Touchback pct
  type_df = nfls[(nfls["kickoff_attempt"] == 1) & (nfls[kickrec] == team)]
  total = 0
  count = 0
  for i in type_df['touchback']:
    count += i
    total += 1
  touchback_pct = count / total
  return touchback_pct


def completion_percentage(team, offdef, play_type = "complete_pass"): #Completion percentage (play_type variable is added to comply with avg func)
  type_df = nfls[(nfls["pass_attempt"] == 1) & (nfls[offdef] == team)]
  total = 0
  count = 0
  for i in type_df[play_type]:
    count += i
    total += 1
  completion_pct = count / total
  return completion_pct

def average_return_yards(team, kickpunt, kickrec): #Average return yards for punting or kicking team or defensive team
  type_df = nfls[(nfls[kickpunt] == 1) & (nfls[kickrec] == team)]
  total = 0
  count = 0
  for i in type_df['return_yards']:
    count += i
    total += 1
  avg_return = count / total
  sd = np.std(type_df['return_yards'])
  return avg_return, sd

"""Average between offense and defense"""

#Find average yards, play percents, and completion percentages by averaging offense and defense stats

import random
import numpy as np
from scipy.stats import skewnorm #Rushing and passing are right skewed:

def average_off_def(offense, defense, play_type, funcname): #Averages offense with defense based on play_type and function name
  if funcname == average_yards:
    off_mean = funcname(team = offense, play_type = play_type, offdef = "posteam")[0] #Use 0 index in case of multiple returns in function
    def_mean = funcname(team = defense, play_type = play_type, offdef = "defteam")[0]
    off_sd = funcname(team = offense, play_type = play_type, offdef = "posteam")[1] #Use 0 index in case of multiple returns in function
    def_sd = funcname(team = defense, play_type = play_type, offdef = "defteam")[1]
    avg_yards = (off_mean + def_mean) / 2
    avg_sd = (off_sd + def_sd) / 2
    return avg_yards, avg_sd
  else:
    off_mean = funcname(team = offense, play_type = play_type, offdef = "posteam")
    def_mean = funcname(team = defense, play_type = play_type, offdef = "defteam")
    avg = (off_mean + def_mean) / 2
    return avg

rush_avg = average_off_def(offense = "BUF", defense = "KC", play_type = "rush_attempt", funcname = average_yards)[0]
complete = average_off_def(offense = "BUF", defense = "KC", play_type = "complete_pass", funcname = completion_percentage)
pass_att_pct = average_off_def(offense = "BUF", defense = "KC", play_type = "pass_attempt", funcname = play_percent)

print(f"When Buffalo is on offense, and Kansas City is on defense, the mean yards on a rush attempt is {rush_avg}")
print(f"When Buffalo is on offense, and Kansas City is on defense, Buffalo's assumed completion percentage is {complete}")
print(f"When Buffalo is on offense, and Kansas City is on defense, Buffalo is assumed to pass the ball {pass_att_pct} of the time")

"""Using right skew distribution for weighted random yards"""

#Defines random yards function based on right-skew distribution
#We can do more testing on data to get exact skew values for rush and pass

def random_yards(mean, sd, yards, skewness):
  while True:
    rand_yards = skewnorm.rvs(skewness, loc=mean, scale=sd, size=1)
    if (yards - 100) <= rand_yards <= yards:
      break
  return rand_yards

mean = average_off_def(offense = "BUF", defense = "KC", play_type = "complete_pass", funcname = average_yards)[0]
sd = average_off_def(offense = "BUF", defense = "KC", play_type = "complete_pass", funcname = average_yards)[1]

buf_yards = random_yards(mean, sd, yards = 75, skewness = 1.5) #75 is a placeholder
print(f"Buffalo completes a pass for {buf_yards} yards!")

"""Dealing with penalties"""

#Penalty functions
#Does not account for spot fouls (pass interference etc.) (yet)
#Chooses random penalty yardage between 5, 10, 15 based on entire NFL probabilities

def penalty_yards():
  pen_options = [5, 10, 15]
def penalty_yard_freq(yards): #5, 10, 15 (not counting spot fouls)
  count = 0
  for yard in nfls["penalty_yards"]:
    if yard == yards:
      count +=1
  return count
def percent_chance_penalty(yards): #Assume penalty type is random (use entire nfl).
  five = penalty_yard_freq(5)
  ten = penalty_yard_freq(10)
  fifteen = penalty_yard_freq(15)
  chance = penalty_yard_freq(yards) / (five + ten + fifteen)
  return chance

def weighted_rand_penalty_yds():
  outcomes = [5, 10, 15]
  penalty_probs = [percent_chance_penalty(5), percent_chance_penalty(10), percent_chance_penalty(15)]
  penalty_yardage = random.choices(outcomes, weights = penalty_probs, k =1)
  return penalty_yardage

yds = weighted_rand_penalty_yds()
print(f"Penalty yards: {yds}")

"""Outputting a random outcome based on normalized weighted probabilities

"""

#Demo functions for defining probabilities of each outcome when a team is on offense.
#Also chooses random outcome based on normalized weighted probabilities

def define_probs(offense, defense):
  outcomes = ["rush_attempt", "pass_attempt", "sack", "fumble", "interception", "penalty"]
  probs = []
  for outcome in range(len(outcomes)):
    prob = average_off_def(offense = offense, defense = defense, play_type = outcomes[outcome], funcname = play_percent)
    probs.append(prob)
  return probs

probs = define_probs("BUF", "KC") #Use Buffalo and KC


def normalize_probs(probs):
  total = 0
  normalized_probs = []
  for p in probs:
    total += p
  for p in probs:
    normal_prob = p / total
    normalized_probs.append(normal_prob)
  return normalized_probs

norm_probs = normalize_probs(probs) #Defines normalized probs list

def choose_outcome(norm_probs):
  outcomes = ["rush_attempt", "pass_attempt", "sack", "fumble", "interception", "penalty"]
  choice = random.choices(outcomes, weights=norm_probs, k=1)
  return choice

print(choose_outcome(norm_probs)) #Based on this outcome we can apply the correct function(s) subsequently