# -*- coding: utf-8 -*-
"""NFLGameSimulator.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XoVs9O1Txo5wDwedOOim6g5i7nXCfOq_

NFL GAME SIMULATOR FUNCTIONS
"""

!pip install nfl-data-py #Install library

import nfl_data_py as nfl #Import library

"""Create Data Frame"""

import pandas as pd
pd.options.display.max_columns = None #Shows all columns
nfls = nfl.import_pbp_data([2023], downcast=True, cache=False, alt_path=None)
team_dict = {}
for team in nfls['home_team']:
    if team not in team_dict:
        team_dict[team] = None

"""Create dictionary for teams (is not used within functions but could be useful for other sections)"""

from scipy.stats import skew
import numpy as np
def teams_list():
  """
  Creates a list of all team abbreviations.
  :return: List of all 32 team abbreviations.
  """
  team_list = []
  for team in nfls['home_team']:
      if team not in team_list:
          team_list.append(team)
  return team_list

def play_percent(team, play_type, offdef):
  """
  Outputs a percent that a play occurs for a specified team on offense or defense.
  :param team: Team abbreviation.
  :type team: string
  :param play_type: Play type that corresponds to a column name of nfls data frame.
  :type play_type: string
  :param offdef: Either "posteam" (offense) or "defteam" representing whether the team is on offense or defense.
  :type offdef: string
  :return: Decimal representation of the percent a play_type occurs with a specified team on offense or defense.
  """
  team_df = nfls[nfls[offdef] == team] #Filter data frame based on team and offdef
  count = 0
  total = 0
  for i in team_df[play_type]:
    if i == 1: #Play type occurs
      count += 1
      total += 1
    else: #Play type does not occur
      total += 1
  percent = count / total
  return percent

def average_yards(play_type, team, offdef):
  """
  Outputs an average yards, skewness, and standard deviation for a team on offense or defense for a specified playtype
  :param play_type: Play type that corresponds to a column name of nfls data frame.
  :type play_type: string
  :param team: Team abbreviation.
  :type team: string
  :param offdef: Either "posteam" (offense) or "defteam" representing whether the team is on offense or defense.
  :type offdef: string
  :return: Average yards, standard deviation, and skewness.
  """
  type_df = nfls[(nfls[play_type] == 1) & (nfls[offdef] == team)] #Filter data frame based on parameters
  total = 0
  count = 0
  for i in type_df['yards_gained']: #Average
    count += i
    total += 1
  standard_deviation = np.std(type_df['yards_gained'])
  skewness = skew(type_df['yards_gained'])
  average_yards = count / total
  return average_yards, standard_deviation, skewness

def touchback_percent(team, kickrec):
  """
  Outputs a percentage of a teams kickoffs that are touchbacks if they are kicking or receiving.
  :param team: Team abbreviation.
  :type team: string
  :param kickrec: Either "posteam" (receiving) or "defteam" (kicking).
  :type kickrec: string
  :return: Decimal representation of touchback percentage.
  """
  type_df = nfls[(nfls["kickoff_attempt"] == 1) & (nfls[kickrec] == team)] #Filter dataframe based on parameters
  total = 0
  count = 0
  for i in type_df['touchback']:
    count += i
    total += 1
  touchback_pct = count / total
  return touchback_pct


def completion_percentage(team, offdef, play_type = "complete_pass"):
  """
  Outputs the completion percentage of a team when they are on offense or defense.
  :param team: Team abbreviation.
  :type team: string
  :param offdef: Either "posteam" (offense) or "defteam" (defense).
  :type offdef: string
  :param play_type: Will always be "complete_pass". Is included to comply with the parameters of average_off_def function.
  :return: Decimal representation of completion percentage.
  """
  type_df = nfls[(nfls["pass_attempt"] == 1) & (nfls[offdef] == team)] #Filter dataframe based on parameters
  total = 0
  count = 0
  for i in type_df[play_type]:
    count += i
    total += 1
  completion_pct = count / total
  return completion_pct

def average_return_yards(team, kickpunt, kickrec, play_type = "return_yards"):
  """
  Outputs an average yards, skewness, and standard deviation for a team kicking or receiving
  :param team: Team abbreviation.
  :type team: string
  :param kickpunt: Either "kickoff_attempt" (kick) or "punt_attempt" (punt).
  :type kickpunt: string
  :param kickrec: Either "posteam" (receiving) or "defteam" (kicking).
  :type kickrec: string
  :param play_type: Set to default "return_yards".
  :type play_type: string
  :return: Average return yards, standard deviation, and skewness.
  """
  type_df = nfls[(nfls[kickpunt] == 1) & (nfls[kickrec] == team)] #Filter dataframe based on parameters
  total = 0
  count = 0
  for i in type_df[play_type]:
    count += i
    total += 1
  avg_return = count / total
  sd = np.std(type_df[play_type])
  skewness = skew(type_df[play_type])
  return avg_return, sd, skewness

"""Average between offense and defense"""

#Find average yards, play percents, and completion percentages by averaging offense and defense stats

import random
import numpy as np
from scipy.stats import skewnorm #Rushing and passing are right skewed:

def average_off_def(offense, defense, play_type, funcname):
  """
  Outputs the average stat of an offense vs a defense for a specific play type.
  :param offense: Team abbreviation of team on offense.
  :type offense: string
  :param defense: Team abbreviation of team on defense.
  :type defense: string
  :param play_type: Play type corresponding to column name of nfls dataframe
  :type play_type: string
  :param funcname: Name of function being called to average.
  :type funcname: function name
  :return: Average stat, standard deviation, skewness of a play type in a specfied game.
  """
  if funcname == average_yards:
    off_mean = funcname(team = offense, play_type = play_type, offdef = "posteam")[0] #Use 0 index in case of multiple returns in function
    def_mean = funcname(team = defense, play_type = play_type, offdef = "defteam")[0]
    off_sd = funcname(team = offense, play_type = play_type, offdef = "posteam")[1] #Use 1 index in case of multiple returns in function
    def_sd = funcname(team = defense, play_type = play_type, offdef = "defteam")[1]
    off_skew = funcname(team = offense, play_type = play_type, offdef = "posteam")[2] #Use 2 index in case of multiple returns in function
    def_skew = funcname(team = defense, play_type = play_type, offdef = "defteam")[2]
    avg_yards = (off_mean + def_mean) / 2
    avg_sd = (off_sd + def_sd) / 2
    avg_skew = (off_skew + def_skew) / 2
    return avg_yards, avg_sd, avg_skew
  else:
    off_mean = funcname(team = offense, play_type = play_type, offdef = "posteam")
    def_mean = funcname(team = defense, play_type = play_type, offdef = "defteam")
    avg = (off_mean + def_mean) / 2
    return avg

"""Using skew distribution for weighted random yards and weighted random time"""

#Defines random yards function based on right-skew distribution
#We can do more testing on data to get exact skew values for rush and pass

def random_yards_time(mean, sd, skewness):
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
  rand_yards_time = skewnorm.rvs(skewness, loc=mean, scale=sd, size=1)
  return rand_yards_time

"""Dealing with penalties"""

def percent_chance_penalty(play_type):
  """
  Outputs the percent chance of a live ball penalty for any play type.
  :param play_type: Play type corresponding to column name of nfls data frame.
  :type play_type: string
  :return: Percent chance of a penalty on a specified play type.
  """
  new = nfls[nfls[play_type] == 1] #Filter data based on play type
  count = 0
  total = 0
  for i in new["penalty"]:
    count += i
    total += 1
  chance = count / total
  return chance

"""Outputting a random outcome based on normalized weighted probabilities

"""

#Demo functions for defining probabilities of each outcome when a team is on offense.

def define_probs(offense, defense):
  """
  Outputs the probability of a rush or a pass based on the offense and defense
  :param offense: Team abbreviation of team on offense.
  :type offense: string
  :param defense: Team abbreviation of team on defense.
  :type defense: string
  :return: Probabilities for passing and rushing attempts
  """
  outcomes = ["rush_attempt", "pass_attempt"]
  probs = []
  for outcome in range(len(outcomes)):
    prob = average_off_def(offense = offense, defense = defense, play_type = outcomes[outcome], funcname = play_percent)
    probs.append(prob)
  return probs

def normalize_probs(probs):
  """
  Outputs normalized probabilities of passing and rushing (so they add up to exactly 1).
  :param probs: Two element list of probabilities of rushing and passing.
  :type probs: list
  :return: Normalized probabilities for passing and rushing attempts
  """
  total = 0
  normalized_probs = []
  for p in probs:
    total += p
  for p in probs:
    normal_prob = p / total
    normalized_probs.append(normal_prob)
  return normalized_probs

def choose_outcome(norm_probs):
  """
  Outputs a random play_type based on the normalized weights
  :param norm_probs: Two element list of normalized probabilities of rushing and passing.
  :type norm_probs: list
  :return: Passing attempt or rushing attempt as a string
  """
  outcomes = ["rush_attempt", "pass_attempt"]
  choice = random.choices(outcomes, weights=norm_probs, k=1)
  return choice

"""Switch sides (for game loop)"""

def switch_sides(offense, defense):
  """
  Switches offense and defense.
  :param offense: Team abbreviation of team on offense.
  :type offense: string
  :param defense: Team abbreviation of team on defense.
  :type defense: string
  :return: Defense and offense are swapped
  """
  return defense, offense

def convert_time_to_seconds(time):
    """
    Converts game clock to seconds.
    :param time: time in minutes:seconds form
    :type time: string
    :return: Time in seconds.
    """
    if not time:
      return None #handles None values
    minutes, seconds = time.split(':')
    return int(minutes) * 60 + int(seconds)

def avg_time(play_type):
  """
  Finds the average time_elapsed for a play_type.
  :param play_type: Play type corresponding to column name of nfls data frame.
  :type play_type: string
  :return: Average time in seconds of a specified play_type.
  """
  time_seconds = []
  for time in nfls["time"]:
    time_seconds.append(convert_time_to_seconds(time))
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

"""More Penalty Analysis:
Penalty yards and time is an interesting factor. For penalties of 10 and 15 yards, time will always come off the clock. 5 yard penalties can be pre-play penalties so I'm going to make a check for 5 yard penalties. Also going to install a check for pass interference that will go in the passing section of the game loop. This section also can output a random penalty based on probabilities for any type of play. Based on the penalty a random amount of yards will be assesed based on their average yards. Also semi-manually classified all penalties into offensive, defensive, and special teams penalties.
"""

#Updated penalty check for passing or rushing play
def pen_probs(play_type):
  """
  Finds the probability of every penalty and the average yards of every penalty for a specified play_type (rush or pass).
  :param play_type: Play type corresponding to column name of nfls data frame.
  :type play_type: string
  :return: Two lists of probabilities of each penalty type and average yards for each penalty type.
  """
  unique_values = nfls['penalty_type'].unique() #All unique penalty names
  new = nfls[(nfls[play_type] == 1) & (nfls["penalty"]==1)]
  penalty_frequencies = [0] * len(unique_values)
  penalty_yds = [0] * len(unique_values)
  penalty_probs = []
  penalty_avgs = []
  for i in new.index:
    for k in range(len(unique_values)):
      if unique_values[k] == new.loc[i, "penalty_type"]:
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

def flag_yards(flag_type, play_type):
  """
  Defines the yards of each penalty type defining it as 5, 10, or 15 based on the average yards and the spot foul of defensive pass interference.
  :param flag_type: Penalty name.
  :type flag_type: string
  :param play_type: Play type corresponding to column name of nfls data frame.
  :type play_type: string
  :return: Yards for a penalty.
  """
  unique_values = nfls['penalty_type'].unique()
  penalty_avgs = pen_probs(play_type)[1]
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
  return yards

def random_penalty(play_type):
  """
  Outputs a random penalty name based on the proabilities for every penalty of a certain play_type.
  :param play_type: Play type corresponding to column name of nfls data frame.
  :type play_type: string
  :return: A random penalty name as a string
  """
  pen_types = nfls['penalty_type'].unique()
  pen_prob, penalty_avgs = pen_probs(play_type)
  penalty_type = random.choices(pen_types, weights = pen_prob, k =1)
  return penalty_type

def avg_pen_time(penalty_type):
  """
  Outputs the average elapsed time for plays that have a certain penalty type
  :param penalty_type: Penalty name.
  :type penalty_type: string
  :return: Average time elapsed in seconds for a penalty type.
  """
  time_seconds = []
  for time in nfls["time"]:
    time_seconds.append(convert_time_to_seconds(time))
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

def offensive_pens():
  """
  Outputs a list of all penalties that can only be called on the offense.
  :return: List of offensive penalties.
  """
  off_pens = []
  for i in nfls['penalty_type'].unique():
    if (isinstance(i, str) and "Offensive" in i): #Avoid problems with None
      off_pens.append(i)
  other_off_pens = ["Illegal Block Above the Waist", "Ineligible Downfield Pass", "False Start", "Delay of Game", "Illegal Shift", "Illegal Formation", "Illegal Motion", "Low Block", "Intentional Grounding", "Illegal Blindside Block", "Chop Block", "Illegal Forward Pass", "Illegal Peelback", "Illegal Touch Pass", "Illegal Crackback", "Illegal Double-Team Block", "Clipping"]
  off_pens.extend(other_off_pens)
  return off_pens

def defensive_pens():
  """
  Outputs a list of all penalties that can only be called on the defense.
  :return: List of defensive penalties.
  """
  def_pens = []
  for i in nfls['penalty_type'].unique():
    if (isinstance(i, str) and "Defensive" in i):
      def_pens.append(i)
  other_def_pens = ["Roughing the Passer", "Illegal Contact", "Running Into the Kicker", "Offside on Free Kick", "Illegal Touch Kick", "Neutral Zone Infraction", "Roughing the Kicker", "Ineligible Downfield Kick", "Horse Collar Tackle", "Fair Catch Interference", "Leverage", "Leaping", "Kick Catch Interference"]
  def_pens.extend(other_def_pens)
  return def_pens

"""Field Goal Checks (for now we will use condition down = 4 and current Position > 60). This function outputs a chance of successful field goal based on offense team and currentPosition"""

def field_goal_percentage(currentPosition, team):
  """
  Calculates the field goal percentage of a team for kicks within 5 yards of 100 - currentPostion
  :param currentPosition: Position on field for offense (1-100)
  :type currentPosition: float
  :param team: Abbreviation of offensive team name.
  :type team: string
  :return: Decimal representation of field goal percentage
  """
  fg = nfls[(nfls["field_goal_attempt"]== 1) & (abs((nfls["yardline_100"] - (100-currentPosition))) <= 5) & (nfls["posteam"]== team) ] #Creates new df for fg attempts and the yardline being within 5 of the currentPosition
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

"""Fumble Check"""

def fumble_chance(play_type, off, deff):
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

def int_chance(off, deff):
  """
  Calculates the chance of an interception based on offense and defense.
  :param off: Abbreviation of offense.
  :type off: string
  :param deff: Abbreviation of defense.
  :type deff: string
  :return: Decimal representation of interception chance.
  """
  play_off = nfls[(nfls["pass_attempt"] == 1) & (nfls["posteam"] == off)]
  count_off = 0
  total_off = 0
  for i in play_off["interception"]:
    count_off += i
    total_off += 1
  int_off = count_off / total_off
  play_def = nfls[(nfls["pass_attempt"] == 1) & (nfls["defteam"] == deff)]
  count_def = 0
  total_def = 0
  for i in play_def["interception"]:
    count_def += i
    total_def += 1
  int_def = count_def / total_def
  int_pct = (int_off + int_def) / 2
  return int_pct

"""Punt Check / Simulate Punt Yardage: preliminary conditions: (Current Position < 60, down = 4) Function also works for kickoffs (puntorkick). Note that kickoffs will always happen at currentPosition = 35 and take place after the offense scores a TD or Field Goal."""



def punt_kick_simulator(off, currentPosition, puntorkick):
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
  punt_df = nfls[(nfls[puntorkick] == 1) & (nfls["posteam"]==off)]
  count = 0
  total = 0
  for i in punt_df["kick_distance"]:
    count += i
    total += 1
  punt_avg = count / total
  punt_sd = np.std(punt_df["kick_distance"])
  skewness = skew(punt_df["kick_distance"])
  while True: #Check that punt or kick isn't too far
    rand_punt = skewnorm.rvs(skewness, punt_avg, punt_sd, 1)
    if rand_punt < ((100- currentPosition) + 10): #Represents currentPosition + end zone length because punts can land in endzone
      break
  return rand_punt[0]

"""Pre Snap Penalties (No time off clock)"""

def percent_chance_pre_snap_penalty():
  """
  Oututs the percent chance of a pre_snap_penalty.
  :param play_type: Play type corresponding to column name of nfls data frame.
  :type play_type: string
  :return: Percent chance of any pre_snap penalty.
  """
  count = 0
  total = 0
  pre_snap_pens = ["False Start", "Delay of Game", "Defensive Delay of Game", "Encroachment", "Neutral Zone Infraction"]
  for idx, i in enumerate(nfls["penalty"]):
    if nfls.loc[idx, "penalty_type"] in pre_snap_pens:
      count += i
      total += 1
    else:
      total += 1
  chance = count / total
  return chance

def pre_snap_pen_chance():
  """
  Outputs a list of probabilities of a pre snap penalty and a list of average yards for each penalty.
  :return: One list of probabilities and one list of average yards.
  """
  pre_snap_pen = ["False Start", "Delay of Game", "Defensive Delay of Game", "Encroachment", "Neutral Zone Infraction"] #All unique pre snappenalty names
  new = nfls[nfls["penalty"]== 1]
  penalty_frequencies = [0] * len(pre_snap_pen)
  penalty_yds = [0] * len(pre_snap_pen)
  penalty_probs = []
  penalty_avgs = []
  for i in new.index:
    for k in range(len(pre_snap_pen)):
      if pre_snap_pen[k] == new.loc[i, "penalty_type"]:
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

percent_chance_pre_snap_penalty()

"""Another condition: since we haven't used machine learning to analyze play decisions based on time, down, score, etc. (yet?) we will need to use an arbitrary condition for a team to "go for it" on fourth down. I would say currentPosition between [50, 60), down = 4, and downLine < 2.

Note that we also need to add a safety check in the loop. If a team is sack or has negative rush/pass yards at a low current position there's a chance their currentPosition becomes negative. If, so the defense is awarded 2 points and receives a kickoff starting at the 20 yard line.

Sack check
"""

def sack_chance(off, deff):
  """
  Calculates the chance of an interception based on offense and defense.
  :param off: Abbreviation of offense.
  :type off: string
  :param deff: Abbreviation of defense.
  :type deff: string
  :return: Decimal representation of interception chance.
  """
  play_off = nfls[(nfls["pass_attempt"] == 1) & (nfls["posteam"] == off)]
  count_off = 0
  total_off = 0
  for i in play_off["sack"]:
    count_off += i
    total_off += 1
  sack_off = count_off / total_off
  play_def = nfls[(nfls["pass_attempt"] == 1) & (nfls["defteam"] == deff)]
  count_def = 0
  total_def = 0
  for i in play_def["sack"]:
    count_def += i
    total_def += 1
  sack_def = count_def / total_def
  sack_pct = (sack_off + sack_def) / 2
  return sack_pct